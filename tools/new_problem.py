#!/usr/bin/env python3
"""로컬 JSON 명세에서 오프라인 추가 훈련 문제 폴더를 생성한다."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from pprint import pformat

try:
    from .judge import ROOT, discover
    from .problem_paths import LEARNING_ORDERS, parse_problem_directory, problem_id
except ImportError:
    from judge import ROOT, discover
    from problem_paths import LEARNING_ORDERS, parse_problem_directory, problem_id


REQUIRED = {
    "category",
    "lesson_id",
    "title",
    "level",
    "parameters",
    "description",
    "constraints",
    "public_examples",
    "edge_tests",
    "source_url",
}


def validate_cases(
    cases: object, parameter_count: int, label: str
) -> list[dict[str, object]]:
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{label}는 한 개 이상의 배열이어야 합니다.")
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict) or set(case) != {"name", "args", "expected"}:
            raise ValueError(f"{label} {index}: name, args, expected만 있어야 합니다.")
        if not isinstance(case["name"], str) or not case["name"].strip():
            raise ValueError(f"{label} {index}: name이 비었습니다.")
        if not isinstance(case["args"], list) or len(case["args"]) != parameter_count:
            raise ValueError(f"{label} {index}: solution 매개변수 수와 args 길이가 다릅니다.")
    return cases


def load_spec(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != REQUIRED:
        missing = REQUIRED - set(data) if isinstance(data, dict) else REQUIRED
        extra = set(data) - REQUIRED if isinstance(data, dict) else set()
        raise ValueError(f"명세 필드 불일치: missing={sorted(missing)}, extra={sorted(extra)}")
    if data["category"] not in LEARNING_ORDERS:
        raise ValueError(f"category는 다음 중 하나여야 합니다: {', '.join(LEARNING_ORDERS)}")
    if not isinstance(data["lesson_id"], int) or data["lesson_id"] <= 0:
        raise ValueError("lesson_id는 양의 정수여야 합니다.")
    if not isinstance(data["level"], int) or data["level"] not in (1, 2, 3):
        raise ValueError("level은 1, 2, 3 중 하나여야 합니다.")
    if not isinstance(data["title"], str) or not data["title"].strip():
        raise ValueError("title이 비었습니다.")
    if not isinstance(data["description"], str) or not data["description"].strip():
        raise ValueError("description이 비었습니다.")
    constraints = data["constraints"]
    if not isinstance(constraints, list) or not constraints or not all(
        isinstance(item, str) and item.strip() for item in constraints
    ):
        raise ValueError("constraints는 비지 않은 문자열 배열이어야 합니다.")
    parameters = data["parameters"]
    if not isinstance(parameters, list) or not parameters or not all(
        isinstance(name, str) and name.isidentifier() and not name.startswith("_")
        for name in parameters
    ):
        raise ValueError("parameters는 유효한 공개 Python 식별자 배열이어야 합니다.")
    if len(set(parameters)) != len(parameters):
        raise ValueError("parameters에는 중복 이름이 없어야 합니다.")
    validate_cases(data["public_examples"], len(parameters), "public_examples")
    validate_cases(data["edge_tests"], len(parameters), "edge_tests")
    return data


def compact(value: object) -> str:
    return pformat(value, width=10_000, sort_dicts=False).replace("\n", " ")


def render_examples(cases: list[dict[str, object]], parameters: list[str]) -> str:
    blocks = []
    for index, case in enumerate(cases, start=1):
        inputs = "; ".join(
            f"{name} = {compact(value)}"
            for name, value in zip(parameters, case["args"], strict=True)
        )
        output = compact(case["expected"])
        if len(inputs) + len(output) <= 110:
            body = f"| INPUT | OUTPUT |\n|---|---|\n| `{inputs}` | `{output}` |"
        else:
            assignments = "\n".join(
                f"{name} = {pformat(value, width=70, sort_dicts=False)}"
                for name, value in zip(parameters, case["args"], strict=True)
            )
            body = f"**INPUT**\n\n```python\n{assignments}\n```\n\n**OUTPUT**\n\n```python\n{output}\n```"
        blocks.append(f"### 예제 {index}\n\n{body}")
    return "\n\n".join(blocks)


def safe_title(title: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z가-힣_()\-]+", "_", title.strip())
    slug = re.sub(r"_+", "_", slug).strip("_")
    if not slug:
        raise ValueError("제목에서 폴더 이름을 만들 수 없습니다.")
    return slug


def solution_source(title: str, parameters: list[str]) -> str:
    signature = ", ".join(parameters)
    return f'''"""추가 훈련 문제: {title}."""


def solution({signature}):
    # TODO: 여기에 풀이를 작성하세요.
    pass


# LOCAL_TEST_RUNNER: 이 아래는 제출하지 않습니다.
if __name__ == "__main__":
    import sys as _sys
    from pathlib import Path as _Path

    _source = _Path(__file__).resolve()
    _workspace_root = next(parent for parent in _source.parents if (parent / "tools").is_dir())
    if str(_workspace_root) not in _sys.path:
        _sys.path.insert(0, str(_workspace_root))
    from tools.direct_runner import run_local_tests as _run_local_tests

    raise SystemExit(_run_local_tests(solution, _source.with_name("tests.json")))
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="추가 오프라인 문제 폴더 생성")
    parser.add_argument("spec", type=Path, help="templates/new_problem_spec.json 형식의 파일")
    args = parser.parse_args()
    try:
        data = load_spec(args.spec)
        lesson_id = int(data["lesson_id"])
        if any(problem_id(directory) == lesson_id for directory in discover()):
            raise ValueError(f"이미 존재하는 문제 번호입니다: {lesson_id}")

        category = str(data["category"])
        category_dir = ROOT / "extra_problems" / category
        existing_orders = []
        if category_dir.is_dir():
            for directory in category_dir.iterdir():
                if directory.is_dir():
                    try:
                        existing_orders.append(parse_problem_directory(directory)[0])
                    except ValueError:
                        continue
        order = max(existing_orders, default=0) + 1
        directory = category_dir / f"{order:02d}_{lesson_id}_{safe_title(str(data['title']))}"
        if directory.exists():
            raise ValueError(f"대상 폴더가 이미 있습니다: {directory}")
        directory.mkdir(parents=True)

        parameters = list(data["parameters"])
        signature = ", ".join(parameters)
        constraints = "\n".join(f"- {item}" for item in data["constraints"])
        source = str(data["source_url"]).strip() or "사용자가 로컬 명세에 기록하지 않음"
        examples = render_examples(data["public_examples"], parameters)
        problem = f"""# {data['title']} — 오프라인 추가 문제 명세

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 난이도 | Level {data['level']} |
| 학습 유형 | {category} |
| 호출 함수 | `solution({signature})` |

## 문제

{data['description']}

## 함수 인터페이스

```python
def solution({signature}):
    ...
```

## 규칙과 제한사항

{constraints}

## 공개 예제

{examples}

## 출처

- 원문 확인용: {source}
"""
        readme = f"""# {data['title']}

- 난이도: Level {data['level']}
- 유형: {category}
- 출처: 사용자가 추가한 오프라인 훈련 문제

`PROBLEM.md`를 읽고 `solution.py`를 완성한 뒤 파일을 직접 실행하세요.
"""
        hints = """# 단계별 힌트 기록

처음에는 비워 두고, 복기할 때 아래 질문에 자신의 말로 답하세요.

1. 제한에서 허용되는 목표 복잡도는 무엇인가?
2. 가장 단순한 정답 모델은 무엇인가?
3. 유지해야 할 상태와 핵심 불변식은 무엇인가?
4. 구현 순서를 3~5줄 의사코드로 어떻게 적는가?
"""
        files = {
            "README.md": readme,
            "PROBLEM.md": problem,
            "HINTS.md": hints,
            "solution.py": solution_source(str(data["title"]), parameters),
            "tests.json": json.dumps(data["public_examples"], ensure_ascii=False, indent=2) + "\n",
            "edge_tests.json": json.dumps(data["edge_tests"], ensure_ascii=False, indent=2) + "\n",
        }
        for name, content in files.items():
            (directory / name).write_text(content, encoding="utf-8")
        # 생성 직후 Python 시그니처 문법까지 확인한다.
        ast.parse((directory / "solution.py").read_text(encoding="utf-8"))
        print(f"추가 문제 생성 완료: {directory.relative_to(ROOT)}")
        print(f"실행: python3 tools/judge.py {lesson_id}")
        return 0
    except (OSError, json.JSONDecodeError, SyntaxError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
