#!/usr/bin/env python3
"""57개 문제의 제한사항 안에서 작은 결정적 랜덤 입력을 생성한다.

작은 입력을 쓰는 이유는 권장·대안 풀이를 수백 번 교차 실행하면서도 빠르게
검증하기 위해서다. 최대 크기 성능은 ``stress.py``가 별도로 담당한다.
"""

from __future__ import annotations

import random
import string
from typing import Callable


Generator = Callable[[random.Random], list[object]]


def alpha_name(index: int) -> str:
    """길이 3~5의 서로 다른 소문자 이름을 만든다."""
    letters = []
    value = index
    for _ in range(3):
        letters.append(chr(ord("a") + value % 26))
        value //= 26
    return "".join(reversed(letters))


def random_word(rng: random.Random, length: int) -> str:
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(length))


def unique_words(rng: random.Random, count: int, length: int) -> list[str]:
    words: set[str] = set()
    while len(words) < count:
        words.add(random_word(rng, length))
    return sorted(words)


def g1845(rng: random.Random) -> list[object]:
    size = 2 * rng.randint(1, 10)
    return [[rng.randint(1, 8) for _ in range(size)]]


def g42576(rng: random.Random) -> list[object]:
    participant = [alpha_name(rng.randrange(6)) for _ in range(rng.randint(1, 20))]
    missing = rng.randrange(len(participant))
    completion = participant[:missing] + participant[missing + 1 :]
    rng.shuffle(completion)
    return [participant, completion]


def g178871(rng: random.Random) -> list[object]:
    players = [alpha_name(index) for index in range(rng.randint(5, 15))]
    ranking = players.copy()
    callings = []
    for _ in range(rng.randint(2, 30)):
        index = rng.randrange(1, len(ranking))
        callings.append(ranking[index])
        ranking[index - 1], ranking[index] = ranking[index], ranking[index - 1]
    return [players, callings]


def g42577(rng: random.Random) -> list[object]:
    count = rng.randint(2, 15)
    numbers: set[str] = set()
    while len(numbers) < count:
        length = rng.randint(1, 8)
        numbers.add("".join(rng.choice(string.digits) for _ in range(length)))
    phone_book = sorted(numbers)
    if rng.random() < 0.5:
        base = rng.choice(phone_book)
        if len(base) < 8:
            candidate = base + rng.choice(string.digits)
            if candidate not in numbers:
                phone_book[rng.randrange(len(phone_book))] = candidate
                if base not in phone_book:
                    phone_book[0] = base
    rng.shuffle(phone_book)
    return [phone_book]


def g42578(rng: random.Random) -> list[object]:
    clothes = []
    for index in range(rng.randint(1, 20)):
        clothes.append([f"item_{alpha_name(index)}", f"kind_{chr(ord('a') + rng.randrange(5))}"])
    return [clothes]


def g42579(rng: random.Random) -> list[object]:
    while True:
        genres = [f"g{rng.randrange(1, 5)}" for _ in range(rng.randint(1, 20))]
        plays = [rng.randint(1, 500) for _ in genres]
        totals: dict[str, int] = {}
        for genre, play in zip(genres, plays):
            totals[genre] = totals.get(genre, 0) + play
        if len(set(totals.values())) == len(totals):
            return [genres, plays]


def g12906(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 9) for _ in range(rng.randint(1, 50))]]


def g12909(rng: random.Random) -> list[object]:
    return ["".join(rng.choice("()") for _ in range(rng.randint(1, 40)))]


def g133502(rng: random.Random) -> list[object]:
    return [[rng.randint(1, 3) for _ in range(rng.randint(1, 80))]]


def g42586(rng: random.Random) -> list[object]:
    size = rng.randint(1, 15)
    return [
        [rng.randint(1, 99) for _ in range(size)],
        [rng.randint(1, 100) for _ in range(size)],
    ]


def g42587(rng: random.Random) -> list[object]:
    priorities = [rng.randint(1, 9) for _ in range(rng.randint(1, 15))]
    return [priorities, rng.randrange(len(priorities))]


def g42583(rng: random.Random) -> list[object]:
    bridge_length = rng.randint(1, 12)
    weight = rng.randint(1, 30)
    trucks = [rng.randint(1, weight) for _ in range(rng.randint(1, 15))]
    return [bridge_length, weight, trucks]


def g42584(rng: random.Random) -> list[object]:
    return [[rng.randint(1, 20) for _ in range(rng.randint(2, 50))]]


def g138477(rng: random.Random) -> list[object]:
    return [rng.randint(3, 12), [rng.randint(0, 100) for _ in range(rng.randint(7, 30))]]


def g42626(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 30) for _ in range(rng.randint(2, 25))], rng.randint(0, 80)]


def g42627(rng: random.Random) -> list[object]:
    return [[[rng.randint(0, 15), rng.randint(1, 10)] for _ in range(rng.randint(1, 9))]]


def g42628(rng: random.Random) -> list[object]:
    operations = []
    for _ in range(rng.randint(1, 50)):
        if rng.random() < 0.6:
            operations.append(f"I {rng.randint(-50, 50)}")
        else:
            operations.append(f"D {rng.choice((-1, 1))}")
    return [operations]


def g12915(rng: random.Random) -> list[object]:
    length = rng.randint(1, 8)
    strings_ = [random_word(rng, length) for _ in range(rng.randint(1, 15))]
    return [strings_, rng.randrange(length)]


def g42748(rng: random.Random) -> list[object]:
    array = [rng.randint(1, 100) for _ in range(rng.randint(1, 20))]
    commands = []
    for _ in range(rng.randint(1, 10)):
        left = rng.randint(1, len(array))
        right = rng.randint(left, len(array))
        commands.append([left, right, rng.randint(1, right - left + 1)])
    return [array, commands]


def g42747(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 50) for _ in range(rng.randint(1, 30))]]


def g42746(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 1000) for _ in range(rng.randint(1, 20))]]


def g131705(rng: random.Random) -> list[object]:
    return [[rng.randint(-15, 15) for _ in range(rng.randint(3, 12))]]


def g42840(rng: random.Random) -> list[object]:
    return [[rng.randint(1, 5) for _ in range(rng.randint(1, 60))]]


def g86491(rng: random.Random) -> list[object]:
    return [[[rng.randint(1, 100), rng.randint(1, 100)] for _ in range(rng.randint(1, 20))]]


def g42842(rng: random.Random) -> list[object]:
    width = rng.randint(3, 30)
    height = rng.randint(3, width)
    yellow = (width - 2) * (height - 2)
    return [width * height - yellow, yellow]


def g42839(rng: random.Random) -> list[object]:
    return ["".join(rng.choice(string.digits) for _ in range(rng.randint(1, 5)))]


def g87946(rng: random.Random) -> list[object]:
    dungeons = []
    for _ in range(rng.randint(1, 7)):
        required = rng.randint(1, 100)
        dungeons.append([required, rng.randint(1, required)])
    return [rng.randint(1, 100), dungeons]


def random_tree(rng: random.Random, node_count: int, *, one_based: bool) -> list[list[int]]:
    offset = 1 if one_based else 0
    return [
        [node + offset, rng.randrange(node) + offset]
        for node in range(1, node_count)
    ]


def g86971(rng: random.Random) -> list[object]:
    node_count = rng.randint(2, 12)
    wires = [sorted(edge) for edge in random_tree(rng, node_count, one_based=True)]
    rng.shuffle(wires)
    return [node_count, wires]


def g84512(rng: random.Random) -> list[object]:
    return ["".join(rng.choice("AEIOU") for _ in range(rng.randint(1, 5)))]


def g135808(rng: random.Random) -> list[object]:
    k = rng.randint(3, 9)
    return [k, rng.randint(3, 10), [rng.randint(1, k) for _ in range(rng.randint(7, 50))]]


def g42862(rng: random.Random) -> list[object]:
    n = rng.randint(2, 20)
    students = list(range(1, n + 1))
    lost = rng.sample(students, rng.randint(1, n))
    reserve = rng.sample(students, rng.randint(1, n))
    return [n, lost, reserve]


def g42885(rng: random.Random) -> list[object]:
    limit = rng.randint(80, 240)
    people = [rng.randint(40, limit) for _ in range(rng.randint(1, 30))]
    return [people, limit]


def g42884(rng: random.Random) -> list[object]:
    routes = []
    for _ in range(rng.randint(1, 20)):
        start = rng.randint(-100, 99)
        routes.append([start, rng.randint(start, 100)])
    return [routes]


def g42883(rng: random.Random) -> list[object]:
    length = rng.randint(2, 50)
    number = "".join(rng.choice(string.digits) for _ in range(length))
    return [number, rng.randint(1, length - 1)]


def g42860(rng: random.Random) -> list[object]:
    return ["".join(rng.choice(string.ascii_uppercase) for _ in range(rng.randint(1, 15)))]


def g42861(rng: random.Random) -> list[object]:
    n = rng.randint(2, 10)
    pairs = {tuple(sorted(edge)) for edge in random_tree(rng, n, one_based=False)}
    all_pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    rng.shuffle(all_pairs)
    for pair in all_pairs[: rng.randint(0, min(12, len(all_pairs)))]:
        pairs.add(pair)
    costs = [[left, right, rng.randint(1, 100)] for left, right in sorted(pairs)]
    rng.shuffle(costs)
    return [n, costs]


def g340198(rng: random.Random) -> list[object]:
    rows, columns = rng.randint(1, 10), rng.randint(1, 10)
    park = [
        ["-1" if rng.random() < 0.65 else "A" for _ in range(columns)]
        for _ in range(rows)
    ]
    mats = rng.sample(range(1, 11), rng.randint(1, 6))
    return [mats, park]


def g43105(rng: random.Random) -> list[object]:
    triangle = [
        [rng.randint(0, 100) for _ in range(width)]
        for width in range(1, rng.randint(1, 10) + 1)
    ]
    return [triangle]


def g42898(rng: random.Random) -> list[object]:
    while True:
        m, n = rng.randint(1, 10), rng.randint(1, 10)
        if not (m == n == 1):
            break
    candidates = [
        [x, y]
        for x in range(1, m + 1)
        for y in range(1, n + 1)
        if [x, y] not in ([1, 1], [m, n])
    ]
    puddles = rng.sample(candidates, rng.randint(0, min(10, len(candidates))))
    return [m, n, puddles]


def g42895(rng: random.Random) -> list[object]:
    return [rng.randint(1, 9), rng.randint(1, 200)]


def g1843(rng: random.Random) -> list[object]:
    operands = rng.randint(2, 7)
    expression = []
    for index in range(operands):
        expression.append(str(rng.randint(1, 30)))
        if index + 1 < operands:
            expression.append(rng.choice(("+", "-")))
    return [expression]


def g42897(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 1000) for _ in range(rng.randint(3, 40))]]


def g172928(rng: random.Random) -> list[object]:
    rows, columns = rng.randint(3, 10), rng.randint(3, 10)
    start_row, start_column = rng.randrange(rows), rng.randrange(columns)
    park = []
    for row in range(rows):
        line = []
        for column in range(columns):
            if (row, column) == (start_row, start_column):
                line.append("S")
            else:
                line.append("X" if rng.random() < 0.2 else "O")
        park.append("".join(line))
    routes = [
        f"{rng.choice('NSWE')} {rng.randint(1, 9)}"
        for _ in range(rng.randint(1, 20))
    ]
    return [park, routes]


def g43165(rng: random.Random) -> list[object]:
    return [[rng.randint(1, 20) for _ in range(rng.randint(2, 12))], rng.randint(1, 100)]


def g1844(rng: random.Random) -> list[object]:
    while True:
        rows, columns = rng.randint(1, 10), rng.randint(1, 10)
        if not (rows == columns == 1):
            break
    maps = [
        [1 if rng.random() < 0.7 else 0 for _ in range(columns)]
        for _ in range(rows)
    ]
    maps[0][0] = maps[-1][-1] = 1
    return [maps]


def g43162(rng: random.Random) -> list[object]:
    n = rng.randint(1, 12)
    computers = [[0] * n for _ in range(n)]
    for node in range(n):
        computers[node][node] = 1
    for left in range(n):
        for right in range(left + 1, n):
            if rng.random() < 0.3:
                computers[left][right] = computers[right][left] = 1
    return [n, computers]


def g43163(rng: random.Random) -> list[object]:
    length = rng.randint(3, 6)
    begin, target, *words = unique_words(rng, rng.randint(5, 15), length)
    if rng.random() < 0.75:
        words[rng.randrange(len(words))] = target
    return [begin, target, words]


def g87694(rng: random.Random) -> list[object]:
    x1, y1 = rng.randint(1, 30), rng.randint(1, 30)
    x2, y2 = rng.randint(x1 + 1, min(50, x1 + 15)), rng.randint(y1 + 1, min(50, y1 + 15))
    boundary = (
        [(x, y1) for x in range(x1, x2 + 1)]
        + [(x, y2) for x in range(x1, x2 + 1)]
        + [(x1, y) for y in range(y1 + 1, y2)]
        + [(x2, y) for y in range(y1 + 1, y2)]
    )
    character, item = rng.sample(boundary, 2)
    return [[[x1, y1, x2, y2]], character[0], character[1], item[0], item[1]]


def g43164(rng: random.Random) -> list[object]:
    airports = ["ICN", "AAA", "BBB", "CCC", "DDD", "EEE"]
    route = ["ICN"] + [rng.choice(airports) for _ in range(rng.randint(3, 9))]
    tickets = [[left, right] for left, right in zip(route, route[1:])]
    rng.shuffle(tickets)
    return [tickets]


def normalize_shape(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    top = min(row for row, _ in shape)
    left = min(column for _, column in shape)
    return {(row - top, column - left) for row, column in shape}


def connected_shape(rng: random.Random, size: int) -> set[tuple[int, int]]:
    shape = {(0, 0)}
    while len(shape) < size:
        row, column = rng.choice(sorted(shape))
        dr, dc = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        shape.add((row + dr, column + dc))
    return normalize_shape(shape)


def rotate_shape(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return normalize_shape({(column, -row) for row, column in shape})


def g84021(rng: random.Random) -> list[object]:
    size = 8
    hole = connected_shape(rng, rng.randint(1, 6))
    if rng.random() < 0.65:
        piece = set(hole)
        for _ in range(rng.randrange(4)):
            piece = rotate_shape(piece)
    else:
        different_size = rng.choice([value for value in range(1, 7) if value != len(hole)])
        piece = connected_shape(rng, different_size)
    game_board = [[1] * size for _ in range(size)]
    table = [[0] * size for _ in range(size)]
    for row, column in hole:
        game_board[row + 1][column + 1] = 0
    for row, column in piece:
        table[row + 1][column + 1] = 1
    return [game_board, table]


def g12982(rng: random.Random) -> list[object]:
    requests = [rng.randint(1, 100) for _ in range(rng.randint(1, 30))]
    return [requests, rng.randint(1, sum(requests) + 50)]


def g43238(rng: random.Random) -> list[object]:
    return [rng.randint(1, 1000), [rng.randint(1, 50) for _ in range(rng.randint(1, 15))]]


def g43236(rng: random.Random) -> list[object]:
    distance = rng.randint(2, 200)
    count = rng.randint(1, min(20, distance - 1))
    rocks = rng.sample(range(1, distance), count)
    return [distance, rocks, rng.randint(1, count)]


def g67256(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 9) for _ in range(rng.randint(1, 50))], rng.choice(("left", "right"))]


def connected_graph(rng: random.Random, node_count: int) -> list[list[int]]:
    edges = {tuple(sorted(edge)) for edge in random_tree(rng, node_count, one_based=True)}
    pairs = [(a, b) for a in range(1, node_count + 1) for b in range(a + 1, node_count + 1)]
    rng.shuffle(pairs)
    for pair in pairs[: rng.randint(0, min(20, len(pairs)))]:
        edges.add(pair)
    result = [list(edge) for edge in sorted(edges)]
    rng.shuffle(result)
    return result


def g49189(rng: random.Random) -> list[object]:
    n = rng.randint(2, 20)
    return [n, connected_graph(rng, n)]


def g49191(rng: random.Random) -> list[object]:
    n = rng.randint(2, 15)
    ranking = list(range(1, n + 1))
    rng.shuffle(ranking)
    possible = [
        [ranking[left], ranking[right]]
        for left in range(n)
        for right in range(left + 1, n)
    ]
    results = rng.sample(possible, rng.randint(1, len(possible)))
    return [n, results]


def g49190(rng: random.Random) -> list[object]:
    return [[rng.randint(0, 7) for _ in range(rng.randint(1, 40))]]


GENERATORS: dict[int, Generator] = {
    lesson_id: globals()[f"g{lesson_id}"]
    for lesson_id in (
        1845, 42576, 178871, 42577, 42578, 42579,
        12906, 12909, 133502, 42586, 42587, 42583, 42584,
        138477, 42626, 42627, 42628,
        12915, 42748, 42747, 42746,
        131705, 42840, 86491, 42842, 42839, 87946, 86971, 84512,
        135808, 42862, 42885, 42884, 42883, 42860, 42861,
        340198, 43105, 42898, 42895, 1843, 42897,
        172928, 43165, 1844, 43162, 43163, 87694, 43164, 84021,
        12982, 43238, 43236,
        67256, 49189, 49191, 49190,
    )
}
