#!/usr/bin/env python3
"""모든 권장/대안 예시 풀이를 저장된 공개·경계 테스트로 검증한다."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

from judge import is_equal, load_cases, short_repr


ROOT = Path(__file__).resolve().parents[1]


def load_function(source: Path):
    module_name = "example_" + hashlib.sha1(str(source).encode()).hexdigest()
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise ImportError(f"불러올 수 없는 파일: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, "solution", None)
    if not callable(function):
        raise AttributeError("호출 가능한 solution 함수가 없습니다.")
    return function


def main() -> int:
    problems = sorted(path.parent for path in ROOT.glob("[0-9][0-9]_*/**/tests.json"))
    passed = failed = 0
    for problem in problems:
        cases = load_cases(problem)
        for variant in ("recommended", "alternative"):
            source = problem / "solutions" / f"{variant}.py"
            try:
                solution = load_function(source)
                for case in cases:
                    actual = solution(*copy.deepcopy(case["args"]))
                    if not is_equal(actual, case["expected"]):
                        failed += 1
                        print(
                            f"FAIL {problem.relative_to(ROOT)}/{variant}: "
                            f"{case['name']} 기대={short_repr(case['expected'])} "
                            f"실제={short_repr(actual)}"
                        )
                    else:
                        passed += 1
            except Exception as error:
                failed += 1
                print(
                    f"ERROR {problem.relative_to(ROOT)}/{variant}: "
                    f"{type(error).__name__}: {error}"
                )
    print(f"예시 풀이 검증(공개+경계): {passed}개 통과 / {failed}개 실패")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
