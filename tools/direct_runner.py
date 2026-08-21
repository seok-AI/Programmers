#!/usr/bin/env python3
"""solution.py를 직접 실행할 때 사용하는 상세 로컬 테스트 실행기."""

from __future__ import annotations

import contextlib
import copy
import inspect
import io
import json
import time
import traceback
from pathlib import Path
from pprint import pformat
from typing import Any, Callable

from .judge import is_equal, load_cases
from .problem_paths import problem_id


def display(value: Any) -> str:
    """중첩 리스트도 잘 보이도록 값을 줄바꿈해 표현한다."""
    return pformat(value, width=100, sort_dicts=False)


def named_arguments(function: Callable[..., Any], arguments: list[Any]) -> dict[str, Any]:
    """테스트의 위치 인자를 solution 함수의 매개변수 이름과 연결한다."""
    names = list(inspect.signature(function).parameters)
    return {
        names[index] if index < len(names) else f"arg{index + 1}": value
        for index, value in enumerate(arguments)
    }


def run_local_tests(
    function: Callable[..., Any],
    tests_path: str | Path,
    *,
    show_passed_details: bool = True,
    fuzz_cases: int = 500,
) -> int:
    """고정 사례는 상세히, 대량 랜덤 사례는 실패만 출력하고 종료 코드를 반환한다."""
    path = Path(tests_path)
    try:
        cases = load_cases(path.parent)
    except (OSError, json.JSONDecodeError) as error:
        print(f"테스트 파일을 읽지 못했습니다: {path}")
        print(f"{type(error).__name__}: {error}")
        return 2

    print(f"문제 폴더: {path.parent}")
    sources = [name for name in ("tests.json", "edge_tests.json") if (path.parent / name).is_file()]
    print(f"테스트 파일: {', '.join(sources)} / 총 {len(cases)}개")
    print("=" * 72)

    passed = failed = 0
    total_started = time.perf_counter()
    for index, case in enumerate(cases, start=1):
        name = case.get("name", f"테스트 {index}")
        arguments = copy.deepcopy(case["args"])
        captured_stdout = io.StringIO()
        started = time.perf_counter()
        error: Exception | None = None
        actual: Any = None

        try:
            with contextlib.redirect_stdout(captured_stdout):
                actual = function(*arguments)
        except Exception as caught:  # 디버깅할 수 있도록 사용자 코드의 예외도 계속 표시한다.
            error = caught
        elapsed_ms = (time.perf_counter() - started) * 1000
        success = error is None and is_equal(actual, case["expected"])
        passed += success
        failed += not success

        print(f"[{index}/{len(cases)}] {'PASS' if success else 'FAIL'} - {name}")
        print(f"입력 인자:\n{display(named_arguments(function, case['args']))}")
        print(f"기대 결과 ({type(case['expected']).__name__}):\n{display(case['expected'])}")
        if error is None:
            if show_passed_details or not success:
                print(f"실행 결과 ({type(actual).__name__}):\n{display(actual)}")
        else:
            print(f"발생 예외: {type(error).__name__}: {error}")
            print("traceback:")
            print("".join(traceback.format_exception(error)).rstrip())
        printed = captured_stdout.getvalue()
        if printed:
            print("solution 함수의 stdout:")
            print(printed.rstrip())
        print(f"실행 시간: {elapsed_ms:.3f} ms")
        print("-" * 72)

    fuzz_passed = fuzz_failed = fuzz_requested = oracle_errors = 0
    if fuzz_cases > 0:
        try:
            from .fuzz import GENERATORS, print_report, run_fuzz

            lesson_id = problem_id(path.parent)
            if lesson_id in GENERATORS:
                print("\n결정적 랜덤 교차검증")
                print("=" * 72)
                report = run_fuzz(function, lesson_id, count=fuzz_cases)
                print_report(report, show_failures=True)
                fuzz_passed = report.passed
                fuzz_failed = report.failed
                fuzz_requested = report.requested
                oracle_errors = report.oracle_errors
            else:
                print("\n추가 문제에는 등록된 랜덤 테스트 생성기가 없어 고정 사례만 실행했습니다.")
        except Exception as error:
            oracle_errors += 1
            print(f"\n랜덤 테스트 구성 오류: {type(error).__name__}: {error}")

    total_ms = (time.perf_counter() - total_started) * 1000
    print("\n" + "=" * 72)
    print(
        f"최종 결과: 고정 {passed}개 통과 / {failed}개 실패, "
        f"랜덤 {fuzz_passed}/{fuzz_requested} 통과, "
        f"오라클 오류 {oracle_errors}개 / 총 {total_ms:.3f} ms"
    )
    return 0 if failed == fuzz_failed == oracle_errors == 0 else 1
