"""학습 순서 접두사가 붙은 문제 폴더 이름을 일관되게 다룬다."""

from __future__ import annotations

import re
from pathlib import Path


LEARNING_ORDERS: dict[str, tuple[int, ...]] = {
    "01_해시": (1845, 42576, 178871, 42577, 42578, 42579),
    "02_스택_큐": (12906, 12909, 133502, 42586, 42587, 42583, 42584),
    "03_힙": (138477, 42626, 42627, 42628),
    "04_정렬": (12915, 42748, 42747, 42746),
    "05_완전탐색": (131705, 42840, 86491, 42842, 42839, 87946, 86971, 84512),
    "06_탐욕법": (135808, 42862, 42885, 42884, 42883, 42860, 42861),
    "07_동적계획법": (340198, 43105, 42898, 42895, 1843, 42897),
    "08_DFS_BFS": (172928, 43165, 1844, 43162, 43163, 87694, 43164, 84021),
    "09_이분탐색": (12982, 43238, 43236),
    "10_그래프": (67256, 49189, 49191, 49190),
}


PROBLEM_DIRECTORY_PATTERN = re.compile(
    r"^(?P<order>\d{2})_(?P<lesson_id>\d+)_(?P<title>.+)$"
)


def parse_problem_directory(path_or_name: str | Path) -> tuple[int, int, str]:
    """``01_42576_제목``에서 학습 순서, 문제 번호와 제목을 꺼낸다."""
    name = Path(path_or_name).name
    match = PROBLEM_DIRECTORY_PATTERN.fullmatch(name)
    if not match:
        raise ValueError(
            f"문제 폴더는 '학습순서_문제번호_제목' 형식이어야 합니다: {name}"
        )
    return (
        int(match.group("order")),
        int(match.group("lesson_id")),
        match.group("title"),
    )


def problem_id(path_or_name: str | Path) -> int:
    return parse_problem_directory(path_or_name)[1]


def learning_order(category: str | Path, lesson_id: int) -> int:
    category_name = Path(category).name
    try:
        return LEARNING_ORDERS[category_name].index(lesson_id) + 1
    except KeyError as error:
        raise ValueError(f"등록되지 않은 유형입니다: {category_name}") from error
    except ValueError as error:
        raise ValueError(
            f"{category_name}에 등록되지 않은 문제 번호입니다: {lesson_id}"
        ) from error


def ordered_directory_name(category: str | Path, lesson_id: int, title: str) -> str:
    return f"{learning_order(category, lesson_id):02d}_{lesson_id}_{title}"
