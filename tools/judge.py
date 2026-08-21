#!/usr/bin/env python3
"""프로그래머스의 solution 함수 호출 방식을 흉내 내는 로컬 채점기."""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import signal
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Callable

try:
    from .problem_paths import problem_id
except ImportError:  # python3 tools/judge.py로 직접 실행할 때
    from problem_paths import problem_id


ROOT = Path(__file__).resolve().parents[1]


class CaseTimeoutError(TimeoutError):
    pass


def timeout_handler(signum: int, frame: object) -> None:
    del signum, frame
    raise CaseTimeoutError("제한 시간을 초과했습니다.")


def is_equal(actual: Any, expected: Any) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if isinstance(actual, float) or isinstance(expected, float):
            return math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
        return actual == expected
    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            is_equal(left, right) for left, right in zip(actual, expected)
        )
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            is_equal(actual[key], expected[key]) for key in actual
        )
    return type(actual) is type(expected) and actual == expected


def discover() -> list[Path]:
    main = {path.parent for path in ROOT.glob("[0-9][0-9]_*/**/tests.json")}
    extra = {
        path.parent
        for path in ROOT.glob("extra_problems/[0-9][0-9]_*/**/tests.json")
    }
    return sorted(main | extra)


def load_cases(problem_dir: Path) -> list[dict[str, Any]]:
    """공개 예제와 별도로 관리하는 경계 테스트를 차례로 읽는다."""
    cases: list[dict[str, Any]] = []
    sources = 0
    for filename in ("tests.json", "edge_tests.json"):
        path = problem_dir / filename
        if path.is_file():
            sources += 1
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(loaded, list):
                raise ValueError(f"{filename}의 최상위 값은 배열이어야 합니다.")
            cases.extend(loaded)
    if sources == 0:
        raise FileNotFoundError(f"테스트 파일이 없습니다: {problem_dir}")
    if not cases:
        raise ValueError(f"실행할 테스트가 없습니다: {problem_dir}")
    return cases


def resolve_problem(raw: str) -> Path:
    candidate = (ROOT / raw).resolve()
    if ROOT not in candidate.parents:
        raise ValueError("저장소 밖의 경로는 실행할 수 없습니다.")
    if candidate.is_file():
        candidate = candidate.parent
    if (candidate / "solution.py").is_file() and (candidate / "tests.json").is_file():
        return candidate

    matches = [
        path
        for path in discover()
        if raw in str(path.relative_to(ROOT))
        or (raw.isdigit() and int(raw) == problem_id(path))
    ]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise ValueError(f"문제를 찾지 못했습니다: {raw}")
    choices = "\n".join(f"  - {path.relative_to(ROOT)}" for path in matches)
    raise ValueError(f"경로가 하나로 결정되지 않습니다:\n{choices}")


def load_solution(problem_dir: Path) -> Callable[..., Any]:
    source = problem_dir / "solution.py"
    module_name = "candidate_" + hashlib.sha1(
        str(source).encode("utf-8")
    ).hexdigest()
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise ImportError(f"모듈을 불러올 수 없습니다: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, "solution", None)
    if not callable(function):
        raise AttributeError("solution.py에 호출 가능한 solution 함수가 없습니다.")
    return function


def short_repr(value: Any, limit: int = 240) -> str:
    rendered = repr(value)
    return rendered if len(rendered) <= limit else rendered[: limit - 3] + "..."


def run_problem(problem_dir: Path, timeout_seconds: float) -> tuple[int, int]:
    relative = problem_dir.relative_to(ROOT)
    print(f"\n▶ {relative}")
    try:
        function = load_solution(problem_dir)
        cases = load_cases(problem_dir)
    except Exception as error:
        print(f"  설정 오류: {error}")
        return 0, 1

    passed = 0
    failed = 0
    previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
    try:
        for index, case in enumerate(cases, start=1):
            name = case.get("name", f"테스트 {index}")
            arguments = copy.deepcopy(case["args"])
            output = io.StringIO()
            started = time.perf_counter()
            try:
                signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
                with contextlib.redirect_stdout(output):
                    actual = function(*arguments)
                elapsed_ms = (time.perf_counter() - started) * 1000
                if is_equal(actual, case["expected"]):
                    passed += 1
                    print(f"  ✅ {name} ({elapsed_ms:.2f} ms)")
                else:
                    failed += 1
                    print(f"  ❌ {name} ({elapsed_ms:.2f} ms)")
                    print(f"     기대: {short_repr(case['expected'])}")
                    print(f"     실제: {short_repr(actual)}")
            except CaseTimeoutError:
                failed += 1
                print(f"  ⏱️  {name}: {timeout_seconds:g}초 시간 초과")
            except Exception as error:
                failed += 1
                print(f"  💥 {name}: {type(error).__name__}: {error}")
                traceback.print_exc(limit=3)
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            printed = output.getvalue()
            if printed:
                print("     stdout:", printed.rstrip().replace("\n", "\n             "))
    finally:
        signal.signal(signal.SIGALRM, previous_handler)
    return passed, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="프로그래머스 로컬 공개·경계 테스트 채점기")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("problem", nargs="?", help="문제 폴더, 문제 ID 또는 경로 일부")
    target.add_argument("--all", action="store_true", help="모든 문제 실행")
    target.add_argument("--list", action="store_true", help="문제 목록 출력")
    parser.add_argument(
        "--timeout", type=float, default=2.0, help="테스트 하나의 제한 시간(기본 2초)"
    )
    args = parser.parse_args()

    problems = discover()
    if args.list:
        for problem in problems:
            print(problem.relative_to(ROOT))
        return 0

    if args.timeout <= 0:
        parser.error("--timeout은 0보다 커야 합니다.")

    try:
        selected = problems if args.all else [resolve_problem(args.problem)]
    except ValueError as error:
        parser.error(str(error))

    total_passed = 0
    total_failed = 0
    for problem in selected:
        passed, failed = run_problem(problem, args.timeout)
        total_passed += passed
        total_failed += failed

    print(f"\n결과: {total_passed}개 통과 / {total_failed}개 실패")
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
