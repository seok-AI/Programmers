#!/usr/bin/env python3
"""로컬 PROBLEM.md의 기계화 가능한 입력 제한을 57문제별로 검사한다."""

from __future__ import annotations

import re
import string
from collections import Counter, deque


def constraint_errors(lesson_id: int, args: list[object]) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def rectangular(board: list[object]) -> bool:
        return bool(board) and bool(board[0]) and all(len(row) == len(board[0]) for row in board)

    def connected_node_count(n: int, edges: list[list[int]], start: int = 1) -> int:
        graph = [[] for _ in range(n + 1)]
        for left, right in edges:
            if 1 <= left <= n and 1 <= right <= n:
                graph[left].append(right)
                graph[right].append(left)
        seen = {start}
        queue = deque([start])
        while queue:
            for neighbor in graph[queue.popleft()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        return len(seen)

    try:
        if lesson_id == 1845:
            (nums,) = args
            require(1 <= len(nums) <= 10_000 and len(nums) % 2 == 0, "nums 길이는 10,000 이하의 짝수")
            require(all(isinstance(value, int) and 1 <= value <= 200_000 for value in nums), "종류 번호는 1~200,000")
        elif lesson_id == 42576:
            participant, completion = args
            require(1 <= len(participant) <= 100_000 and len(completion) == len(participant) - 1, "참가·완주자 수 관계")
            require(all(isinstance(name, str) and name.isalpha() and name.islower() and 1 <= len(name) <= 20 for name in [*participant, *completion]), "이름은 길이 1~20 소문자")
            participant_counts, completion_counts = Counter(participant), Counter(completion)
            require(all(completion_counts[name] <= participant_counts[name] for name in completion_counts), "완주자는 참가자 명단의 부분 다중집합")
        elif lesson_id == 178871:
            players, callings = args
            require(5 <= len(players) <= 50_000 and len(set(players)) == len(players), "players는 서로 다른 5~50,000명")
            require(all(isinstance(name, str) and name.isalpha() and name.islower() and 3 <= len(name) <= 10 for name in players), "선수 이름은 길이 3~10 소문자")
            require(2 <= len(callings) <= 1_000_000, "callings 길이는 2~1,000,000")
            ranking = list(players)
            positions = {name: index for index, name in enumerate(ranking)}
            for called in callings:
                if called not in positions or positions[called] == 0:
                    errors.append("호출 이름은 존재하며 호출 순간 1등이 아니어야 함")
                    break
                index = positions[called]
                front = ranking[index - 1]
                ranking[index - 1], ranking[index] = called, front
                positions[called], positions[front] = index - 1, index
        elif lesson_id == 42577:
            (phone_book,) = args
            require(1 <= len(phone_book) <= 1_000_000 and len(set(phone_book)) == len(phone_book), "전화번호는 1~1,000,000개이며 중복 없음")
            require(all(isinstance(number, str) and number.isdigit() and 1 <= len(number) <= 20 for number in phone_book), "전화번호는 길이 1~20 숫자 문자열")
        elif lesson_id == 42578:
            (clothes,) = args
            allowed = set(string.ascii_lowercase + "_")
            require(1 <= len(clothes) <= 30 and all(len(item) == 2 for item in clothes), "의상은 1~30개의 이름·종류 쌍")
            names = [item[0] for item in clothes]
            require(len(set(names)) == len(names), "의상 이름은 중복될 수 없음")
            require(all(isinstance(value, str) and 1 <= len(value) <= 20 and set(value) <= allowed for item in clothes for value in item), "의상 문자열은 길이 1~20 소문자·밑줄")
        elif lesson_id == 42579:
            genres, plays = args
            require(1 <= len(genres) == len(plays) <= 10_000 and len(set(genres)) < 100, "장르·재생수 배열 길이 및 장르 수")
            totals = Counter()
            for genre, play in zip(genres, plays):
                totals[genre] += play
            require(len(set(totals.values())) == len(totals), "서로 다른 장르 총 재생 수는 달라야 함")
        elif lesson_id == 12906:
            (arr,) = args
            require(1 <= len(arr) <= 1_000_000 and all(isinstance(value, int) and 0 <= value <= 9 for value in arr), "arr 길이 1~1,000,000, 원소 0~9")
        elif lesson_id == 12909:
            (s,) = args
            require(isinstance(s, str) and 1 <= len(s) <= 100_000 and set(s) <= {"(", ")"}, "s는 길이 1~100,000의 괄호 문자열")
        elif lesson_id == 133502:
            (ingredient,) = args
            require(1 <= len(ingredient) <= 1_000_000 and all(value in (1, 2, 3) for value in ingredient), "ingredient 길이와 원소 범위")
        elif lesson_id == 42586:
            progresses, speeds = args
            require(1 <= len(progresses) == len(speeds) <= 100, "두 배열 길이는 같고 1~100")
            require(all(1 <= value <= 99 for value in progresses), "초기 진도는 1~99")
            require(all(1 <= value <= 100 for value in speeds), "속도는 1~100")
        elif lesson_id == 42587:
            priorities, location = args
            require(1 <= len(priorities) <= 100 and all(1 <= value <= 9 for value in priorities), "우선순위 길이·범위")
            require(0 <= location < len(priorities), "location 범위")
        elif lesson_id == 42583:
            bridge_length, weight, trucks = args
            require(1 <= bridge_length <= 10_000 and 1 <= weight <= 10_000, "다리 길이·무게는 1~10,000")
            require(1 <= len(trucks) <= 10_000 and all(1 <= truck <= weight for truck in trucks), "트럭 수·무게 범위")
        elif lesson_id == 42584:
            (prices,) = args
            require(2 <= len(prices) <= 100_000 and all(1 <= price <= 10_000 for price in prices), "prices 길이·값 범위")
        elif lesson_id == 138477:
            k, score = args
            require(3 <= k <= 100 and 7 <= len(score) <= 1_000 and all(0 <= value <= 2_000 for value in score), "k·score 길이·점수 범위")
        elif lesson_id == 42626:
            scoville, k = args
            require(2 <= len(scoville) <= 1_000_000 and all(0 <= value <= 1_000_000 for value in scoville), "scoville 길이·값 범위")
            require(0 <= k <= 1_000_000_000, "K 범위")
        elif lesson_id == 42627:
            (jobs,) = args
            require(1 <= len(jobs) <= 500 and all(len(job) == 2 and 0 <= job[0] <= 1_000 and 1 <= job[1] <= 1_000 for job in jobs), "jobs 개수·요청·실행시간 범위")
        elif lesson_id == 42628:
            (operations,) = args
            require(1 <= len(operations) <= 1_000_000 and all(re.fullmatch(r"(?:I -?\d+|D (?:-1|1))", operation) for operation in operations), "operations 명령 형식·개수")
        elif lesson_id == 12915:
            strings_, n = args
            require(1 <= len(strings_) <= 50 and all(isinstance(value, str) and value.isalpha() and value.islower() and 1 <= len(value) <= 100 and len(value) > n for value in strings_), "strings 개수·문자·길이와 n 관계")
        elif lesson_id == 42748:
            array, commands = args
            require(1 <= len(array) <= 100 and all(1 <= value <= 100 for value in array), "array 길이·값 범위")
            require(1 <= len(commands) <= 50 and all(len(command) == 3 and 1 <= command[0] <= command[1] <= len(array) and 1 <= command[2] <= command[1] - command[0] + 1 for command in commands), "commands 유효 범위")
        elif lesson_id == 42747:
            (citations,) = args
            require(1 <= len(citations) <= 1_000 and all(0 <= value <= 10_000 for value in citations), "논문 수·인용 수 범위")
        elif lesson_id == 42746:
            (numbers,) = args
            require(1 <= len(numbers) <= 100_000 and all(isinstance(value, int) and 0 <= value <= 1_000 for value in numbers), "numbers 길이·값 범위")
        elif lesson_id == 131705:
            (numbers,) = args
            require(3 <= len(numbers) <= 13 and all(-1_000 <= value <= 1_000 for value in numbers), "number 길이·값 범위")
        elif lesson_id == 42840:
            (answers,) = args
            require(1 <= len(answers) <= 10_000 and all(1 <= value <= 5 for value in answers), "answers 길이·값 범위")
        elif lesson_id == 86491:
            (sizes,) = args
            require(1 <= len(sizes) <= 10_000 and all(len(size) == 2 and all(1 <= value <= 1_000 for value in size) for size in sizes), "명함 수·변 길이 범위")
        elif lesson_id == 42842:
            brown, yellow = args
            require(8 <= brown <= 5_000 and 1 <= yellow <= 2_000_000, "brown·yellow 범위")
            area = brown + yellow
            require(any(area % height == 0 and (area // height - 2) * (height - 2) == yellow for height in range(3, int(area**0.5) + 1)), "조건을 만족하는 카펫 크기 존재")
        elif lesson_id == 42839:
            (numbers,) = args
            require(isinstance(numbers, str) and 1 <= len(numbers) <= 7 and numbers.isdigit(), "numbers는 길이 1~7 숫자 문자열")
        elif lesson_id == 87946:
            k, dungeons = args
            require(1 <= k <= 5_000 and 1 <= len(dungeons) <= 8, "k·던전 수 범위")
            require(all(len(dungeon) == 2 and 1 <= dungeon[1] <= dungeon[0] <= 1_000 for dungeon in dungeons), "던전 피로도 범위·관계")
        elif lesson_id == 86971:
            n, wires = args
            require(2 <= n <= 100 and len(wires) == n - 1, "n과 전선 수 관계")
            require(all(len(wire) == 2 and 1 <= wire[0] < wire[1] <= n for wire in wires), "전선 정점 순서·범위")
            require(connected_node_count(n, wires) == n, "전선 그래프는 트리로 연결되어야 함")
        elif lesson_id == 84512:
            (word,) = args
            require(isinstance(word, str) and 1 <= len(word) <= 5 and set(word) <= set("AEIOU"), "word 길이·문자 범위")
        elif lesson_id == 135808:
            k, m, score = args
            require(3 <= k <= 9 and 3 <= m <= 10, "k·m 범위")
            require(7 <= len(score) <= 1_000_000 and all(1 <= value <= k for value in score), "score 길이·값 범위")
        elif lesson_id == 42862:
            n, lost, reserve = args
            require(2 <= n <= 30 and 1 <= len(lost) <= n and 1 <= len(reserve) <= n, "n·lost·reserve 길이 범위")
            require(len(set(lost)) == len(lost) and len(set(reserve)) == len(reserve) and all(1 <= value <= n for value in [*lost, *reserve]), "학생 번호 범위·배열 내 중복 없음")
        elif lesson_id == 42885:
            people, limit = args
            require(1 <= len(people) <= 50_000 and 40 <= limit <= 240, "사람 수·limit 범위")
            require(all(40 <= weight <= limit for weight in people), "몸무게는 40 이상 limit 이하")
        elif lesson_id == 42884:
            (routes,) = args
            require(1 <= len(routes) <= 10_000 and all(len(route) == 2 and -30_000 <= route[0] <= route[1] <= 30_000 for route in routes), "차량 수·경로 좌표 범위")
        elif lesson_id == 42883:
            number, k = args
            require(isinstance(number, str) and 2 <= len(number) <= 1_000_000 and number.isdigit(), "number 길이·문자")
            require(1 <= k < len(number), "k 범위")
        elif lesson_id == 42860:
            (name,) = args
            require(isinstance(name, str) and 1 <= len(name) <= 20 and name.isalpha() and name.isupper(), "name은 길이 1~20 대문자")
        elif lesson_id == 42861:
            n, costs = args
            pairs = [tuple(sorted((left, right))) for left, right, _ in costs]
            require(1 <= n <= 100 and len(costs) <= n * (n - 1) // 2, "n·간선 수 범위")
            require(len(set(pairs)) == len(pairs) and all(0 <= left < n and 0 <= right < n and left != right for left, right, _ in costs), "섬 쌍 중복 없음·정점 범위")
            one_based = [[left + 1, right + 1] for left, right, _ in costs]
            require(n == 1 or connected_node_count(n, one_based) == n, "모든 섬이 연결 가능해야 함")
        elif lesson_id == 340198:
            mats, park = args
            require(1 <= len(mats) <= 10 and len(set(mats)) == len(mats) and all(1 <= value <= 20 for value in mats), "mats 길이·중복·값 범위")
            require(rectangular(park) and 1 <= len(park) <= 50 and 1 <= len(park[0]) <= 50, "park는 1~50 직사각 격자")
            require(all(cell == "-1" or isinstance(cell, str) and len(cell) == 1 and cell.isalpha() for row in park for cell in row), "park 칸 문자열 형식")
        elif lesson_id == 43105:
            (triangle,) = args
            require(1 <= len(triangle) <= 500 and all(len(row) == index + 1 and all(0 <= value <= 9_999 for value in row) for index, row in enumerate(triangle)), "삼각형 높이·행 길이·값 범위")
        elif lesson_id == 42898:
            m, n, puddles = args
            require(1 <= m <= 100 and 1 <= n <= 100 and not (m == n == 1), "m·n 범위와 1×1 제외")
            require(len(puddles) <= 10 and all(len(point) == 2 and 1 <= point[0] <= m and 1 <= point[1] <= n for point in puddles), "물웅덩이 수·좌표 범위")
            require([1, 1] not in puddles and [m, n] not in puddles, "집과 학교는 물웅덩이가 아님")
        elif lesson_id == 42895:
            n, number = args
            require(1 <= n <= 9 and 1 <= number <= 32_000, "N·number 범위")
        elif lesson_id == 1843:
            (arr,) = args
            require(3 <= len(arr) <= 201 and len(arr) % 2 == 1, "arr는 길이 3~201 홀수")
            require(all(arr[index].isdigit() and 1 <= int(arr[index]) <= 1_000 for index in range(0, len(arr), 2)), "숫자 위치 값 범위")
            require(all(arr[index] in ("+", "-") for index in range(1, len(arr), 2)), "연산자 위치는 + 또는 -")
        elif lesson_id == 42897:
            (money,) = args
            require(3 <= len(money) <= 1_000_000 and all(0 <= value <= 1_000 for value in money), "money 길이·값 범위")
        elif lesson_id == 172928:
            park, routes = args
            require(rectangular(park) and 3 <= len(park) <= 50 and 3 <= len(park[0]) <= 50, "공원 행·열은 3~50")
            require(sum(row.count("S") for row in park) == 1 and all(set(row) <= {"S", "O", "X"} for row in park), "공원 문자와 시작점 수")
            require(1 <= len(routes) <= 50 and all(re.fullmatch(r"[NSWE] [1-9]", route) for route in routes), "routes 수·명령 형식")
        elif lesson_id == 43165:
            numbers, target = args
            require(2 <= len(numbers) <= 20 and all(1 <= value <= 50 for value in numbers), "numbers 길이·값 범위")
            require(1 <= target <= 1_000, "target 범위")
        elif lesson_id == 1844:
            (maps,) = args
            require(rectangular(maps) and 1 <= len(maps) <= 100 and 1 <= len(maps[0]) <= 100 and not (len(maps) == len(maps[0]) == 1), "맵 행·열 범위와 1×1 제외")
            require(all(cell in (0, 1) for row in maps for cell in row), "맵 칸은 0 또는 1")
        elif lesson_id == 43162:
            n, computers = args
            require(1 <= n <= 200 and len(computers) == n and all(len(row) == n for row in computers), "n과 n×n 행렬")
            require(all(cell in (0, 1) for row in computers for cell in row) and all(computers[index][index] == 1 for index in range(n)), "행렬 값과 대각선")
            require(all(computers[left][right] == computers[right][left] for left in range(n) for right in range(n)), "직접 연결 행렬은 대칭")
        elif lesson_id == 43163:
            begin, target, words = args
            all_words = [begin, target, *words]
            require(3 <= len(words) <= 50 and len(set(words)) == len(words), "words 수·중복 없음")
            require(begin != target and len({len(word) for word in all_words}) == 1, "begin·target 다름과 같은 단어 길이")
            require(all(isinstance(word, str) and word.isalpha() and word.islower() and 3 <= len(word) <= 10 for word in all_words), "단어는 길이 3~10 소문자")
        elif lesson_id == 87694:
            rectangles, character_x, character_y, item_x, item_y = args
            require(1 <= len(rectangles) <= 4 and all(len(rect) == 4 and 1 <= rect[0] < rect[2] <= 50 and 1 <= rect[1] < rect[3] <= 50 for rect in rectangles), "직사각형 수·좌표 범위")
            require(len({value for rect in rectangles for value in (rect[0], rect[2])}) == 2 * len(rectangles) and len({value for rect in rectangles for value in (rect[1], rect[3])}) == 2 * len(rectangles), "서로 다른 직사각형은 x·y 끝좌표를 공유하지 않음")
            require(
                all(
                    not (
                        outer_rect[0] < inner_rect[0] < inner_rect[2] < outer_rect[2]
                        and outer_rect[1] < inner_rect[1] < inner_rect[3] < outer_rect[3]
                    )
                    for outer_index, outer_rect in enumerate(rectangles)
                    for inner_index, inner_rect in enumerate(rectangles)
                    if outer_index != inner_index
                ),
                "한 직사각형이 다른 직사각형에 완전히 포함될 수 없음",
            )
            overlap_graph = [[] for _ in rectangles]
            for left in range(len(rectangles)):
                for right in range(left + 1, len(rectangles)):
                    a, b = rectangles[left], rectangles[right]
                    if max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3]):
                        overlap_graph[left].append(right)
                        overlap_graph[right].append(left)
            seen_rectangles = {0}
            queue = deque([0])
            while queue:
                for neighbor in overlap_graph[queue.popleft()]:
                    if neighbor not in seen_rectangles:
                        seen_rectangles.add(neighbor)
                        queue.append(neighbor)
            require(len(seen_rectangles) == len(rectangles), "직사각형 합집합은 분리되지 않아야 함")
            def outer(point_x: int, point_y: int) -> bool:
                on_edge = any(x1 <= point_x <= x2 and y1 <= point_y <= y2 and (point_x in (x1, x2) or point_y in (y1, y2)) for x1, y1, x2, y2 in rectangles)
                inside = any(x1 < point_x < x2 and y1 < point_y < y2 for x1, y1, x2, y2 in rectangles)
                return on_edge and not inside
            require((character_x, character_y) != (item_x, item_y) and outer(character_x, character_y) and outer(item_x, item_y), "시작·아이템은 서로 다른 바깥 테두리 점")
        elif lesson_id == 43164:
            (tickets,) = args
            require(3 <= len(tickets) <= 10_000 and all(len(ticket) == 2 and all(isinstance(code, str) and len(code) == 3 and code.isalpha() and code.isupper() for code in ticket) for ticket in tickets), "항공권 수·공항 코드 형식")
            graph: dict[str, list[str]] = {}
            for departure, arrival in tickets:
                graph.setdefault(departure, []).append(arrival)
            stack, route = ["ICN"], []
            while stack:
                if graph.get(stack[-1]):
                    stack.append(graph[stack[-1]].pop())
                else:
                    route.append(stack.pop())
            candidate = route[::-1]
            used = Counter(zip(candidate, candidate[1:]))
            require(len(candidate) == len(tickets) + 1 and used == Counter(map(tuple, tickets)), "ICN에서 모든 항공권을 쓰는 경로 존재")
        elif lesson_id == 84021:
            game_board, table = args
            size = len(game_board)
            require(3 <= size <= 50 and len(table) == size and all(len(row) == size for row in [*game_board, *table]), "두 보드는 같은 3~50 정사각 행렬")
            require(all(cell in (0, 1) for row in [*game_board, *table] for cell in row), "보드 칸은 0 또는 1")
            require(any(0 in row for row in game_board) and any(1 in row for row in table), "빈칸과 조각이 각각 하나 이상")
            def component_sizes(board: list[list[int]], target: int) -> list[int]:
                seen: set[tuple[int, int]] = set()
                sizes = []
                for start_row in range(size):
                    for start_column in range(size):
                        if board[start_row][start_column] != target or (start_row, start_column) in seen:
                            continue
                        seen.add((start_row, start_column))
                        queue = deque([(start_row, start_column)])
                        count = 0
                        while queue:
                            row, column = queue.popleft()
                            count += 1
                            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                                point = row + dr, column + dc
                                if 0 <= point[0] < size and 0 <= point[1] < size and point not in seen and board[point[0]][point[1]] == target:
                                    seen.add(point)
                                    queue.append(point)
                        sizes.append(count)
                return sizes
            require(all(1 <= value <= 6 for value in component_sizes(game_board, 0) + component_sizes(table, 1)), "각 빈 영역·조각 크기는 1~6")
        elif lesson_id == 12982:
            departments, budget = args
            require(1 <= len(departments) <= 100 and all(1 <= value <= 100_000 for value in departments), "부서 수·신청액 범위")
            require(1 <= budget <= 10_000_000, "budget 범위")
        elif lesson_id == 43238:
            n, times = args
            require(1 <= n <= 1_000_000_000 and 1 <= len(times) <= 100_000 and all(1 <= value <= 1_000_000_000 for value in times), "n·심사관 수·시간 범위")
        elif lesson_id == 43236:
            distance, rocks, n = args
            require(1 <= distance <= 1_000_000_000 and 1 <= len(rocks) <= 50_000 and len(set(rocks)) == len(rocks), "distance·바위 수·중복 없음")
            require(all(0 < rock < distance for rock in rocks) and 1 <= n <= len(rocks), "바위 위치와 n 범위")
        elif lesson_id == 67256:
            numbers, hand = args
            require(1 <= len(numbers) <= 1_000 and all(0 <= value <= 9 for value in numbers), "numbers 길이·값 범위")
            require(hand in ("left", "right"), "hand 값")
        elif lesson_id == 49189:
            n, edges = args
            require(2 <= n <= 20_000 and 1 <= len(edges) <= 50_000 and all(len(edge) == 2 and 1 <= edge[0] <= n and 1 <= edge[1] <= n for edge in edges), "n·간선 수·정점 범위")
            require(connected_node_count(n, edges) == n, "1번에서 모든 정점 도달 가능")
        elif lesson_id == 49191:
            n, results = args
            require(1 <= n <= 100 and 1 <= len(results) <= 4_500 and len({tuple(result) for result in results}) == len(results), "n·경기 수·중복 없음")
            graph = [[] for _ in range(n + 1)]
            indegree = [0] * (n + 1)
            for winner, loser in results:
                if 1 <= winner <= n and 1 <= loser <= n and winner != loser:
                    graph[winner].append(loser)
                    indegree[loser] += 1
                else:
                    errors.append("경기 정점 범위와 자기 경기 금지")
                    break
            queue = deque(node for node in range(1, n + 1) if indegree[node] == 0)
            visited = 0
            while queue:
                node = queue.popleft()
                visited += 1
                for neighbor in graph[node]:
                    indegree[neighbor] -= 1
                    if indegree[neighbor] == 0:
                        queue.append(neighbor)
            require(visited == n, "경기 결과에는 순환 모순이 없어야 함")
        elif lesson_id == 49190:
            (arrows,) = args
            require(1 <= len(arrows) <= 100_000 and all(0 <= value <= 7 for value in arrows), "arrows 길이·값 범위")
        else:
            errors.append(f"등록되지 않은 문제 번호: {lesson_id}")
    except (IndexError, KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        errors.append(f"인자 형식 오류: {type(error).__name__}: {error}")
    return errors
