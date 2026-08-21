#!/usr/bin/env python3
"""문제를 풀지 않은 초기 상태에서도 전체 폴더 구성을 검증한다."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

try:
    from .fuzz_case_bank import GENERATORS
    from .input_constraints import constraint_errors
    from .problem_paths import learning_order, parse_problem_directory
except ImportError:
    from fuzz_case_bank import GENERATORS
    from input_constraints import constraint_errors
    from problem_paths import learning_order, parse_problem_directory


ROOT = Path(__file__).resolve().parents[1]


def validate_problem(directory: Path) -> list[str]:
    errors: list[str] = []
    try:
        actual_order, lesson_id, _ = parse_problem_directory(directory)
        expected_order = learning_order(directory.parent, lesson_id)
        if actual_order != expected_order:
            errors.append(
                f"{directory.relative_to(ROOT)}: 학습 순서 {actual_order:02d}, "
                f"기대 {expected_order:02d}"
            )
    except ValueError as error:
        errors.append(f"{directory.relative_to(ROOT)}: {error}")
    required = (
        "README.md",
        "PROBLEM.md",
        "solution.py",
        "tests.json",
        "edge_tests.json",
        "HINTS.md",
    )
    for name in required:
        if not (directory / name).is_file():
            errors.append(f"{directory.relative_to(ROOT)}: {name} 없음")
    if errors:
        return errors

    try:
        solution_text = (directory / "solution.py").read_text(encoding="utf-8")
        tree = ast.parse(solution_text)
        solutions = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "solution"
        ]
        if len(solutions) != 1 or isinstance(solutions[0], ast.AsyncFunctionDef):
            errors.append(
                f"{directory.relative_to(ROOT)}: 동기 solution 함수가 정확히 하나여야 함"
            )
        parameter_count = len(solutions[0].args.args) if solutions else -1
        parameter_names = (
            [argument.arg for argument in solutions[0].args.args] if solutions else []
        )
        if "# LOCAL_TEST_RUNNER" not in solution_text:
            errors.append(
                f"{directory.relative_to(ROOT)}: solution.py 직접 실행 블록 없음"
            )
    except (OSError, SyntaxError) as error:
        errors.append(f"{directory.relative_to(ROOT)}: solution.py 오류: {error}")
        parameter_count = -1
        parameter_names = []

    cases: list[dict[str, object]] = []
    try:
        cases = json.loads((directory / "tests.json").read_text(encoding="utf-8"))
        if not isinstance(cases, list) or not cases:
            errors.append(f"{directory.relative_to(ROOT)}: 테스트가 한 개 이상이어야 함")
        else:
            for index, case in enumerate(cases, start=1):
                if set(case) != {"name", "args", "expected"}:
                    errors.append(
                        f"{directory.relative_to(ROOT)}: 테스트 {index} 필드 오류"
                    )
                elif not isinstance(case["args"], list):
                    errors.append(
                        f"{directory.relative_to(ROOT)}: 테스트 {index} args는 배열이어야 함"
                    )
                elif len(case["args"]) != parameter_count:
                    errors.append(
                        f"{directory.relative_to(ROOT)}: 테스트 {index} 인자 수 불일치"
                    )
                else:
                    for violation in constraint_errors(lesson_id, case["args"]):
                        errors.append(
                            f"{directory.relative_to(ROOT)}: 공개 테스트 {index} "
                            f"명세 위반 - {violation}"
                        )
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{directory.relative_to(ROOT)}: tests.json 오류: {error}")

    edge_cases: list[dict[str, object]] = []
    try:
        edge_cases = json.loads(
            (directory / "edge_tests.json").read_text(encoding="utf-8")
        )
        if not isinstance(edge_cases, list) or not edge_cases:
            errors.append(
                f"{directory.relative_to(ROOT)}: 경계 테스트가 한 개 이상이어야 함"
            )
        else:
            for index, case in enumerate(edge_cases, start=1):
                if set(case) != {"name", "args", "expected"}:
                    errors.append(
                        f"{directory.relative_to(ROOT)}: 경계 테스트 {index} 필드 오류"
                    )
                elif not isinstance(case["args"], list):
                    errors.append(
                        f"{directory.relative_to(ROOT)}: 경계 테스트 {index} args는 배열이어야 함"
                    )
                elif len(case["args"]) != parameter_count:
                    errors.append(
                        f"{directory.relative_to(ROOT)}: 경계 테스트 {index} 인자 수 불일치"
                    )
                else:
                    for violation in constraint_errors(lesson_id, case["args"]):
                        errors.append(
                            f"{directory.relative_to(ROOT)}: 경계 테스트 {index} "
                            f"명세 위반 - {violation}"
                        )
    except (OSError, json.JSONDecodeError) as error:
        errors.append(
            f"{directory.relative_to(ROOT)}: edge_tests.json 오류: {error}"
        )

    try:
        problem_text = (directory / "PROBLEM.md").read_text(encoding="utf-8")
        required_sections = (
            "## 문제",
            "## 함수 인터페이스",
            "## 규칙과 제한사항",
            "## 공개 예제",
            "## 예제 해설",
        )
        for section in required_sections:
            if section not in problem_text:
                errors.append(
                    f"{directory.relative_to(ROOT)}: PROBLEM.md에 {section!r} 없음"
                )
        expected_signature = f"def solution({', '.join(parameter_names)}):"
        if expected_signature not in problem_text:
            errors.append(
                f"{directory.relative_to(ROOT)}: 문서와 solution 함수 시그니처 불일치"
            )
        if problem_text.count("### 예제 ") != len(cases):
            errors.append(
                f"{directory.relative_to(ROOT)}: 문서 예제 수와 tests.json 불일치"
            )
    except OSError as error:
        errors.append(f"{directory.relative_to(ROOT)}: PROBLEM.md 오류: {error}")

    try:
        hints_text = (directory / "HINTS.md").read_text(encoding="utf-8")
        for phrase in ("2단계 — 핵심 접근", "상태 정의:", "핵심 불변식:", "구현 순서 의사코드"):
            if phrase not in hints_text:
                errors.append(
                    f"{directory.relative_to(ROOT)}: HINTS.md에 {phrase!r} 없음"
                )
        if "def solution(" in hints_text:
            errors.append(
                f"{directory.relative_to(ROOT)}: HINTS.md가 정답 함수 전문을 노출함"
            )
    except OSError as error:
        errors.append(f"{directory.relative_to(ROOT)}: HINTS.md 오류: {error}")

    solution_directory = directory / "solutions"
    for name in ("README.md", "SOURCES.md", "recommended.py", "alternative.py"):
        source = solution_directory / name
        if not source.is_file():
            errors.append(
                f"{directory.relative_to(ROOT)}: solutions/{name} 없음"
            )
            continue
        if name.endswith(".py"):
            try:
                example_text = source.read_text(encoding="utf-8")
                example_tree = ast.parse(example_text)
                functions = [
                    node
                    for node in example_tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "solution"
                ]
                if len(functions) != 1:
                    errors.append(
                        f"{directory.relative_to(ROOT)}: solutions/{name}의 "
                        "solution 함수는 정확히 하나여야 함"
                    )
                function_comments = []
                if len(functions) == 1:
                    lines = example_text.splitlines()
                    function_comments = [
                        line
                        for line in lines[functions[0].lineno : functions[0].end_lineno]
                        if line.lstrip().startswith("#")
                    ]
                if len(function_comments) < 2:
                    errors.append(
                        f"{directory.relative_to(ROOT)}: solutions/{name}의 solution 내부 "
                        "학습 주석이 2개 미만"
                    )
            except (OSError, SyntaxError) as error:
                errors.append(
                    f"{directory.relative_to(ROOT)}: solutions/{name} 오류: {error}"
                )
    try:
        explanation = (solution_directory / "README.md").read_text(encoding="utf-8")
        if "- 적용 범위:" not in explanation or "- 문제별 주의:" not in explanation:
            errors.append(
                f"{directory.relative_to(ROOT)}: 풀이 README의 적용 범위·문제별 주의 분리 필요"
            )
    except OSError:
        pass
    return errors


def main() -> int:
    categories = sorted(ROOT.glob("[0-9][0-9]_*"))
    directories = sorted(path.parent for path in ROOT.glob("[0-9][0-9]_*/**/tests.json"))
    errors: list[str] = []
    if len(categories) != 10:
        errors.append(f"유형 폴더: 기대 10개, 실제 {len(categories)}개")
    if len(directories) != 57:
        errors.append(f"문제 폴더: 기대 57개, 실제 {len(directories)}개")
    for category in categories:
        if not (category / "README.md").is_file():
            errors.append(f"{category.relative_to(ROOT)}: README.md 없음")
        guide = category / "MASTERY_GUIDE.md"
        if not guide.is_file():
            errors.append(f"{category.relative_to(ROOT)}: MASTERY_GUIDE.md 없음")
        else:
            guide_text = guide.read_text(encoding="utf-8")
            for phrase in ("사고", "학습", "마스터 체크리스트"):
                if phrase not in guide_text:
                    errors.append(
                        f"{category.relative_to(ROOT)}: 학습 가이드에 {phrase!r} 없음"
                    )
    if not (ROOT / "MASTER_ROADMAP.md").is_file():
        errors.append("MASTER_ROADMAP.md 없음")
    required_tools = (
        "direct_runner.py",
        "progress.py",
        "mock.py",
        "new_problem.py",
        "stress.py",
        "fuzz.py",
        "fuzz_case_bank.py",
        "input_constraints.py",
        "pedagogy_bank.py",
    )
    for tool in required_tools:
        if not (ROOT / "tools" / tool).is_file():
            errors.append(f"tools/{tool} 없음")
    for snippet in ("README.md", "bfs.py", "union_find.py", "dijkstra.py"):
        if not (ROOT / "snippets" / snippet).is_file():
            errors.append(f"snippets/{snippet} 없음")
    registered_ids = {
        parse_problem_directory(directory)[1] for directory in directories
    }
    if set(GENERATORS) != registered_ids:
        errors.append(
            "랜덤 테스트 생성기 ID 불일치: "
            f"missing={sorted(registered_ids - set(GENERATORS))}, "
            f"extra={sorted(set(GENERATORS) - registered_ids)}"
        )
    for directory in directories:
        errors.extend(validate_problem(directory))

    if errors:
        print("구성 검증 실패:")
        for error in errors:
            print(f"- {error}")
        return 1
    public_case_count = sum(
        len(json.loads((directory / "tests.json").read_text(encoding="utf-8")))
        for directory in directories
    )
    edge_case_count = sum(
        len(json.loads((directory / "edge_tests.json").read_text(encoding="utf-8")))
        for directory in directories
    )
    print(
        f"구성 검증 완료: 유형 {len(categories)}개, 문제 {len(directories)}개, "
        f"공개 예제 {public_case_count}개, 경계 테스트 {edge_case_count}개"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
