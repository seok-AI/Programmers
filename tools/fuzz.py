#!/usr/bin/env python3
"""57문제의 결정적 랜덤 입력을 권장·대안 풀이와 교차검증한다."""

from __future__ import annotations

import argparse
import contextlib
import copy
import io
import random
import signal
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from .fuzz_case_bank import GENERATORS
    from .input_constraints import constraint_errors
    from .judge import ROOT, discover, is_equal, load_solution as load_candidate, resolve_problem, short_repr
    from .problem_paths import problem_id
    from .stress import load_solution as load_example
except ImportError:
    from fuzz_case_bank import GENERATORS
    from input_constraints import constraint_errors
    from judge import ROOT, discover, is_equal, load_solution as load_candidate, resolve_problem, short_repr
    from problem_paths import problem_id
    from stress import load_solution as load_example


DEFAULT_SEED = 20260803


class FuzzTimeout(TimeoutError):
    pass


def timeout_handler(signum: int, frame: object) -> None:
    del signum, frame
    raise FuzzTimeout("랜덤 테스트 제한 시간 초과")


@dataclass(frozen=True)
class Failure:
    index: int
    arguments: list[object]
    expected: object | None
    actual: object | None
    message: str
    stdout: str = ""


@dataclass(frozen=True)
class Report:
    lesson_id: int
    requested: int
    passed: int
    failed: int
    oracle_errors: int
    elapsed: float
    failures: tuple[Failure, ...]


def call(
    function: Callable[..., Any], arguments: list[object], timeout: float
) -> tuple[object | None, Exception | None, str]:
    output = io.StringIO()
    try:
        signal.setitimer(signal.ITIMER_REAL, timeout)
        with contextlib.redirect_stdout(output):
            actual = function(*copy.deepcopy(arguments))
        return actual, None, output.getvalue()
    except Exception as error:
        return None, error, output.getvalue()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def run_fuzz(
    function: Callable[..., Any] | None,
    lesson_id: int,
    *,
    count: int = 500,
    seed: int = DEFAULT_SEED,
    timeout: float = 1.0,
    max_failures: int = 5,
) -> Report:
    """예시 풀이 두 개가 합의한 결과와 candidate를 비교한다.

    ``function``이 None이면 생성기와 두 예시 풀이의 합의만 검사한다.
    """
    if lesson_id not in GENERATORS:
        raise ValueError(f"랜덤 테스트 생성기가 없는 문제입니다: {lesson_id}")
    if count <= 0 or timeout <= 0 or max_failures <= 0:
        raise ValueError("count, timeout, max_failures는 0보다 커야 합니다.")

    recommended = load_example(lesson_id, "recommended")
    alternative = load_example(lesson_id, "alternative")
    # 문제별 시드를 분리하면 --all과 단일 실행이 정확히 같은 사례를 만든다.
    rng = random.Random((seed << 20) ^ lesson_id)
    generator = GENERATORS[lesson_id]
    failures: list[Failure] = []
    passed = failed = oracle_errors = 0
    started = time.perf_counter()
    previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
    try:
        for index in range(1, count + 1):
            arguments = generator(rng)
            violations = constraint_errors(lesson_id, arguments)
            if violations:
                oracle_errors += 1
                failures.append(
                    Failure(
                        index,
                        arguments,
                        None,
                        None,
                        "랜덤 생성 입력의 명세 위반: " + "; ".join(violations),
                    )
                )
                break
            expected, first_error, _ = call(recommended, arguments, timeout)
            alternative_result, second_error, _ = call(alternative, arguments, timeout)
            if first_error or second_error or not is_equal(expected, alternative_result):
                oracle_errors += 1
                message = (
                    f"권장 예외={first_error!r}, 대안 예외={second_error!r}"
                    if first_error or second_error
                    else "권장·대안 풀이 결과 불일치"
                )
                failures.append(
                    Failure(index, arguments, expected, alternative_result, message)
                )
                # 기대값 자체가 불확실하면 이후 candidate 판정을 계속하지 않는다.
                break

            if function is None:
                passed += 1
                continue
            actual, candidate_error, printed = call(function, arguments, timeout)
            if candidate_error is None and is_equal(actual, expected):
                passed += 1
                continue
            failed += 1
            message = (
                f"{type(candidate_error).__name__}: {candidate_error}"
                if candidate_error
                else "기대값과 결과가 다름"
            )
            if len(failures) < max_failures:
                failures.append(
                    Failure(index, arguments, expected, actual, message, printed)
                )
            if failed >= max_failures:
                break
    finally:
        signal.signal(signal.SIGALRM, previous_handler)
    return Report(
        lesson_id,
        count,
        passed,
        failed,
        oracle_errors,
        time.perf_counter() - started,
        tuple(failures),
    )


def print_report(report: Report, *, show_failures: bool = True) -> None:
    status = "PASS" if report.failed == report.oracle_errors == 0 and report.passed == report.requested else "FAIL"
    print(
        f"{status} {report.lesson_id}: 랜덤 {report.passed}/{report.requested} 통과, "
        f"candidate 실패 {report.failed}, 오라클 오류 {report.oracle_errors}, "
        f"{report.elapsed:.3f}초"
    )
    if not show_failures:
        return
    for failure in report.failures:
        print(f"  - 랜덤 사례 #{failure.index}: {failure.message}")
        print(f"    args={short_repr(failure.arguments, 500)}")
        print(f"    expected={short_repr(failure.expected, 300)}")
        print(f"    actual={short_repr(failure.actual, 300)}")
        if failure.stdout:
            print(f"    stdout={short_repr(failure.stdout, 300)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="결정적 랜덤 교차검증")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("problem", nargs="?", help="문제 번호 또는 폴더")
    target.add_argument("--all", action="store_true", help="기본 57문제 전체")
    parser.add_argument("--cases", type=int, default=500, help="문제당 랜덤 사례 수")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="재현용 기준 시드")
    parser.add_argument("--timeout", type=float, default=1.0, help="함수 호출당 제한 시간")
    parser.add_argument("--max-failures", type=int, default=5, help="문제당 조기 중단 실패 수")
    parser.add_argument(
        "--oracles-only",
        action="store_true",
        help="사용자 solution.py 없이 권장·대안 풀이와 생성기만 검사",
    )
    args = parser.parse_args()
    if args.cases <= 0 or args.timeout <= 0 or args.max_failures <= 0:
        parser.error("--cases, --timeout, --max-failures는 0보다 커야 합니다.")

    if args.all:
        selected = [directory for directory in discover() if problem_id(directory) in GENERATORS]
    else:
        try:
            selected = [resolve_problem(args.problem)]
        except ValueError as error:
            parser.error(str(error))
    reports = []
    for directory in selected:
        lesson_id = problem_id(directory)
        if lesson_id not in GENERATORS:
            parser.error(f"추가 문제에는 아직 랜덤 생성기가 없습니다: {lesson_id}")
        function = None if args.oracles_only else load_candidate(directory)
        report = run_fuzz(
            function,
            lesson_id,
            count=args.cases,
            seed=args.seed,
            timeout=args.timeout,
            max_failures=args.max_failures,
        )
        print_report(report)
        reports.append(report)

    passed = sum(
        report.passed == report.requested
        and report.failed == 0
        and report.oracle_errors == 0
        for report in reports
    )
    print(
        f"\n랜덤 검증 결과: {passed}/{len(reports)}문제 통과 "
        f"(문제당 {args.cases}개, seed={args.seed})"
    )
    return 0 if passed == len(reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
