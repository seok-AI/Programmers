#!/usr/bin/env python3
"""최대·적대 입력으로 예시 풀이의 시간복잡도 퇴행을 검사한다.

공개 예제와 경계 테스트는 작은 입력의 정확성을, 이 도구는 입력 크기에 따른
실행 가능성을 검사한다. 측정값은 기기마다 다르므로 절대 속도 비교가 아니라
제한 시간 안에 끝나는지만 판정한다.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import signal
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

try:
    from .problem_paths import problem_id
except ImportError:
    from problem_paths import problem_id


ROOT = Path(__file__).resolve().parents[1]


class StressTimeout(TimeoutError):
    pass


def timeout_handler(signum: int, frame: object) -> None:
    del signum, frame
    raise StressTimeout


@dataclass(frozen=True)
class StressCase:
    lesson_id: int
    name: str
    arguments: Callable[[], list[object]]
    validate: Callable[[object], bool]


PRICE_COUNT = 100_000
NUMBER_LENGTH = 1_000_000
OPERATION_COUNT = 100_000
MAX_LIST_LENGTH = 1_000_000
MAX_SORT_LENGTH = 100_000
MAX_ROCKS = 50_000
MAX_NODES = 20_000
MAX_EXAMINERS = 100_000
MAX_PHONE_NUMBERS = 1_000_000
MAX_TRIANGLE_HEIGHT = 500
MAX_TICKETS = 10_000


def ranking_arguments() -> list[object]:
    players = [f"p{index:05d}" for index in range(50_000)]
    # 매 호출 시 2등인 두 선수가 번갈아 1등이 된다. 따라서 100만 호출 모두 명세 안이다.
    callings = [players[1], players[0]] * 500_000
    return [players, callings]


def stepping_stones_arguments() -> list[object]:
    unit = 10_000
    rocks = [unit * index for index in range(1, MAX_ROCKS + 1)]
    # 50,002개의 단위 구간에서 25,000개 바위를 없애면 최소 간격 2*unit이 가능하다.
    return [unit * (MAX_ROCKS + 2), rocks, MAX_ROCKS // 2]


def triangle_arguments() -> list[object]:
    return [[[1] * width for width in range(1, MAX_TRIANGLE_HEIGHT + 1)]]


def itinerary_arguments() -> list[object]:
    route = ["ICN" if index % 2 == 0 else "AAA" for index in range(MAX_TICKETS + 1)]
    tickets = [[left, right] for left, right in zip(route, route[1:])]
    return [tickets]


CASES = (
    StressCase(
        42576,
        "참가자 10만 명·동명이인 사이 마지막 미완주자",
        lambda: [["same"] * 99_999 + ["missing"], ["same"] * 99_999],
        lambda result: result == "missing",
    ),
    StressCase(
        42577,
        "전화번호 100만 개·모두 같은 길이",
        lambda: [[f"{value:07d}" for value in range(MAX_PHONE_NUMBERS)]],
        lambda result: result is True,
    ),
    StressCase(
        12906,
        "최대 길이·모든 값이 같은 배열",
        lambda: [[1] * MAX_LIST_LENGTH],
        lambda result: result == [1],
    ),
    StressCase(
        12909,
        "괄호 문자열 최대 길이·깊게 중첩된 유효 입력",
        lambda: ["(" * 50_000 + ")" * 50_000],
        lambda result: result is True,
    ),
    StressCase(
        133502,
        "최대 길이·햄버거 패턴 연속 완성",
        lambda: [[1, 2, 3, 1] * (MAX_LIST_LENGTH // 4)],
        lambda result: result == MAX_LIST_LENGTH // 4,
    ),
    StressCase(
        178871,
        "선수 5만 명·유효한 호출 100만 번",
        ranking_arguments,
        lambda result: isinstance(result, list)
        and len(result) == 50_000
        and result[0] == "p00000"
        and result[1] == "p00001",
    ),
    StressCase(
        42579,
        "곡 1만 개·한 장르의 전곡 재생 수 동률",
        lambda: [["genre"] * 10_000, [1] * 10_000],
        lambda result: result == [0, 1],
    ),
    StressCase(
        42583,
        "트럭 1만 대·다리 길이 1만",
        lambda: [10_000, 10_000, [1] * 10_000],
        lambda result: result == 20_000,
    ),
    StressCase(
        42584,
        "최대 길이·전부 동일한 가격",
        lambda: [[1] * PRICE_COUNT],
        lambda result: isinstance(result, list)
        and len(result) == PRICE_COUNT
        and all(value == PRICE_COUNT - index - 1 for index, value in enumerate(result)),
    ),
    StressCase(
        42626,
        "음식 100만 개·끝까지 혼합해도 실패하는 적대 입력",
        lambda: [[0] * MAX_LIST_LENGTH, 1],
        lambda result: result == -1,
    ),
    StressCase(
        42883,
        "최대 길이·전부 같은 숫자에서 절반 제거",
        lambda: ["1" * NUMBER_LENGTH, NUMBER_LENGTH // 2],
        lambda result: result == "1" * (NUMBER_LENGTH // 2),
    ),
    StressCase(
        42746,
        "정렬 원소 10만 개·최대 네 자리 문자열",
        lambda: [[1000] * MAX_SORT_LENGTH],
        lambda result: result == "1000" * MAX_SORT_LENGTH,
    ),
    StressCase(
        42897,
        "원형 집 100만 채·모든 금액 동일",
        lambda: [[1] * MAX_LIST_LENGTH],
        lambda result: result == MAX_LIST_LENGTH // 2,
    ),
    StressCase(
        135808,
        "사과 100만 개·모든 상자가 최고 등급",
        lambda: [9, 10, [9] * MAX_LIST_LENGTH],
        lambda result: result == 9_000_000,
    ),
    StressCase(
        42885,
        "구명보트 5만 명·모두 두 명씩 탑승",
        lambda: [[40] * 50_000, 80],
        lambda result: result == 25_000,
    ),
    StressCase(
        43105,
        "높이 500 삼각형·모든 경로 합 동일",
        triangle_arguments,
        lambda result: result == MAX_TRIANGLE_HEIGHT,
    ),
    StressCase(
        43164,
        "항공권 1만 장·두 공항 왕복 오일러 경로",
        itinerary_arguments,
        lambda result: isinstance(result, list)
        and len(result) == MAX_TICKETS + 1
        and all(code == ("ICN" if index % 2 == 0 else "AAA") for index, code in enumerate(result)),
    ),
    StressCase(
        42628,
        "정렬 리스트의 앞 삽입을 유발하는 역순 명령",
        lambda: [[f"I {value}" for value in range(OPERATION_COUNT, 0, -1)]],
        lambda result: result == [OPERATION_COUNT, 1],
    ),
    StressCase(
        49190,
        "화살표 10만 개·한 방향 직선 이동",
        lambda: [[0] * 100_000],
        lambda result: result == 0,
    ),
    StressCase(
        43236,
        "바위 5만 개·거리 상한에 가까운 매개변수 탐색",
        stepping_stones_arguments,
        lambda result: result == 20_000,
    ),
    StressCase(
        43238,
        "심사관 10만 명·대기 인원 10억 명",
        lambda: [1_000_000_000, [1] * MAX_EXAMINERS],
        lambda result: result == 10_000,
    ),
    StressCase(
        49189,
        "노드 2만 개가 1번에 연결된 별 그래프",
        lambda: [MAX_NODES, [[1, node] for node in range(2, MAX_NODES + 1)]],
        lambda result: result == MAX_NODES - 1,
    ),
)


def load_solution(lesson_id: int, variant: str):
    matches = [
        source
        for source in ROOT.glob(f"[0-9][0-9]_*/**/solutions/{variant}.py")
        if problem_id(source.parents[1]) == lesson_id
    ]
    if len(matches) != 1:
        raise ValueError(f"{lesson_id}/{variant} 풀이 파일을 하나로 찾지 못했습니다.")
    source = matches[0]
    module_name = "stress_" + hashlib.sha1(str(source).encode()).hexdigest()
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise ImportError(source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


def run_case(case: StressCase, variant: str, timeout: float) -> bool:
    solution = load_solution(case.lesson_id, variant)
    arguments = case.arguments()
    started = time.perf_counter()
    try:
        signal.setitimer(signal.ITIMER_REAL, timeout)
        result = solution(*arguments)
    except StressTimeout:
        print(f"FAIL {case.lesson_id}/{variant}: {timeout:g}초 시간 초과 - {case.name}")
        return False
    except Exception as error:
        print(f"FAIL {case.lesson_id}/{variant}: {type(error).__name__}: {error}")
        return False
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    elapsed = time.perf_counter() - started
    if not case.validate(result):
        print(f"FAIL {case.lesson_id}/{variant}: 결과 검증 실패 - {case.name}")
        return False
    print(f"PASS {case.lesson_id}/{variant}: {elapsed:.3f}초 - {case.name}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="예시 풀이 최대·적대 입력 검사")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("problem", nargs="?", type=int, help="문제 번호")
    target.add_argument("--all", action="store_true", help="등록된 스트레스 테스트 전체")
    parser.add_argument("--timeout", type=float, default=3.0, help="풀이별 제한 시간")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout은 0보다 커야 합니다.")

    selected = list(CASES) if args.all else [case for case in CASES if case.lesson_id == args.problem]
    if not selected:
        parser.error(f"등록된 스트레스 테스트가 없습니다: {args.problem}")

    previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
    passed = failed = 0
    try:
        for case in selected:
            for variant in ("recommended", "alternative"):
                if run_case(case, variant, args.timeout):
                    passed += 1
                else:
                    failed += 1
    finally:
        signal.signal(signal.SIGALRM, previous_handler)
    print(f"스트레스 검증: {passed}개 통과 / {failed}개 실패")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
