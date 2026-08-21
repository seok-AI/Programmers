#!/usr/bin/env python3
"""현재 solution.py의 시도·공개/경계 테스트 통과 현황을 자동 집계한다."""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
from dataclasses import dataclass
from pathlib import Path

try:
    from .fuzz import GENERATORS, run_fuzz
    from .judge import ROOT, discover, load_cases, load_solution, run_problem
    from .problem_paths import problem_id
except ImportError:
    from fuzz import GENERATORS, run_fuzz
    from judge import ROOT, discover, load_cases, load_solution, run_problem
    from problem_paths import problem_id


@dataclass(frozen=True)
class Result:
    directory: Path
    state: str
    passed: int
    total: int


def is_attempted(source: Path) -> bool:
    """초기 ``pass`` 템플릿과 사용자가 작성하기 시작한 함수를 구분한다."""
    try:
        tree = ast.parse(source.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return True
    function = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "solution"
        ),
        None,
    )
    return function is None or not (
        len(function.body) == 1 and isinstance(function.body[0], ast.Pass)
    )


def evaluate(directory: Path, timeout: float, fuzz_cases: int) -> Result:
    lesson_id = problem_id(directory)
    random_total = fuzz_cases if lesson_id in GENERATORS else 0
    total = len(load_cases(directory)) + random_total
    if not is_attempted(directory / "solution.py"):
        return Result(directory, "미시도", 0, total)
    # 세부 실패 출력은 대시보드에서 숨기고 --details일 때 재현 명령만 안내한다.
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        passed, failed = run_problem(directory, timeout)
        if failed == 0 and random_total:
            report = run_fuzz(
                load_solution(directory),
                lesson_id,
                count=fuzz_cases,
                timeout=timeout,
            )
            passed += report.passed
            failed += report.failed + report.oracle_errors
    state = "통과" if failed == 0 and passed == total else "진행중"
    return Result(directory, state, passed, total)


def main() -> int:
    parser = argparse.ArgumentParser(description="문제 풀이 진척 자동 집계")
    parser.add_argument("--category", help="예: 04, 정렬, 04_정렬")
    parser.add_argument("--timeout", type=float, default=2.0, help="테스트당 제한 시간")
    parser.add_argument("--fuzz-cases", type=int, default=100, help="시도한 문제당 랜덤 사례 수")
    parser.add_argument("--details", action="store_true", help="문제별 상태도 출력")
    args = parser.parse_args()
    if args.timeout <= 0 or args.fuzz_cases < 0:
        parser.error("--timeout은 양수, --fuzz-cases는 0 이상이어야 합니다.")

    problems = discover()
    if args.category:
        problems = [
            path for path in problems if args.category in path.parent.name
        ]
    if not problems:
        parser.error("조건에 맞는 문제가 없습니다.")

    results = [evaluate(directory, args.timeout, args.fuzz_cases) for directory in problems]
    categories = sorted({result.directory.parent.name for result in results})

    print("| 유형 | 통과 | 진행중 | 미시도 | 테스트 통과 |")
    print("|---|---:|---:|---:|---:|")
    for category in categories:
        rows = [result for result in results if result.directory.parent.name == category]
        counts = {state: sum(row.state == state for row in rows) for state in ("통과", "진행중", "미시도")}
        passed = sum(row.passed for row in rows)
        total = sum(row.total for row in rows)
        print(
            f"| {category} | {counts['통과']} | {counts['진행중']} | "
            f"{counts['미시도']} | {passed}/{total} |"
        )

    solved = sum(result.state == "통과" for result in results)
    attempted = sum(result.state != "미시도" for result in results)
    passed_cases = sum(result.passed for result in results)
    total_cases = sum(result.total for result in results)
    print(
        f"\n전체: 문제 {solved}/{len(results)} 통과, {attempted}개 시도, "
        f"테스트 {passed_cases}/{total_cases} 통과"
    )

    if args.details:
        print("\n| 상태 | 문제 | 테스트 | 재현 명령 |")
        print("|---|---|---:|---|")
        for result in results:
            relative = result.directory.relative_to(ROOT)
            command = f'python3 "{relative}/solution.py"'
            print(
                f"| {result.state} | {relative} | {result.passed}/{result.total} | "
                f"`{command}` |"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
