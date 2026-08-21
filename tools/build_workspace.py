#!/usr/bin/env python3
"""공식 페이지의 공개 예제를 내려받아 로컬 연습 폴더를 만든다.

최초 구성과 공식 예제 갱신에만 네트워크가 필요하다. 생성된 채점 환경은
오프라인에서 동작한다.
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    from .problem_paths import learning_order, ordered_directory_name
except ImportError:
    from problem_paths import learning_order, ordered_directory_name


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://school.programmers.co.kr/learn/courses/30/lessons"
USER_AGENT = "Mozilla/5.0 (compatible; local-programmers-kit-builder/1.0)"


@dataclass(frozen=True)
class Problem:
    lesson_id: int
    title: str
    level: int
    added: bool = False
    reason: str = ""


@dataclass(frozen=True)
class Category:
    directory: str
    title: str
    english: str
    part_id: int
    description: str
    problems: tuple[Problem, ...]


CATEGORIES = (
    Category(
        "01_해시",
        "해시",
        "Hash",
        12077,
        "키-값 매핑으로 탐색과 빈도 계산을 빠르게 처리합니다.",
        (
            Problem(42576, "완주하지 못한 선수", 1),
            Problem(1845, "폰켓몬", 1),
            Problem(42577, "전화번호 목록", 2),
            Problem(42578, "의상", 2),
            Problem(42579, "베스트앨범", 3),
            Problem(
                178871,
                "달리기 경주",
                1,
                True,
                "이름→순위와 순위→이름 매핑을 함께 갱신하는 해시 연습 문제입니다.",
            ),
        ),
    ),
    Category(
        "02_스택_큐",
        "스택/큐",
        "Stack / Queue",
        12081,
        "LIFO/FIFO 규칙과 순차 처리 상태를 연습합니다.",
        (
            Problem(12906, "같은 숫자는 싫어", 1),
            Problem(42586, "기능개발", 2),
            Problem(12909, "올바른 괄호", 2),
            Problem(42587, "프로세스", 2),
            Problem(42583, "다리를 지나는 트럭", 2),
            Problem(42584, "주식가격", 2),
            Problem(
                133502,
                "햄버거 만들기",
                1,
                True,
                "최근 재료부터 패턴을 확인하고 제거하는 전형적인 스택 연습 문제입니다.",
            ),
        ),
    ),
    Category(
        "03_힙",
        "힙(Heap)",
        "Heap",
        12117,
        "우선순위 큐로 최솟값/최댓값을 효율적으로 유지합니다.",
        (
            Problem(42626, "더 맵게", 2),
            Problem(42627, "디스크 컨트롤러", 3),
            Problem(42628, "이중우선순위큐", 3),
            Problem(
                138477,
                "명예의 전당 (1)",
                1,
                True,
                "상위 k개 중 최솟값을 계속 유지하는 최소 힙 입문 문제입니다.",
            ),
        ),
    ),
    Category(
        "04_정렬",
        "정렬",
        "Sort",
        12198,
        "정렬 기준을 설계하고 정렬된 결과를 활용합니다.",
        (
            Problem(42748, "K번째수", 1),
            Problem(42746, "가장 큰 수", 2),
            Problem(42747, "H-Index", 2),
            Problem(
                12915,
                "문자열 내 마음대로 정렬하기",
                1,
                True,
                "복합 정렬 키를 직접 설계하는 Level 1 연습 문제입니다.",
            ),
        ),
    ),
    Category(
        "05_완전탐색",
        "완전탐색",
        "Brute Force",
        12230,
        "가능한 후보를 빠짐없이 생성하고 조건에 맞는 답을 찾습니다.",
        (
            Problem(86491, "최소직사각형", 1),
            Problem(42840, "모의고사", 1),
            Problem(42839, "소수 찾기", 2),
            Problem(42842, "카펫", 2),
            Problem(87946, "피로도", 2),
            Problem(86971, "전력망을 둘로 나누기", 2),
            Problem(84512, "모음사전", 2),
            Problem(
                131705,
                "삼총사",
                1,
                True,
                "모든 3명 조합을 조사하는 작은 완전탐색 문제입니다.",
            ),
        ),
    ),
    Category(
        "06_탐욕법",
        "탐욕법(Greedy)",
        "Greedy",
        12244,
        "매 단계의 선택이 전체 최적해로 이어지는 조건을 찾습니다.",
        (
            Problem(42862, "체육복", 1),
            Problem(42860, "조이스틱", 2),
            Problem(42883, "큰 수 만들기", 2),
            Problem(42885, "구명보트", 2),
            Problem(42861, "섬 연결하기", 3),
            Problem(42884, "단속카메라", 3),
            Problem(
                135808,
                "과일 장수",
                1,
                True,
                "가치가 큰 사과부터 묶는 지역 최적 선택을 연습합니다.",
            ),
        ),
    ),
    Category(
        "07_동적계획법",
        "동적계획법(Dynamic Programming)",
        "Dynamic Programming",
        12263,
        "작은 부분 문제의 답을 저장해 더 큰 문제의 답을 만듭니다.",
        (
            Problem(42895, "N으로 표현", 3),
            Problem(43105, "정수 삼각형", 3),
            Problem(42898, "등굣길", 3),
            Problem(1843, "사칙연산", 4),
            Problem(42897, "도둑질", 4),
            Problem(
                340198,
                "[PCCE 기출문제] 10번 / 공원",
                1,
                True,
                "빈칸 최대 정사각형을 2차원 DP로도 찾을 수 있어 재분류했습니다. "
                "다만 원래 제한에서는 돗자리 크기를 직접 검사하는 구현이 더 자연스러우므로 "
                "DP 대표 문제로 오해하지 말고 정수 삼각형부터 핵심 DP를 익히세요.",
            ),
        ),
    ),
    Category(
        "08_DFS_BFS",
        "깊이/너비 우선 탐색(DFS/BFS)",
        "DFS / BFS",
        12421,
        "그래프나 격자를 깊이 또는 너비 순서로 탐색합니다.",
        (
            Problem(43165, "타겟 넘버", 2),
            Problem(43162, "네트워크", 3),
            Problem(1844, "게임 맵 최단거리", 2),
            Problem(43163, "단어 변환", 3),
            Problem(87694, "아이템 줍기", 3),
            Problem(43164, "여행경로", 3),
            Problem(84021, "퍼즐 조각 채우기", 3),
            Problem(
                172928,
                "공원 산책",
                1,
                True,
                "격자 경계와 장애물을 다루는 입문용 재분류입니다. 실제 핵심은 DFS/BFS가 "
                "아니라 명령 시뮬레이션이므로 게임 맵 최단거리부터 탐색의 대표 신호를 익히세요.",
            ),
        ),
    ),
    Category(
        "09_이분탐색",
        "이분탐색",
        "Binary Search",
        12486,
        "단조성을 이용해 답이 존재하는 범위를 절반씩 줄입니다.",
        (
            Problem(43238, "입국심사", 3),
            Problem(43236, "징검다리", 4),
            Problem(
                12982,
                "예산",
                1,
                True,
                "누적합에서 가능한 최대 개수를 이분탐색할 수도 있어 재분류했습니다. 자연스러운 "
                "첫 풀이는 정렬+그리디이므로 입국심사부터 매개변수 이분탐색의 핵심을 익히세요.",
            ),
        ),
    ),
    Category(
        "10_그래프",
        "그래프",
        "Graph",
        14393,
        "정점과 간선의 관계를 모델링해 경로와 연결 관계를 구합니다.",
        (
            Problem(49189, "가장 먼 노드", 3),
            Problem(49191, "순위", 3),
            Problem(49190, "방의 개수", 5),
            Problem(
                67256,
                "키패드 누르기",
                1,
                True,
                "키패드를 작은 격자 그래프로 볼 수 있어 재분류했습니다. 실제 핵심은 좌표 거리와 "
                "상태 시뮬레이션이므로 가장 먼 노드부터 그래프 탐색의 대표 신호를 익히세요.",
            ),
        ),
    ),
)


class ExampleTableParser(HTMLParser):
    """문제 설명 영역의 HTML 표를 셀 단위 문자열로 변환한다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"th", "td"} and self._row is not None:
            self._cell = []
        elif tag == "br" and self._cell is not None:
            self._cell.append(" ")

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"th", "td"} and self._cell is not None and self._row is not None:
            value = "".join(self._cell).strip()
            self._row.append(re.sub(r"\s+", " ", value))
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table is not None:
            if self._row:
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            if self._table:
                self.tables.append(self._table)
            self._table = None


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def parse_value(raw: str) -> Any:
    value = raw.strip()
    value = re.sub(r"\btrue\b", "True", value, flags=re.IGNORECASE)
    value = re.sub(r"\bfalse\b", "False", value, flags=re.IGNORECASE)
    value = re.sub(r"\bnull\b", "None", value, flags=re.IGNORECASE)
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        # 공식 표의 문자열은 대개 따옴표가 있지만, 예외도 로컬 문자열로 보존한다.
        return raw.strip()


def parse_page(source: str) -> tuple[str, int, list[str], list[dict[str, Any]]]:
    decoded = html.unescape(source)
    metadata = re.search(
        r'"challenge_title":"(?P<title>.*?)","challenge_level":(?P<level>\d+)',
        decoded,
    )
    if not metadata:
        raise ValueError("문제 제목/레벨 메타데이터를 찾지 못했습니다.")

    signature = re.search(r"def\s+solution\((?P<args>[^)]*)\)\s*:", decoded)
    if not signature:
        raise ValueError("Python solution 함수 시그니처를 찾지 못했습니다.")
    parameters = [part.strip() for part in signature.group("args").split(",") if part.strip()]

    parser = ExampleTableParser()
    parser.feed(source)
    example_table = None
    for table in parser.tables:
        if table and table[0] and table[0][-1].lower() in {
            "return",
            "result",
            "answer",
        }:
            example_table = table
            break
    if example_table is None:
        raise ValueError("입출력 예 표를 찾지 못했습니다.")

    headers = example_table[0]
    input_headers = headers[:-1]
    if len(input_headers) != len(parameters):
        raise ValueError(
            f"표 인자({input_headers})와 함수 인자({parameters}) 개수가 다릅니다."
        )

    cases = []
    for index, row in enumerate(example_table[1:], start=1):
        if len(row) != len(headers):
            raise ValueError(f"공개 예제 {index}의 열 개수가 올바르지 않습니다: {row}")
        cases.append(
            {
                "name": f"공개 예제 {index}",
                "args": [parse_value(cell) for cell in row[:-1]],
                "expected": parse_value(row[-1]),
            }
        )
    return metadata.group("title"), int(metadata.group("level")), parameters, cases


def safe_name(title: str) -> str:
    value = re.sub(r'[<>:"/\\|?*]+', "_", title)
    value = re.sub(r"\s+", "_", value.strip())
    return re.sub(r"_+", "_", value).strip("_")


def problem_readme(
    category: Category,
    problem: Problem,
    parameters: list[str],
    case_count: int,
) -> str:
    label = "추가 Level 1" if problem.added else "고득점 Kit"
    classification = (
        f"\n## 이 유형에 넣은 이유\n\n{problem.reason}\n"
        if problem.added
        else ""
    )
    parameter_text = ", ".join(f"`{name}`" for name in parameters)
    directory_name = ordered_directory_name(
        category.directory, problem.lesson_id, safe_name(problem.title)
    )
    command_path = f"{category.directory}/{directory_name}"
    return f"""# {problem.title}

- 구분: {label}
- 난이도: Level {problem.level}
- 유형: {category.title}
- 오프라인 문제 명세: [PROBLEM.md](./PROBLEM.md)
- 주석 포함 예시 풀이: [solutions/README.md](./solutions/README.md)
- 공식 문제: <{BASE_URL}/{problem.lesson_id}>
- 함수: `solution({", ".join(parameters)})`
- 포함된 테스트: 공식 공개 예제 {case_count}개 + 자체 경계 사례 2개
{classification}
## 풀이 방법

1. 이 폴더의 `PROBLEM.md`에서 문제 규칙, 제한사항, 예제를 읽습니다.
2. `solution.py`의 `solution()` 함수를 구현합니다.
3. 저장한 뒤 저장소 루트에서 아래 명령을 실행합니다.
4. 통과 후 `solutions/README.md`와 두 예시 답안을 비교하며 복기합니다.

```bash
python3 tools/judge.py "{command_path}"
```

채점기는 {parameter_text} 순서로 함수를 호출합니다. `tests.json`은 공개 예제,
`edge_tests.json`은 자체 경계 사례입니다. 제출 전에는 자신이 찾은 반례도
`edge_tests.json`에 더 추가하세요.

## `solution.py` 직접 디버깅

아래처럼 파일을 직접 실행하면 두 테스트 파일의 모든 입력, 기대값, 실제 반환값,
실행 시간과 예외 traceback이 출력됩니다.

```bash
python3 "{command_path}/solution.py"
```
"""


def category_readme(category: Category) -> str:
    rows = []
    for problem in sorted(
        category.problems,
        key=lambda item: learning_order(category.directory, item.lesson_id),
    ):
        kind = "추가 Level 1" if problem.added else "Kit"
        directory = ordered_directory_name(
            category.directory, problem.lesson_id, safe_name(problem.title)
        )
        display_title = problem.title.replace("[", r"\[").replace("]", r"\]")
        rows.append(
            f"| [{display_title}](<./{directory}/>) | {problem.level} | {kind} |"
        )
    heading = category.title if "(" in category.title else f"{category.title} ({category.english})"
    return f"""# {heading}

{category.description}

- 유형 학습법: [MASTERY_GUIDE.md](./MASTERY_GUIDE.md)
- 프로그래머스 공식 Kit 유형: <https://school.programmers.co.kr/learn/courses/30/parts/{category.part_id}>

| 문제 | Level | 구분 |
|---|---:|---|
{chr(10).join(rows)}
"""


def write_problem(
    category: Category,
    problem: Problem,
    parameters: list[str],
    cases: list[dict[str, Any]],
) -> None:
    directory = ROOT / category.directory / ordered_directory_name(
        category.directory, problem.lesson_id, safe_name(problem.title)
    )
    directory.mkdir(parents=True, exist_ok=True)
    signature = ", ".join(parameters)
    solution = f'''"""프로그래머스 {problem.title} 풀이."""


def solution({signature}):
    # TODO: 여기에 풀이를 작성하세요.
    pass


# LOCAL_TEST_RUNNER: 이 아래는 로컬 실행용이며 solution 함수 제출 코드와 분리되어 있습니다.
if __name__ == "__main__":
    import sys as _sys
    from pathlib import Path as _Path

    _tests_path = _Path(__file__).with_name("tests.json")
    if _tests_path.is_file():
        _workspace_root = _Path(__file__).resolve().parents[2]
        if str(_workspace_root) not in _sys.path:
            _sys.path.insert(0, str(_workspace_root))
        from tools.direct_runner import run_local_tests as _run_local_tests

        raise SystemExit(_run_local_tests(solution, _tests_path))
'''
    solution_path = directory / "solution.py"
    if not solution_path.exists():
        solution_path.write_text(solution, encoding="utf-8")
    (directory / "tests.json").write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (directory / "README.md").write_text(
        problem_readme(category, problem, parameters, len(cases)),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="공식 페이지에서 공개 예제를 명시적으로 갱신합니다."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--refresh-public-examples",
        action="store_true",
        help="네트워크를 사용해 tests.json과 생성 문서를 갱신",
    )
    mode.add_argument(
        "--refresh-navigation",
        action="store_true",
        help="네트워크 없이 유형 README의 추천 순서 링크만 갱신",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="갱신 전 확인 질문을 생략",
    )
    args = parser.parse_args(argv)
    if args.refresh_navigation:
        for category in CATEGORIES:
            (ROOT / category.directory / "README.md").write_text(
                category_readme(category), encoding="utf-8"
            )
        print(f"유형 탐색 문서 갱신 완료: {len(CATEGORIES)}개")
        return 0
    if not args.refresh_public_examples:
        print(
            "기본 실행은 네트워크에 접속하거나 파일을 바꾸지 않습니다.\n"
            "유형 링크는 --refresh-navigation, 공개 예제는 "
            "--refresh-public-examples로 갱신하세요."
        )
        return 0
    if not args.yes:
        if not sys.stdin.isatty():
            print("비대화형 환경에서는 --yes도 함께 지정해야 합니다.", file=sys.stderr)
            return 2
        answer = input(
            "tests.json, 문제 README와 PROBLEM.md를 공식 공개 정보로 갱신합니다. "
            "계속할까요? [y/N] "
        )
        if answer.strip().lower() not in {"y", "yes"}:
            print("갱신을 취소했습니다.")
            return 0

    total = sum(len(category.problems) for category in CATEGORIES)
    completed = 0
    errors: list[str] = []

    for category in CATEGORIES:
        (ROOT / category.directory).mkdir(parents=True, exist_ok=True)
        (ROOT / category.directory / "README.md").write_text(
            category_readme(category), encoding="utf-8"
        )
        for problem in category.problems:
            url = f"{BASE_URL}/{problem.lesson_id}?language=python3"
            try:
                title, level, parameters, cases = parse_page(fetch(url))
                if title != problem.title:
                    raise ValueError(f"제목 불일치: 기대={problem.title!r}, 실제={title!r}")
                if level != problem.level:
                    raise ValueError(
                        f"난이도 불일치: 기대=Level {problem.level}, 실제=Level {level}"
                    )
                if not cases:
                    raise ValueError("공개 예제가 없습니다.")
                write_problem(category, problem, parameters, cases)
                completed += 1
                print(f"[{completed:02d}/{total}] {category.title} / {problem.title}")
            except (OSError, ValueError, urllib.error.URLError) as error:
                errors.append(f"{problem.lesson_id} {problem.title}: {error}")

    if errors:
        print("\n생성 실패:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    from offline_specs import main as build_offline_specs

    build_offline_specs()
    print(f"\n총 {completed}개 문제 구성을 완료했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
