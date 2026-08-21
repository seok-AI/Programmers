#!/usr/bin/env python3
"""문제별 주석 예시 풀이를 생성하는 독립 구현 모음.

각 함수는 공개적으로 널리 알려진 알고리즘 접근을 바탕으로 이 저장소를 위해 새로
작성했다. 생성 결과는 문제 폴더의 solutions/ 아래에 독립 실행 가능한 형태로 저장된다.
"""

from __future__ import annotations

import ast
import inspect
import json
import re
import textwrap
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import cmp_to_key, lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
from bisect import bisect_left, insort
import heapq
import math

try:
    from .pedagogy_bank import PEDAGOGY
    from .problem_paths import problem_id
except ImportError:
    from pedagogy_bank import PEDAGOGY
    from problem_paths import problem_id


ROOT = Path(__file__).resolve().parents[1]
SHARED_REFERENCE = "https://github.com/codeisneverodd/programmers-coding-test"
SHARED_REFERENCE_COMMIT = "a7e263009f5cc5694957b10b91005dc2dbc2129d"
SHARED_REFERENCE_DATA = (
    f"{SHARED_REFERENCE}/blob/{SHARED_REFERENCE_COMMIT}/data/solutions.json"
)


@dataclass(frozen=True)
class Entry:
    lesson_id: int
    variant: str
    approach: str
    complexity: str
    note: str
    function: object


ENTRIES: dict[tuple[int, str], Entry] = {}


def register(
    lesson_id: int,
    variant: str,
    approach: str,
    complexity: str,
    note: str = "",
):
    def decorator(function):
        ENTRIES[(lesson_id, variant)] = Entry(
            lesson_id, variant, approach, complexity, note, function
        )
        return function

    return decorator


# ---------------------------------------------------------------------------
# 01 해시
# ---------------------------------------------------------------------------


@register(42576, "recommended", "Counter로 참가/완주 빈도 차감", "O(n) time, O(n) space")
def p42576_recommended(participant, completion):
    # 동명이인을 보존하려면 집합이 아니라 이름별 등장 횟수가 필요하다.
    remaining = Counter(participant)
    remaining.subtract(completion)

    # 정확히 한 사람만 남는다는 입력 보장이 있다.
    return next(name for name, count in remaining.items() if count > 0)


@register(42576, "alternative", "두 목록 정렬 후 첫 불일치 탐색", "O(n log n) time, O(n) space")
def p42576_alternative(participant, completion):
    # 정렬하면 같은 이름이 나란히 오므로 처음 다른 위치가 미완주자다.
    participants = sorted(participant)
    completions = sorted(completion)
    for runner, finisher in zip(participants, completions):
        if runner != finisher:
            return runner
    return participants[-1]


@register(1845, "recommended", "종류 수와 선택 가능 수의 작은 값", "O(n) time, O(n) space")
def p1845_recommended(nums):
    # 서로 다른 종류를 한 마리씩 먼저 고를 수 있지만 총 선택 수 N/2를 넘을 수 없다.
    return min(len(set(nums)), len(nums) // 2)


@register(1845, "alternative", "빈도표의 키 수로 종류 계산", "O(n) time, O(n) space")
def p1845_alternative(nums):
    kinds = Counter(nums)
    capacity = len(nums) // 2
    return capacity if len(kinds) >= capacity else len(kinds)


@register(42577, "recommended", "정렬 후 인접 전화번호만 비교", "O(n log n) time, O(n) space")
def p42577_recommended(phone_book):
    # 접두어 관계가 있다면 사전순 정렬에서 두 번호가 반드시 인접한다.
    ordered = sorted(phone_book)
    return all(not right.startswith(left) for left, right in zip(ordered, ordered[1:]))


@register(42577, "alternative", "각 번호의 모든 진접두어를 해시 조회", "O(total digits) time, O(n) space")
def p42577_alternative(phone_book):
    numbers = set(phone_book)
    for number in phone_book:
        # 자기 자신은 비교 대상이 아니므로 마지막 문자는 제외한다.
        for end in range(1, len(number)):
            if number[:end] in numbers:
                return False
    return True


@register(42578, "recommended", "종류별 (선택+미선택) 경우를 곱함", "O(n) time, O(n) space")
def p42578_recommended(clothes):
    counts = Counter(kind for _, kind in clothes)
    combinations_count = 1
    for count in counts.values():
        combinations_count *= count + 1  # 이 종류를 입지 않는 한 경우 포함
    return combinations_count - 1  # 아무것도 입지 않는 경우 제외


@register(42578, "alternative", "종류를 하나씩 추가하는 1상태 DP", "O(n) time, O(n) space")
def p42578_alternative(clothes):
    counts = Counter(kind for _, kind in clothes)
    ways = 1  # 아직 아무 종류도 처리하지 않았을 때 빈 선택 한 가지
    for count in counts.values():
        ways += ways * count
    return ways - 1


@register(42579, "recommended", "장르 집계 후 장르/곡 다중 정렬", "O(n log n) time, O(n) space")
def p42579_recommended(genres, plays):
    totals = defaultdict(int)
    songs = defaultdict(list)
    for index, (genre, play) in enumerate(zip(genres, plays)):
        totals[genre] += play
        songs[genre].append((play, index))

    answer = []
    for genre in sorted(totals, key=totals.get, reverse=True):
        # 재생 수 내림차순, 고유 번호 오름차순.
        songs[genre].sort(key=lambda item: (-item[0], item[1]))
        answer.extend(index for _, index in songs[genre][:2])
    return answer


@register(42579, "alternative", "전체 인덱스를 장르 총합/곡 재생수로 한 번 정렬", "O(n log n) time, O(n) space")
def p42579_alternative(genres, plays):
    totals = Counter()
    for genre, play in zip(genres, plays):
        totals[genre] += play

    ordered = sorted(
        range(len(genres)),
        key=lambda i: (-totals[genres[i]], -plays[i], i),
    )
    used = Counter()
    answer = []
    for index in ordered:
        genre = genres[index]
        if used[genre] < 2:
            answer.append(index)
            used[genre] += 1
    return answer


@register(178871, "recommended", "이름-순위 역인덱스로 인접 교환", "O(n+m) time, O(n) space")
def p178871_recommended(players, callings):
    ranking = list(players)  # 입력 변형을 피한다.
    position = {name: rank for rank, name in enumerate(ranking)}

    for called in callings:
        current = position[called]
        overtaken = ranking[current - 1]
        ranking[current - 1], ranking[current] = called, overtaken
        position[called] = current - 1
        position[overtaken] = current
    return ranking


@register(178871, "alternative", "두 방향 매핑을 명시적으로 동기화", "O(n+m) time, O(n) space")
def p178871_alternative(players, callings):
    rank_to_name = dict(enumerate(players))
    name_to_rank = {name: rank for rank, name in rank_to_name.items()}

    for name in callings:
        rank = name_to_rank[name]
        front_name = rank_to_name[rank - 1]
        rank_to_name[rank - 1], rank_to_name[rank] = name, front_name
        name_to_rank[name], name_to_rank[front_name] = rank - 1, rank
    return [rank_to_name[rank] for rank in range(len(players))]


# ---------------------------------------------------------------------------
# 02 스택/큐
# ---------------------------------------------------------------------------


@register(12906, "recommended", "직전 값과 다른 원소만 결과에 추가", "O(n) time, O(n) space")
def p12906_recommended(arr):
    answer = []
    for value in arr:
        if not answer or answer[-1] != value:
            answer.append(value)
    return answer


@register(12906, "alternative", "연속 그룹의 첫 원소 선택", "O(n) time, O(n) space")
def p12906_alternative(arr):
    if not arr:
        return []
    answer = [arr[0]]
    for previous, current in zip(arr, arr[1:]):
        if previous != current:
            answer.append(current)
    return answer


@register(12909, "recommended", "접두 구간의 괄호 균형 유지", "O(n) time, O(1) space")
def p12909_recommended(s):
    balance = 0
    for char in s:
        balance += 1 if char == "(" else -1
        # 닫는 괄호가 먼저 많아지면 이후 문자로 복구해도 올바른 접두부가 아니다.
        if balance < 0:
            return False
    return balance == 0


@register(12909, "alternative", "여는 괄호를 스택에 저장", "O(n) time, O(n) space")
def p12909_alternative(s):
    stack = []
    for char in s:
        if char == "(":
            stack.append(char)
        elif not stack:
            return False
        else:
            stack.pop()
    return not stack


@register(133502, "recommended", "최근 네 재료를 스택에서 즉시 제거", "O(n) time, O(n) space")
def p133502_recommended(ingredient):
    stack = []
    burgers = 0
    for item in ingredient:
        stack.append(item)
        if len(stack) >= 4 and stack[-4:] == [1, 2, 3, 1]:
            del stack[-4:]
            burgers += 1
    return burgers


@register(133502, "alternative", "고정 배열과 top 포인터로 스택 구현", "O(n) time, O(n) space")
def p133502_alternative(ingredient):
    stack = [0] * len(ingredient)
    top = 0
    burgers = 0
    for item in ingredient:
        stack[top] = item
        top += 1
        if top >= 4 and stack[top - 4 : top] == [1, 2, 3, 1]:
            top -= 4
            burgers += 1
    return burgers


@register(42586, "recommended", "기능별 완료일 계산 후 비감소 배포 경계 그룹화", "O(n) time, O(n) space")
def p42586_recommended(progresses, speeds):
    days = [math.ceil((100 - progress) / speed) for progress, speed in zip(progresses, speeds)]
    answer = []
    release_day = days[0]
    batch = 0
    for day in days:
        if day <= release_day:
            batch += 1
        else:
            answer.append(batch)
            release_day = day
            batch = 1
    answer.append(batch)
    return answer


@register(42586, "alternative", "완료일 큐에서 선두 이하를 묶어 배포", "O(n) time, O(n) space")
def p42586_alternative(progresses, speeds):
    queue = deque(
        math.ceil((100 - progress) / speed)
        for progress, speed in zip(progresses, speeds)
    )
    answer = []
    while queue:
        release_day = queue.popleft()
        count = 1
        while queue and queue[0] <= release_day:
            queue.popleft()
            count += 1
        answer.append(count)
    return answer


@register(42587, "recommended", "큐 순환과 남은 우선순위 빈도표", "O(n) time, O(n) space")
def p42587_recommended(priorities, location):
    queue = deque(enumerate(priorities))
    counts = Counter(priorities)
    current_max = max(counts)
    executed = 0

    while queue:
        index, priority = queue.popleft()
        if priority < current_max:
            queue.append((index, priority))
            continue
        executed += 1
        counts[priority] -= 1
        if counts[priority] == 0:
            del counts[priority]
            current_max = max(counts, default=0)
        if index == location:
            return executed


@register(42587, "alternative", "매 회차 큐의 최대 우선순위와 비교", "O(n^2) time, O(n) space", "n<=100에서 충분한 단순 풀이")
def p42587_alternative(priorities, location):
    queue = deque(enumerate(priorities))
    executed = 0
    while queue:
        item = queue.popleft()
        if queue and item[1] < max(priority for _, priority in queue):
            queue.append(item)
            continue
        executed += 1
        if item[0] == location:
            return executed


@register(42583, "recommended", "트럭별 진입 시각과 종료 시각을 이벤트로 관리", "O(n) time, O(n) space")
def p42583_recommended(bridge_length, weight, truck_weights):
    waiting = deque(truck_weights)
    crossing = deque()  # (exit_time, truck_weight)
    current_weight = 0
    time = 0

    while waiting or crossing:
        # 다리가 비고 다음 진입까지 기다릴 이유가 없으면 다음 종료 시각으로 이동한다.
        if crossing and (not waiting or current_weight + waiting[0] > weight):
            time = max(time + 1, crossing[0][0])
        else:
            time += 1

        while crossing and crossing[0][0] <= time:
            _, truck = crossing.popleft()
            current_weight -= truck

        if waiting and current_weight + waiting[0] <= weight:
            truck = waiting.popleft()
            current_weight += truck
            crossing.append((time + bridge_length, truck))
    return time


@register(42583, "alternative", "다리 길이만큼의 고정 큐를 매초 이동", "O(total seconds) time, O(bridge_length) space")
def p42583_alternative(bridge_length, weight, truck_weights):
    waiting = deque(truck_weights)
    bridge = deque([0] * bridge_length)
    bridge_weight = 0
    time = 0

    while waiting:
        time += 1
        bridge_weight -= bridge.popleft()
        if bridge_weight + waiting[0] <= weight:
            truck = waiting.popleft()
            bridge.append(truck)
            bridge_weight += truck
        else:
            bridge.append(0)
    return time + bridge_length


@register(42584, "recommended", "가격이 처음 떨어지는 시점을 단조 스택으로 확정", "O(n) time, O(n) space")
def p42584_recommended(prices):
    answer = [0] * len(prices)
    stack = []
    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            previous = stack.pop()
            answer[previous] = index - previous
        stack.append(index)
    last = len(prices) - 1
    while stack:
        previous = stack.pop()
        answer[previous] = last - previous
    return answer


@register(42584, "alternative", "기본 지속 시간을 채운 뒤 단조 스택으로 하락 시점 갱신", "O(n) time, O(n) space")
def p42584_alternative(prices):
    last = len(prices) - 1
    answer = [last - index for index in range(len(prices))]
    unresolved = []
    for current, price in enumerate(prices):
        while unresolved and prices[unresolved[-1]] > price:
            previous = unresolved.pop()
            answer[previous] = current - previous
        unresolved.append(current)
    return answer


# ---------------------------------------------------------------------------
# 03 힙
# ---------------------------------------------------------------------------


@register(138477, "recommended", "크기 k의 최소 힙으로 상위 점수 유지", "O(n log k) time, O(k) space")
def p138477_recommended(k, score):
    hall = []
    answer = []
    for value in score:
        if len(hall) < k:
            heapq.heappush(hall, value)
        elif value > hall[0]:
            heapq.heapreplace(hall, value)
        answer.append(hall[0])
    return answer


@register(138477, "alternative", "정렬 리스트를 k개 이하로 유지", "O(n*k) time, O(k) space", "k<=100이라 충분한 대안")
def p138477_alternative(k, score):
    hall = []
    answer = []
    for value in score:
        insort(hall, value)
        if len(hall) > k:
            hall.pop(0)
        answer.append(hall[0])
    return answer


@register(42626, "recommended", "최소 힙에서 가장 작은 두 음식 반복 혼합", "O(n log n) time, O(n) space")
def p42626_recommended(scoville, K):
    heap = list(scoville)
    heapq.heapify(heap)
    mixes = 0
    while heap and heap[0] < K:
        if len(heap) < 2:
            return -1
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        heapq.heappush(heap, first + 2 * second)
        mixes += 1
    return mixes


@register(42626, "alternative", "정렬 원본 큐와 비감소 생성값 큐 병합", "O(n log n) time, O(n) space")
def p42626_alternative(scoville, K):
    original = deque(sorted(scoville))
    mixed = deque()

    def pop_smallest():
        if not original:
            return mixed.popleft()
        if not mixed:
            return original.popleft()
        return original.popleft() if original[0] <= mixed[0] else mixed.popleft()

    count = 0
    while len(original) + len(mixed) >= 1:
        smallest = pop_smallest()
        if smallest >= K:
            return count
        if not original and not mixed:
            return -1
        second = pop_smallest()
        mixed.append(smallest + 2 * second)
        count += 1
    return -1


@register(42627, "recommended", "요청 시각 정렬 + 실행 시간 우선 힙", "O(n log n) time, O(n) space")
def p42627_recommended(jobs):
    ordered = sorted((request, duration, index) for index, (request, duration) in enumerate(jobs))
    heap = []
    time = total = cursor = 0

    while cursor < len(ordered) or heap:
        if not heap and cursor < len(ordered) and time < ordered[cursor][0]:
            time = ordered[cursor][0]
        while cursor < len(ordered) and ordered[cursor][0] <= time:
            request, duration, index = ordered[cursor]
            heapq.heappush(heap, (duration, request, index))
            cursor += 1
        duration, request, _ = heapq.heappop(heap)
        time += duration
        total += time - request
    return total // len(jobs)


@register(42627, "alternative", "매 시점 가능한 작업을 선형 선택", "O(n^2) time, O(n) space", "n<=500에서 이해하기 쉬운 대안")
def p42627_alternative(jobs):
    remaining = [(request, duration, index) for index, (request, duration) in enumerate(jobs)]
    time = total = 0
    while remaining:
        available = [job for job in remaining if job[0] <= time]
        if not available:
            time = min(request for request, _, _ in remaining)
            available = [job for job in remaining if job[0] <= time]
        chosen = min(available, key=lambda job: (job[1], job[0], job[2]))
        remaining.remove(chosen)
        request, duration, _ = chosen
        time += duration
        total += time - request
    return total // len(jobs)


@register(42628, "recommended", "최소/최대 힙과 활성 ID로 지연 삭제", "O(n log n) time, O(n) space")
def p42628_recommended(operations):
    min_heap = []
    max_heap = []
    active = set()
    serial = 0

    for operation in operations:
        command, raw = operation.split()
        value = int(raw)
        if command == "I":
            heapq.heappush(min_heap, (value, serial))
            heapq.heappush(max_heap, (-value, serial))
            active.add(serial)
            serial += 1
            continue

        heap = max_heap if value == 1 else min_heap
        while heap and heap[0][1] not in active:
            heapq.heappop(heap)
        if heap:
            _, item_id = heapq.heappop(heap)
            active.remove(item_id)

    while min_heap and min_heap[0][1] not in active:
        heapq.heappop(min_heap)
    while max_heap and max_heap[0][1] not in active:
        heapq.heappop(max_heap)
    return [-max_heap[0][0], min_heap[0][0]] if active else [0, 0]


@register(42628, "alternative", "두 힙과 값별 개수로 지연 삭제", "O(n log n) time, O(n) space")
def p42628_alternative(operations):
    minimums = []
    maximums = []
    counts = Counter()
    size = 0

    def discard_stale(heap, sign):
        while heap and counts[sign * heap[0]] == 0:
            heapq.heappop(heap)

    for operation in operations:
        command, raw = operation.split()
        value = int(raw)
        if command == "I":
            heapq.heappush(minimums, value)
            heapq.heappush(maximums, -value)
            counts[value] += 1
            size += 1
        elif size:
            heap = maximums if value == 1 else minimums
            sign = -1 if value == 1 else 1
            discard_stale(heap, sign)
            removed = sign * heapq.heappop(heap)
            counts[removed] -= 1
            size -= 1

    if not size:
        return [0, 0]
    discard_stale(minimums, 1)
    discard_stale(maximums, -1)
    return [-maximums[0], minimums[0]]


# ---------------------------------------------------------------------------
# 04 정렬
# ---------------------------------------------------------------------------


@register(12915, "recommended", "n번째 문자와 전체 문자열의 복합 키", "O(m log m) time, O(m) space")
def p12915_recommended(strings, n):
    return sorted(strings, key=lambda word: (word[n], word))


@register(12915, "alternative", "사전순 선행 정렬 뒤 안정 정렬", "O(m log m) time, O(m) space")
def p12915_alternative(strings, n):
    # Python 정렬은 안정적이므로 두 번째 정렬의 동률에서 사전순이 보존된다.
    ordered = sorted(strings)
    ordered.sort(key=lambda word: word[n])
    return ordered


@register(42748, "recommended", "명령별 슬라이스 정렬", "O(q*k log k) time, O(k) space")
def p42748_recommended(array, commands):
    return [sorted(array[start - 1 : end])[rank - 1] for start, end, rank in commands]


@register(42748, "alternative", "반복문으로 1기반 명령을 명시적으로 변환", "O(q*k log k) time, O(k) space")
def p42748_alternative(array, commands):
    answer = []
    for start, end, rank in commands:
        section = list(array[start - 1 : end])
        section.sort()
        answer.append(section[rank - 1])
    return answer


@register(42747, "recommended", "정렬한 인용수와 남은 논문 수 비교", "O(n log n) time, O(n) space")
def p42747_recommended(citations):
    ordered = sorted(citations)
    count = len(ordered)
    for index, citation in enumerate(ordered):
        papers = count - index
        if citation >= papers:
            return papers
    return 0


@register(42747, "alternative", "가능한 h를 큰 값부터 직접 검증", "O(n^2) time, O(1) space", "n<=1,000에서 가능한 정의 그대로의 풀이")
def p42747_alternative(citations):
    for h in range(len(citations), -1, -1):
        high = sum(citation >= h for citation in citations)
        low = sum(citation <= h for citation in citations)
        if high >= h and low >= len(citations) - h:
            return h


@register(42746, "recommended", "a+b와 b+a를 비교하는 사용자 정렬", "O(n log n) time, O(n) space")
def p42746_recommended(numbers):
    strings = list(map(str, numbers))

    def compare(left, right):
        if left + right > right + left:
            return -1
        if left + right < right + left:
            return 1
        return 0

    result = "".join(sorted(strings, key=cmp_to_key(compare)))
    return "0" if result[0] == "0" else result


@register(42746, "alternative", "최대 4자리 반복 키로 내림차순 정렬", "O(n log n) time, O(n) space", "각 수가 0..1000인 제한을 이용")
def p42746_alternative(numbers):
    strings = list(map(str, numbers))
    # 원소 길이가 최대 4이므로 충분히 반복한 앞 4문자가 비교 순서를 결정한다.
    strings.sort(key=lambda value: (value * 4)[:4], reverse=True)
    result = "".join(strings)
    # int 변환은 100,000자리 입력에서 불필요하게 큰 정수를 만들므로 피한다.
    return "0" if result[0] == "0" else result


# ---------------------------------------------------------------------------
# 05 완전탐색
# ---------------------------------------------------------------------------


@register(131705, "recommended", "세 수의 조합을 열거해 합이 0인지 확인", "O(n^3) time, O(1) extra space")
def p131705_recommended(number):
    # 사람의 순서는 중요하지 않으므로 순열이 아닌 조합을 사용한다.
    return sum(a + b + c == 0 for a, b, c in combinations(number, 3))


@register(131705, "alternative", "서로 다른 세 인덱스를 삼중 반복문으로 선택", "O(n^3) time, O(1) space")
def p131705_alternative(number):
    answer = 0
    for first in range(len(number) - 2):
        for second in range(first + 1, len(number) - 1):
            for third in range(second + 1, len(number)):
                if number[first] + number[second] + number[third] == 0:
                    answer += 1
    return answer


@register(42839, "recommended", "모든 숫자 순열을 집합에 모아 소수 판정", "O(sum P(n,k) * sqrt(M)) time, O(sum P(n,k)) space")
def p42839_recommended(numbers):
    candidates = set()
    for length in range(1, len(numbers) + 1):
        candidates.update(int("".join(digits)) for digits in permutations(numbers, length))

    def is_prime(value):
        if value < 2:
            return False
        if value % 2 == 0:
            return value == 2
        divisor = 3
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 2
        return True

    return sum(is_prime(value) for value in candidates)


@register(42839, "alternative", "DFS로 수를 만들고 에라토스테네스의 체로 일괄 판정", "O(n*n! + M log log M) time, O(M) space")
def p42839_alternative(numbers):
    made = set()
    used = [False] * len(numbers)

    def build(current):
        if current:
            made.add(int(current))
        for index, digit in enumerate(numbers):
            if not used[index]:
                used[index] = True
                build(current + digit)
                used[index] = False

    build("")
    maximum = max(made, default=0)
    prime = bytearray(b"\x01") * (maximum + 1)
    if maximum >= 0:
        prime[0] = 0
    if maximum >= 1:
        prime[1] = 0
    for value in range(2, math.isqrt(maximum) + 1):
        if prime[value]:
            start = value * value
            prime[start : maximum + 1 : value] = b"\x00" * (((maximum - start) // value) + 1)
    return sum(prime[value] for value in made)


@register(42840, "recommended", "수포자별 주기 패턴을 나머지 인덱스로 비교", "O(n) time, O(1) extra space")
def p42840_recommended(answers):
    patterns = (
        (1, 2, 3, 4, 5),
        (2, 1, 2, 3, 2, 4, 2, 5),
        (3, 3, 1, 1, 2, 2, 4, 4, 5, 5),
    )
    scores = [
        sum(answer == pattern[index % len(pattern)] for index, answer in enumerate(answers))
        for pattern in patterns
    ]
    best = max(scores)
    return [index + 1 for index, score in enumerate(scores) if score == best]


@register(42840, "alternative", "정답을 한 번 순회하며 세 패턴 점수를 동시에 누적", "O(n) time, O(1) space")
def p42840_alternative(answers):
    patterns = [[1, 2, 3, 4, 5], [2, 1, 2, 3, 2, 4, 2, 5], [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]]
    scores = [0, 0, 0]
    for index, answer in enumerate(answers):
        for student, pattern in enumerate(patterns):
            scores[student] += pattern[index % len(pattern)] == answer
    return [student + 1 for student, score in enumerate(scores) if score == max(scores)]


@register(42842, "recommended", "전체 격자의 약수 쌍에서 테두리 조건 확인", "O(sqrt(area)) time, O(1) space")
def p42842_recommended(brown, yellow):
    area = brown + yellow
    for height in range(3, math.isqrt(area) + 1):
        if area % height == 0:
            width = area // height
            if (width - 2) * (height - 2) == yellow:
                return [width, height]


@register(42842, "alternative", "노란 내부 높이를 늘리며 가로 길이 계산", "O(sqrt(yellow)) time, O(1) space")
def p42842_alternative(brown, yellow):
    for inner_height in range(1, math.isqrt(yellow) + 1):
        if yellow % inner_height == 0:
            inner_width = yellow // inner_height
            width, height = inner_width + 2, inner_height + 2
            if 2 * width + 2 * height - 4 == brown:
                return [width, height]


@register(84512, "recommended", "각 자리의 사전순 가중치로 순번을 바로 계산", "O(5) time, O(1) space")
def p84512_recommended(word):
    # 한 글자 아래에는 1+5+25+125+625개 단어가 연속해서 놓인다.
    weights = [781, 156, 31, 6, 1]
    order = {letter: index for index, letter in enumerate("AEIOU")}
    return sum(order[letter] * weights[index] + 1 for index, letter in enumerate(word))


@register(84512, "alternative", "길이 1..5의 모든 단어를 생성해 사전순 위치 탐색", "O(5^5 log 5^5) time, O(5^5) space", "전체 단어가 3,905개뿐인 제한을 이용")
def p84512_alternative(word):
    alphabet = "AEIOU"
    words = []
    for length in range(1, 6):
        words.extend("".join(letters) for letters in product(alphabet, repeat=length))
    words.sort()
    return words.index(word) + 1


@register(86491, "recommended", "각 명함의 긴 변과 짧은 변을 같은 축으로 정렬", "O(n) time, O(1) space")
def p86491_recommended(sizes):
    long_side = max(max(width, height) for width, height in sizes)
    short_side = max(min(width, height) for width, height in sizes)
    return long_side * short_side


@register(86491, "alternative", "필요할 때만 명함을 회전하며 지갑 치수 갱신", "O(n) time, O(1) space")
def p86491_alternative(sizes):
    wallet_width = wallet_height = 0
    for width, height in sizes:
        if width < height:
            width, height = height, width
        wallet_width = max(wallet_width, width)
        wallet_height = max(wallet_height, height)
    return wallet_width * wallet_height


@register(86971, "recommended", "간선을 하나씩 끊고 BFS로 한쪽 송전탑 수 계산", "O(n^2) time, O(n) space")
def p86971_recommended(n, wires):
    answer = n
    for removed, _ in enumerate(wires):
        graph = [[] for _ in range(n + 1)]
        for index, (left, right) in enumerate(wires):
            if index != removed:
                graph[left].append(right)
                graph[right].append(left)
        seen = {1}
        queue = deque([1])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        answer = min(answer, abs(n - 2 * len(seen)))
    return answer


@register(86971, "alternative", "트리를 한 번 순회해 각 자식 서브트리 크기 계산", "O(n) time, O(n) space")
def p86971_alternative(n, wires):
    graph = [[] for _ in range(n + 1)]
    for left, right in wires:
        graph[left].append(right)
        graph[right].append(left)

    answer = n

    def subtree(node, parent):
        nonlocal answer
        size = 1
        for neighbor in graph[node]:
            if neighbor != parent:
                size += subtree(neighbor, node)
        # 부모와 연결된 간선을 자르면 size 대 n-size로 나뉜다.
        if parent:
            answer = min(answer, abs(n - 2 * size))
        return size

    subtree(1, 0)
    return answer


@register(87946, "recommended", "방문 배열을 되돌리는 DFS로 가능한 순서 탐색", "O(n!) time, O(n) space")
def p87946_recommended(k, dungeons):
    visited = [False] * len(dungeons)
    best = 0

    def explore(fatigue, count):
        nonlocal best
        best = max(best, count)
        for index, (required, cost) in enumerate(dungeons):
            if not visited[index] and fatigue >= required:
                visited[index] = True
                explore(fatigue - cost, count + 1)
                visited[index] = False

    explore(k, 0)
    return best


@register(87946, "alternative", "던전 순열을 만들고 각 순서의 실행 가능 접두부 측정", "O(n!*n) time, O(n) space", "n<=8이므로 전 순열 탐색 가능")
def p87946_alternative(k, dungeons):
    best = 0
    for order in permutations(dungeons):
        fatigue = k
        cleared = 0
        for required, cost in order:
            if fatigue < required:
                break
            fatigue -= cost
            cleared += 1
        best = max(best, cleared)
    return best


# ---------------------------------------------------------------------------
# 06 탐욕법
# ---------------------------------------------------------------------------


@register(135808, "recommended", "점수를 내림차순 정렬해 상자별 최솟값 선택", "O(n log n) time, O(n) space")
def p135808_recommended(k, m, score):
    ordered = sorted(score, reverse=True)
    # 완성된 각 묶음의 마지막 원소가 그 상자의 최저 점수다.
    return sum(ordered[index] * m for index in range(m - 1, len(ordered), m))


@register(135808, "alternative", "1..k 점수 빈도로 높은 점수부터 상자 채우기", "O(n+k) time, O(k) space")
def p135808_alternative(k, m, score):
    counts = Counter(score)
    filled = answer = 0
    for value in range(k, 0, -1):
        for _ in range(counts[value]):
            filled += 1
            if filled == m:
                answer += value * m
                filled = 0
    return answer


@register(42860, "recommended", "상하 이동 합과 연속 A 구간별 최소 좌우 이동 결합", "O(n^2) time, O(1) space")
def p42860_recommended(name):
    vertical = sum(min(ord(char) - ord("A"), ord("Z") - ord(char) + 1) for char in name)
    horizontal = len(name) - 1
    for index in range(len(name)):
        next_index = index + 1
        while next_index < len(name) and name[next_index] == "A":
            next_index += 1
        # 오른쪽으로 갔다 돌아오기 / 왼쪽으로 먼저 갔다 돌아오기 중 작은 값.
        horizontal = min(
            horizontal,
            2 * index + len(name) - next_index,
            index + 2 * (len(name) - next_index),
        )
    return vertical + horizontal


@register(42860, "alternative", "바꿔야 할 위치 사이의 가장 긴 미방문 A 구간을 조사", "O(n^2) time, O(1) space")
def p42860_alternative(name):
    change = sum(min(ord(char) - 65, 91 - ord(char)) for char in name)
    move = max(0, len(name) - 1)
    for left in range(len(name)):
        right = left + 1
        while right < len(name) and name[right] == "A":
            right += 1
        tail = len(name) - right
        move = min(move, left * 2 + tail, left + tail * 2)
    return change + move


@register(42861, "recommended", "비용순 간선과 Union-Find를 쓰는 Kruskal MST", "O(e log e) time, O(n) space")
def p42861_recommended(n, costs):
    parent = list(range(n))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    total = selected = 0
    for left, right, cost in sorted(costs, key=lambda edge: edge[2]):
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            continue
        parent[root_right] = root_left
        total += cost
        selected += 1
        if selected == n - 1:
            break
    return total


@register(42861, "alternative", "현재 트리와 연결되는 최소 간선을 고르는 Prim MST", "O(e log e) time, O(n+e) space")
def p42861_alternative(n, costs):
    graph = [[] for _ in range(n)]
    for left, right, cost in costs:
        graph[left].append((cost, right))
        graph[right].append((cost, left))
    visited = [False] * n
    heap = [(0, 0)]
    total = count = 0
    while heap and count < n:
        cost, node = heapq.heappop(heap)
        if visited[node]:
            continue
        visited[node] = True
        total += cost
        count += 1
        for next_cost, neighbor in graph[node]:
            if not visited[neighbor]:
                heapq.heappush(heap, (next_cost, neighbor))
    return total


@register(42862, "recommended", "중복 상태 정리 후 앞번호부터 왼쪽 이웃 우선 대여", "O(n) time, O(n) space")
def p42862_recommended(n, lost, reserve):
    lost_set = set(lost) - set(reserve)
    reserve_set = set(reserve) - set(lost)
    for student in sorted(lost_set):
        for lender in (student - 1, student + 1):
            if lender in reserve_set:
                reserve_set.remove(lender)
                lost_set.remove(student)
                break
    return n - len(lost_set)


@register(42862, "alternative", "학생별 체육복 수 배열에서 왼쪽부터 부족분 전달", "O(n) time, O(n) space")
def p42862_alternative(n, lost, reserve):
    clothes = [1] * (n + 2)
    for student in lost:
        clothes[student] -= 1
    for student in reserve:
        clothes[student] += 1
    for student in range(1, n + 1):
        if clothes[student] == 0 and clothes[student - 1] == 2:
            clothes[student - 1] -= 1
            clothes[student] += 1
        elif clothes[student] == 0 and clothes[student + 1] == 2:
            clothes[student + 1] -= 1
            clothes[student] += 1
    return sum(clothes[student] >= 1 for student in range(1, n + 1))


@register(42883, "recommended", "작은 앞자리 숫자를 제거하는 단조 감소 스택", "O(n) time, O(n) space")
def p42883_recommended(number, k):
    stack = []
    removals = k
    for digit in number:
        while removals and stack and stack[-1] < digit:
            stack.pop()
            removals -= 1
        stack.append(digit)
    if removals:
        del stack[-removals:]
    return "".join(stack)


@register(42883, "alternative", "고정 배열과 top 포인터로 단조 스택 구현", "O(n) time, O(n) space")
def p42883_alternative(number, k):
    buffer = [""] * len(number)
    top = 0
    removals = k
    for digit in number:
        while removals and top and buffer[top - 1] < digit:
            top -= 1
            removals -= 1
        buffer[top] = digit
        top += 1
    return "".join(buffer[: top - removals])


@register(42884, "recommended", "진출 지점이 빠른 차량부터 그 지점에 카메라 설치", "O(n log n) time, O(1) extra space")
def p42884_recommended(routes):
    cameras = 0
    last_camera = -math.inf
    for entry, exit_point in sorted(routes, key=lambda route: route[1]):
        if last_camera < entry:
            last_camera = exit_point
            cameras += 1
    return cameras


@register(42884, "alternative", "겹치는 차량 구간의 교집합을 유지", "O(n log n) time, O(1) extra space")
def p42884_alternative(routes):
    ordered = sorted(routes)
    cameras = 1
    intersection_end = ordered[0][1]
    for entry, exit_point in ordered[1:]:
        if entry > intersection_end:
            cameras += 1
            intersection_end = exit_point
        else:
            intersection_end = min(intersection_end, exit_point)
    return cameras


@register(42885, "recommended", "가벼운 사람과 무거운 사람을 투 포인터로 짝지음", "O(n log n) time, O(n) space")
def p42885_recommended(people, limit):
    ordered = sorted(people)
    light, heavy = 0, len(ordered) - 1
    boats = 0
    while light <= heavy:
        if light < heavy and ordered[light] + ordered[heavy] <= limit:
            light += 1
        heavy -= 1
        boats += 1
    return boats


@register(42885, "alternative", "정렬 덱의 양끝에서 탑승자를 꺼냄", "O(n log n) time, O(n) space")
def p42885_alternative(people, limit):
    queue = deque(sorted(people))
    boats = 0
    while queue:
        heaviest = queue.pop()
        if queue and queue[0] + heaviest <= limit:
            queue.popleft()
        boats += 1
    return boats


# ---------------------------------------------------------------------------
# 07 동적계획법
# ---------------------------------------------------------------------------


@register(1843, "recommended", "구간별 최솟값·최댓값을 함께 저장하는 구간 DP", "O(n^3) time, O(n^2) space")
def p1843_recommended(arr):
    numbers = list(map(int, arr[::2]))
    operators = arr[1::2]
    count = len(numbers)
    minimum = [[math.inf] * count for _ in range(count)]
    maximum = [[-math.inf] * count for _ in range(count)]
    for index, value in enumerate(numbers):
        minimum[index][index] = maximum[index][index] = value

    for length in range(2, count + 1):
        for left in range(count - length + 1):
            right = left + length - 1
            for split in range(left, right):
                if operators[split] == "+":
                    candidates = (
                        minimum[left][split] + minimum[split + 1][right],
                        maximum[left][split] + maximum[split + 1][right],
                    )
                else:
                    # 뺄셈의 최대는 왼쪽 최대 - 오른쪽 최소다.
                    candidates = (
                        minimum[left][split] - maximum[split + 1][right],
                        maximum[left][split] - minimum[split + 1][right],
                    )
                minimum[left][right] = min(minimum[left][right], *candidates)
                maximum[left][right] = max(maximum[left][right], *candidates)
    return maximum[0][count - 1]


@register(1843, "alternative", "구간의 최솟값·최댓값을 재귀 메모이제이션", "O(n^3) time, O(n^2) space")
def p1843_alternative(arr):
    numbers = tuple(map(int, arr[::2]))
    operators = arr[1::2]

    @lru_cache(None)
    def bounds(left, right):
        if left == right:
            return numbers[left], numbers[left]
        low, high = math.inf, -math.inf
        for split in range(left, right):
            left_low, left_high = bounds(left, split)
            right_low, right_high = bounds(split + 1, right)
            if operators[split] == "+":
                values = (left_low + right_low, left_high + right_high)
            else:
                values = (left_low - right_high, left_high - right_low)
            low, high = min(low, *values), max(high, *values)
        return low, high

    return bounds(0, len(numbers) - 1)[1]


@register(340198, "recommended", "빈 칸으로 끝나는 최대 정사각형 DP 후 돗자리 선택", "O(h*w + m log m) time, O(w) space")
def p340198_recommended(mats, park):
    width = len(park[0])
    previous = [0] * (width + 1)
    largest = 0
    for row in park:
        current = [0] * (width + 1)
        for column, value in enumerate(row, 1):
            if value == "-1":
                current[column] = 1 + min(
                    current[column - 1], previous[column], previous[column - 1]
                )
                largest = max(largest, current[column])
        previous = current
    possible = [size for size in mats if size <= largest]
    return max(possible, default=-1)


@register(340198, "alternative", "2차원 누적합으로 큰 돗자리부터 빈 영역 탐색", "O(h*w + m*h*w) time, O(h*w) space", "돗자리 종류가 10개 이하인 제한을 이용")
def p340198_alternative(mats, park):
    height, width = len(park), len(park[0])
    occupied = [[0] * (width + 1) for _ in range(height + 1)]
    for row in range(height):
        for column in range(width):
            occupied[row + 1][column + 1] = (
                occupied[row][column + 1]
                + occupied[row + 1][column]
                - occupied[row][column]
                + (park[row][column] != "-1")
            )
    for size in sorted(mats, reverse=True):
        for bottom in range(size, height + 1):
            for right in range(size, width + 1):
                people = (
                    occupied[bottom][right]
                    - occupied[bottom - size][right]
                    - occupied[bottom][right - size]
                    + occupied[bottom - size][right - size]
                )
                if people == 0:
                    return size
    return -1


@register(42895, "recommended", "사용 횟수별 만들 수 있는 수의 집합 DP", "O(8^3*S^2) worst time, O(8*S) space")
def p42895_recommended(N, number):
    possible = [set() for _ in range(9)]
    for count in range(1, 9):
        possible[count].add(int(str(N) * count))
        for left_count in range(1, count):
            right_count = count - left_count
            for left in possible[left_count]:
                for right in possible[right_count]:
                    possible[count].update((left + right, left - right, left * right))
                    if right:
                        possible[count].add(left // right)
        if number in possible[count]:
            return count
    return -1


@register(42895, "alternative", "필요 개수 집합을 재귀적으로 조합해 메모이제이션", "O(8^3*S^2) worst time, O(8*S) space")
def p42895_alternative(N, number):
    @lru_cache(None)
    def values(count):
        result = {int(str(N) * count)}
        for left_count in range(1, count):
            for left in values(left_count):
                for right in values(count - left_count):
                    result |= {left + right, left - right, left * right}
                    if right:
                        result.add(left // right)
        return result

    for count in range(1, 9):
        if number in values(count):
            return count
    return -1


@register(42897, "recommended", "첫 집 포함/제외를 나눠 선형 도둑질 DP 두 번", "O(n) time, O(1) extra space")
def p42897_recommended(money):
    def rob(values):
        two_back = one_back = 0
        for value in values:
            two_back, one_back = one_back, max(one_back, two_back + value)
        return one_back

    # 원형에서는 첫 집과 마지막 집을 동시에 고를 수 없다.
    return max(rob(money[:-1]), rob(money[1:]))


@register(42897, "alternative", "첫 집을 고르는 경우와 버리는 경우의 DP 배열", "O(n) time, O(n) space")
def p42897_alternative(money):
    if len(money) <= 3:
        return max(money)

    def table(values):
        dp = [0] * (len(values) + 1)
        dp[1] = values[0]
        for index in range(2, len(values) + 1):
            dp[index] = max(dp[index - 1], dp[index - 2] + values[index - 1])
        return dp[-1]

    return max(table(money[:-1]), table(money[1:]))


@register(42898, "recommended", "행을 순회하며 왼쪽·위쪽 경로 수를 1차원 DP에 누적", "O(m*n) time, O(m) space")
def p42898_recommended(m, n, puddles):
    blocked = {(column, row) for column, row in puddles}
    ways = [0] * (m + 1)
    ways[1] = 1
    for row in range(1, n + 1):
        for column in range(1, m + 1):
            if (column, row) in blocked:
                ways[column] = 0
            elif column > 1:
                ways[column] = (ways[column] + ways[column - 1]) % 1_000_000_007
    return ways[m]


@register(42898, "alternative", "격자 모양 2차원 DP로 경로 수 계산", "O(m*n) time, O(m*n) space")
def p42898_alternative(m, n, puddles):
    blocked = {tuple(point) for point in puddles}
    ways = [[0] * (m + 1) for _ in range(n + 1)]
    ways[1][1] = 1
    for row in range(1, n + 1):
        for column in range(1, m + 1):
            if (column, row) in blocked:
                ways[row][column] = 0
            elif (column, row) != (1, 1):
                ways[row][column] = (ways[row - 1][column] + ways[row][column - 1]) % 1_000_000_007
    return ways[n][m]


@register(43105, "recommended", "아래 행에서 위로 올라오며 최선의 자식 합 선택", "O(n^2) time, O(n^2) space")
def p43105_recommended(triangle):
    best = [row[:] for row in triangle]
    for row in range(len(best) - 2, -1, -1):
        for column in range(len(best[row])):
            best[row][column] += max(best[row + 1][column], best[row + 1][column + 1])
    return best[0][0]


@register(43105, "alternative", "꼭대기에서 각 칸까지 최대 합을 한 행씩 갱신", "O(n^2) time, O(n) space")
def p43105_alternative(triangle):
    previous = [triangle[0][0]]
    for row in triangle[1:]:
        current = [0] * len(row)
        for column, value in enumerate(row):
            left_parent = previous[column - 1] if column > 0 else -math.inf
            right_parent = previous[column] if column < len(previous) else -math.inf
            current[column] = value + max(left_parent, right_parent)
        previous = current
    return max(previous)


# ---------------------------------------------------------------------------
# 08 깊이/너비 우선 탐색
# ---------------------------------------------------------------------------


@register(172928, "recommended", "명령마다 경로 전체의 경계와 장애물을 확인한 뒤 이동", "O(routes*distance) time, O(1) space")
def p172928_recommended(park, routes):
    height, width = len(park), len(park[0])
    for row in range(height):
        for column in range(width):
            if park[row][column] == "S":
                current_row, current_column = row, column
    direction = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
    for route in routes:
        command, raw_distance = route.split()
        distance = int(raw_distance)
        dr, dc = direction[command]
        path = [
            (current_row + dr * step, current_column + dc * step)
            for step in range(1, distance + 1)
        ]
        if all(0 <= row < height and 0 <= column < width and park[row][column] != "X" for row, column in path):
            current_row, current_column = path[-1]
    return [current_row, current_column]


@register(172928, "alternative", "후보 도착점까지 한 칸씩 검사하고 실패 시 원위치", "O(routes*distance) time, O(1) space")
def p172928_alternative(park, routes):
    height, width = len(park), len(park[0])
    start = next((row, line.index("S")) for row, line in enumerate(park) if "S" in line)
    row, column = start
    moves = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
    for route in routes:
        command, distance = route.split()
        dr, dc = moves[command]
        candidate_row, candidate_column = row, column
        valid = True
        for _ in range(int(distance)):
            candidate_row += dr
            candidate_column += dc
            if not (0 <= candidate_row < height and 0 <= candidate_column < width) or park[candidate_row][candidate_column] == "X":
                valid = False
                break
        if valid:
            row, column = candidate_row, candidate_column
    return [row, column]


@register(1844, "recommended", "시작점부터 레벨 순서 BFS로 최단거리 탐색", "O(n*m) time, O(n*m) space")
def p1844_recommended(maps):
    height, width = len(maps), len(maps[0])
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        row, column, distance = queue.popleft()
        if (row, column) == (height - 1, width - 1):
            return distance
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row, next_column = row + dr, column + dc
            if 0 <= next_row < height and 0 <= next_column < width and maps[next_row][next_column] == 1 and (next_row, next_column) not in visited:
                visited.add((next_row, next_column))
                queue.append((next_row, next_column, distance + 1))
    return -1


@register(1844, "alternative", "거리 배열을 방문 표시로 겸용하는 BFS", "O(n*m) time, O(n*m) space")
def p1844_alternative(maps):
    height, width = len(maps), len(maps[0])
    distance = [[-1] * width for _ in range(height)]
    distance[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        row, column = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row, next_column = row + dr, column + dc
            if 0 <= next_row < height and 0 <= next_column < width and maps[next_row][next_column] and distance[next_row][next_column] == -1:
                distance[next_row][next_column] = distance[row][column] + 1
                queue.append((next_row, next_column))
    return distance[-1][-1]


@register(43162, "recommended", "방문하지 않은 컴퓨터마다 DFS를 시작해 연결요소 계산", "O(n^2) time, O(n) space")
def p43162_recommended(n, computers):
    visited = [False] * n
    networks = 0
    for start in range(n):
        if visited[start]:
            continue
        networks += 1
        stack = [start]
        visited[start] = True
        while stack:
            node = stack.pop()
            for neighbor, connected in enumerate(computers[node]):
                if connected and not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
    return networks


@register(43162, "alternative", "연결 행렬의 간선을 Union-Find로 병합", "O(n^2 alpha(n)) time, O(n) space")
def p43162_alternative(n, computers):
    parent = list(range(n))

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    for left in range(n):
        for right in range(left + 1, n):
            if computers[left][right]:
                root_left, root_right = find(left), find(right)
                if root_left != root_right:
                    parent[root_right] = root_left
    return len({find(node) for node in range(n)})


@register(43163, "recommended", "한 글자 차이인 단어를 BFS로 탐색", "O(n^2*L) time, O(n) space")
def p43163_recommended(begin, target, words):
    if target not in words:
        return 0
    queue = deque([(begin, 0)])
    visited = set()
    while queue:
        current, steps = queue.popleft()
        if current == target:
            return steps
        for index, word in enumerate(words):
            if index not in visited and sum(left != right for left, right in zip(current, word)) == 1:
                visited.add(index)
                queue.append((word, steps + 1))
    return 0


@register(43163, "alternative", "단어 그래프를 미리 만든 뒤 최단거리 BFS", "O(n^2*L) time, O(n^2) space")
def p43163_alternative(begin, target, words):
    vocabulary = [begin] + list(words)
    if target not in vocabulary:
        return 0
    graph = [[] for _ in vocabulary]
    for left in range(len(vocabulary)):
        for right in range(left + 1, len(vocabulary)):
            if sum(a != b for a, b in zip(vocabulary[left], vocabulary[right])) == 1:
                graph[left].append(right)
                graph[right].append(left)
    queue = deque([(0, 0)])
    visited = {0}
    while queue:
        node, distance = queue.popleft()
        if vocabulary[node] == target:
            return distance
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return 0


@register(43164, "recommended", "도착지를 최소 힙으로 관리하는 Hierholzer 오일러 경로", "O(e log e) time, O(e) space")
def p43164_recommended(tickets):
    graph = defaultdict(list)
    for departure, arrival in tickets:
        heapq.heappush(graph[departure], arrival)
    stack = ["ICN"]
    route = []
    while stack:
        airport = stack[-1]
        if graph[airport]:
            stack.append(heapq.heappop(graph[airport]))
        else:
            route.append(stack.pop())
    return route[::-1]


@register(43164, "alternative", "도착지를 역정렬한 스택으로 관리하는 Hierholzer 경로", "O(e log e) time, O(e) space")
def p43164_alternative(tickets):
    graph = defaultdict(list)
    for departure, arrival in sorted(tickets, reverse=True):
        graph[departure].append(arrival)
    path, route = ["ICN"], []
    while path:
        while graph[path[-1]]:
            path.append(graph[path[-1]].pop())
        route.append(path.pop())
    return route[::-1]


@register(43165, "recommended", "현재 합별 경우의 수를 Counter로 압축", "O(n*S) time, O(S) space")
def p43165_recommended(numbers, target):
    states = Counter({0: 1})
    for number in numbers:
        next_states = Counter()
        for total, count in states.items():
            next_states[total + number] += count
            next_states[total - number] += count
        states = next_states
    return states[target]


@register(43165, "alternative", "각 수에 +와 -를 붙이는 재귀 DFS", "O(2^n) time, O(n) space")
def p43165_alternative(numbers, target):
    answer = 0

    def search(index, total):
        nonlocal answer
        if index == len(numbers):
            answer += total == target
            return
        search(index + 1, total + numbers[index])
        search(index + 1, total - numbers[index])

    search(0, 0)
    return answer


@register(84021, "recommended", "빈칸/조각 컴포넌트를 추출하고 회전 정규화해 매칭", "O(n^2) time, O(n^2) space")
def p84021_recommended(game_board, table):
    def components(board, target):
        size = len(board)
        visited = [[False] * size for _ in range(size)]
        result = []
        for start_row in range(size):
            for start_column in range(size):
                if visited[start_row][start_column] or board[start_row][start_column] != target:
                    continue
                queue = deque([(start_row, start_column)])
                visited[start_row][start_column] = True
                cells = []
                while queue:
                    row, column = queue.popleft()
                    cells.append((row, column))
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        next_row, next_column = row + dr, column + dc
                        if 0 <= next_row < size and 0 <= next_column < size and not visited[next_row][next_column] and board[next_row][next_column] == target:
                            visited[next_row][next_column] = True
                            queue.append((next_row, next_column))
                result.append(cells)
        return result

    def normalize(cells):
        min_row = min(row for row, _ in cells)
        min_column = min(column for _, column in cells)
        return tuple(sorted((row - min_row, column - min_column) for row, column in cells))

    def rotations(cells):
        current = list(cells)
        result = []
        for _ in range(4):
            normalized = normalize(current)
            result.append(normalized)
            # (행, 열) -> (열, -행)은 원점 기준 90도 회전이다.
            current = [(column, -row) for row, column in normalized]
        return result

    pieces = Counter()
    for piece in components(table, 1):
        # 네 회전의 사전순 최솟값을 택하면 시작 방향과 무관한 표준 키가 된다.
        pieces[min(rotations(piece))] += 1
    answer = 0
    for hole in components(game_board, 0):
        key = min(rotations(hole))
        if pieces[key]:
            pieces[key] -= 1
            answer += len(hole)
    return answer


@register(84021, "alternative", "각 도형의 네 회전 중 사전순 최소 좌표를 표준 모양으로 사용", "O(n^2) time, O(n^2) space")
def p84021_alternative(game_board, table):
    def extract(board, value):
        size = len(board)
        seen = set()
        shapes = []
        for row in range(size):
            for column in range(size):
                if board[row][column] != value or (row, column) in seen:
                    continue
                shape = []
                stack = [(row, column)]
                seen.add((row, column))
                while stack:
                    cell = stack.pop()
                    shape.append(cell)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        neighbor = (cell[0] + dr, cell[1] + dc)
                        if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size and board[neighbor[0]][neighbor[1]] == value and neighbor not in seen:
                            seen.add(neighbor)
                            stack.append(neighbor)
                shapes.append(shape)
        return shapes

    def shifted(shape):
        top = min(row for row, _ in shape)
        left = min(column for _, column in shape)
        return tuple(sorted((row - top, column - left) for row, column in shape))

    def canonical(shape):
        forms = []
        current = shape
        for _ in range(4):
            form = shifted(current)
            forms.append(form)
            # 회전 뒤 shifted를 다시 적용하므로 음수 좌표도 같은 원점으로 정렬된다.
            current = [(column, -row) for row, column in form]
        return min(forms)

    available = Counter(canonical(shape) for shape in extract(table, 1))
    filled = 0
    for hole in extract(game_board, 0):
        shape = canonical(hole)
        if available[shape]:
            available[shape] -= 1
            filled += len(hole)
    return filled


@register(87694, "recommended", "좌표를 2배 확대해 사각형 테두리만 남긴 뒤 BFS", "O(C^2) time, O(C^2) space")
def p87694_recommended(rectangle, characterX, characterY, itemX, itemY):
    grid = [[0] * 102 for _ in range(102)]
    for x1, y1, x2, y2 in rectangle:
        x1, y1, x2, y2 = 2 * x1, 2 * y1, 2 * x2, 2 * y2
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if x1 < x < x2 and y1 < y < y2:
                    grid[x][y] = 2  # 내부는 이후 다른 사각형의 변도 지나갈 수 없다.
                elif grid[x][y] != 2:
                    grid[x][y] = 1
    start = (2 * characterX, 2 * characterY)
    target = (2 * itemX, 2 * itemY)
    queue = deque([(start[0], start[1], 0)])
    visited = {start}
    while queue:
        x, y, distance = queue.popleft()
        if (x, y) == target:
            return distance // 2
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_point = (x + dx, y + dy)
            if grid[next_point[0]][next_point[1]] == 1 and next_point not in visited:
                visited.add(next_point)
                queue.append((next_point[0], next_point[1], distance + 1))


@register(87694, "alternative", "각 격자점이 합성 도형의 외곽선인지 직접 판정 후 BFS", "O(C^2*r) time, O(C^2) space")
def p87694_alternative(rectangle, characterX, characterY, itemX, itemY):
    doubled = [[2 * value for value in rect] for rect in rectangle]

    def boundary(x, y):
        on_edge = any(
            x1 <= x <= x2 and y1 <= y <= y2 and (x in (x1, x2) or y in (y1, y2))
            for x1, y1, x2, y2 in doubled
        )
        inside = any(x1 < x < x2 and y1 < y < y2 for x1, y1, x2, y2 in doubled)
        return on_edge and not inside

    start = (2 * characterX, 2 * characterY)
    target = (2 * itemX, 2 * itemY)
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (x, y), distance = queue.popleft()
        if (x, y) == target:
            return distance // 2
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_point = (x + dx, y + dy)
            if 0 <= next_point[0] <= 100 and 0 <= next_point[1] <= 100 and next_point not in visited and boundary(*next_point):
                visited.add(next_point)
                queue.append((next_point, distance + 1))


# ---------------------------------------------------------------------------
# 09 이분탐색
# ---------------------------------------------------------------------------


@register(12982, "recommended", "신청 금액을 작은 순서로 더해 예산 내 부서 수 최대화", "O(n log n) time, O(n) space")
def p12982_recommended(d, budget):
    supported = 0
    for request in sorted(d):
        if request > budget:
            break
        budget -= request
        supported += 1
    return supported


@register(12982, "alternative", "정렬한 금액의 누적합에서 예산의 삽입 위치 탐색", "O(n log n) time, O(n) space")
def p12982_alternative(d, budget):
    totals = []
    running = 0
    for request in sorted(d):
        running += request
        totals.append(running)
    return bisect_left(totals, budget + 1)


@register(43236, "recommended", "최소 거리의 가능 여부를 판정하는 매개변수 이분탐색", "O(n log distance) time, O(n) space")
def p43236_recommended(distance, rocks, n):
    positions = sorted(rocks) + [distance]

    def can_keep(minimum_gap):
        removed = 0
        previous = 0
        for position in positions:
            if position - previous < minimum_gap:
                removed += 1
            else:
                previous = position
        return removed <= n

    low, high = 0, distance + 1  # low는 가능, high는 불가능
    while low + 1 < high:
        middle = (low + high) // 2
        if can_keep(middle):
            low = middle
        else:
            high = middle
    return low


@register(43236, "alternative", "제거 횟수를 직접 세며 가능한 거리의 최댓값 저장", "O(n log distance) time, O(n) space")
def p43236_alternative(distance, rocks, n):
    ordered = [0] + sorted(rocks) + [distance]
    left, right = 1, distance
    answer = 0
    while left <= right:
        gap = (left + right) // 2
        removals = 0
        last = ordered[0]
        for position in ordered[1:]:
            if position - last < gap:
                removals += 1
            else:
                last = position
        if removals <= n:
            answer = gap
            left = gap + 1
        else:
            right = gap - 1
    return answer


@register(43238, "recommended", "주어진 시간에 처리 가능한 사람 수로 최소 시간 이분탐색", "O(k log answer) time, O(1) space")
def p43238_recommended(n, times):
    low, high = 0, min(times) * n
    while low + 1 < high:
        middle = (low + high) // 2
        processed = sum(middle // duration for duration in times)
        if processed >= n:
            high = middle
        else:
            low = middle
    return high


@register(43238, "alternative", "첫 가능 시간을 찾는 닫힌 구간 이분탐색", "O(k log answer) time, O(1) space")
def p43238_alternative(n, times):
    left, right = 1, max(times) * n
    answer = right
    while left <= right:
        middle = (left + right) // 2
        if sum(middle // duration for duration in times) >= n:
            answer = middle
            right = middle - 1
        else:
            left = middle + 1
    return answer


# ---------------------------------------------------------------------------
# 10 그래프
# ---------------------------------------------------------------------------


@register(49189, "recommended", "1번 노드부터 BFS 거리 계산 후 최댓값 빈도 집계", "O(n+e) time, O(n+e) space")
def p49189_recommended(n, edge):
    graph = [[] for _ in range(n + 1)]
    for left, right in edge:
        graph[left].append(right)
        graph[right].append(left)
    distance = [-1] * (n + 1)
    distance[1] = 0
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    farthest = max(distance)
    return distance.count(farthest)


@register(49189, "alternative", "BFS의 현재 레이어 집합을 교체하며 마지막 레이어 크기 반환", "O(n+e) time, O(n+e) space")
def p49189_alternative(n, edge):
    graph = defaultdict(set)
    for left, right in edge:
        graph[left].add(right)
        graph[right].add(left)
    visited = {1}
    layer = {1}
    while layer:
        next_layer = set()
        for node in layer:
            next_layer.update(graph[node] - visited)
        if not next_layer:
            return len(layer)
        visited.update(next_layer)
        layer = next_layer


@register(49190, "recommended", "대각선 교차를 잡도록 이동을 2분할하고 새 간선의 재방문 정점 집계", "O(a) time, O(a) space")
def p49190_recommended(arrows):
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    point = (0, 0)
    vertices = {point}
    edges = set()
    rooms = 0
    for arrow in arrows:
        dx, dy = directions[arrow]
        for _ in range(2):
            next_point = (point[0] + dx, point[1] + dy)
            edge_key = (point, next_point)
            reverse_key = (next_point, point)
            if next_point in vertices and edge_key not in edges:
                rooms += 1
            vertices.add(next_point)
            edges.add(edge_key)
            edges.add(reverse_key)
            point = next_point
    return rooms


@register(49190, "alternative", "확대 경로 그래프의 V-E+F 관계로 방 개수 계산", "O(a) time, O(a) space")
def p49190_alternative(arrows):
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    current = (0, 0)
    vertices = {current}
    edges = set()
    for arrow in arrows:
        dx, dy = directions[arrow]
        for _ in range(2):
            neighbor = (current[0] + dx, current[1] + dy)
            vertices.add(neighbor)
            edges.add(frozenset((current, neighbor)))
            current = neighbor
    # 연결 평면 그래프에서 내부 면의 수 = E - V + 1.
    return len(edges) - len(vertices) + 1


@register(49191, "recommended", "Floyd-Warshall로 모든 승패 도달 관계 계산", "O(n^3) time, O(n^2) space")
def p49191_recommended(n, results):
    wins = [[False] * n for _ in range(n)]
    for winner, loser in results:
        wins[winner - 1][loser - 1] = True
    for middle in range(n):
        for winner in range(n):
            if wins[winner][middle]:
                for loser in range(n):
                    wins[winner][loser] |= wins[middle][loser]
    return sum(
        all(player == other or wins[player][other] or wins[other][player] for other in range(n))
        for player in range(n)
    )


@register(49191, "alternative", "각 선수에서 정방향·역방향 DFS로 비교 가능한 선수 집계", "O(n*(n+e)) time, O(n+e) space")
def p49191_alternative(n, results):
    defeated = [[] for _ in range(n + 1)]
    defeated_by = [[] for _ in range(n + 1)]
    for winner, loser in results:
        defeated[winner].append(loser)
        defeated_by[loser].append(winner)

    def reachable(start, graph):
        seen = set()
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return seen

    answer = 0
    for player in range(1, n + 1):
        known = reachable(player, defeated) | reachable(player, defeated_by)
        known.discard(player)  # 승패 순환이 있어도 자기 자신은 비교 대상이 아니다.
        answer += len(known) == n - 1
    return answer


@register(67256, "recommended", "키패드 좌표의 맨해튼 거리와 주손 우선순위 비교", "O(n) time, O(1) space")
def p67256_recommended(numbers, hand):
    coordinates = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2),
        "*": (3, 0), 0: (3, 1), "#": (3, 2),
    }
    left, right = "*", "#"
    answer = []
    for number in numbers:
        if number in (1, 4, 7):
            chosen = "L"
        elif number in (3, 6, 9):
            chosen = "R"
        else:
            target = coordinates[number]
            left_distance = sum(abs(a - b) for a, b in zip(coordinates[left], target))
            right_distance = sum(abs(a - b) for a, b in zip(coordinates[right], target))
            chosen = "L" if left_distance < right_distance or (left_distance == right_distance and hand == "left") else "R"
        answer.append(chosen)
        if chosen == "L":
            left = number
        else:
            right = number
    return "".join(answer)


@register(67256, "alternative", "키패드 인덱스의 행·열 차이로 거리 계산", "O(n) time, O(1) space")
def p67256_alternative(numbers, hand):
    # *, 0, #을 각각 10, 11, 12로 보면 3열 격자의 행/열 계산이 가능하다.
    def position(key):
        key = 11 if key == 0 else key
        return divmod(key - 1, 3)

    left, right = 10, 12
    preferred = "L" if hand == "left" else "R"
    answer = []
    for number in numbers:
        key = 11 if number == 0 else number
        if key % 3 == 1:
            press = "L"
        elif key % 3 == 0:
            press = "R"
        else:
            target = position(key)
            left_distance = sum(abs(a - b) for a, b in zip(position(left), target))
            right_distance = sum(abs(a - b) for a, b in zip(position(right), target))
            press = preferred if left_distance == right_distance else ("L" if left_distance < right_distance else "R")
        answer.append(press)
        if press == "L":
            left = key
        else:
            right = key
    return "".join(answer)


# ---------------------------------------------------------------------------
# 생성기
# ---------------------------------------------------------------------------


IMPORT_GROUPS = (
    ("collections", ("Counter", "defaultdict", "deque")),
    ("functools", ("cmp_to_key", "lru_cache")),
    ("itertools", ("combinations", "permutations", "product")),
    ("bisect", ("bisect_left", "insort")),
)


def standalone_imports(source: str) -> str:
    """풀이 함수가 실제로 참조하는 표준 라이브러리만 가져온다."""
    names = {
        node.id for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Name)
    }
    lines: list[str] = []
    for module, candidates in IMPORT_GROUPS:
        selected = [name for name in candidates if name in names]
        if selected:
            lines.append(f"from {module} import {', '.join(selected)}")
    for module in ("heapq", "math"):
        if module in names:
            lines.append(f"import {module}")
    return "\n".join(lines)


def inject_function_comments(source: str, entry: Entry) -> str:
    """템플릿 머리말 대신 실제 solution 함수 안에 문제별 사고 주석을 넣는다."""
    pedagogy = PEDAGOGY[entry.lesson_id]
    lines = source.splitlines()
    definition = next(
        index for index, line in enumerate(lines) if line.startswith("def solution(")
    )
    comments = [
        f"    # 이 구현의 선택: {entry.approach}",
        f"    # 상태 정의: {pedagogy.state}",
        f"    # 핵심 불변식: {pedagogy.invariant}",
    ]
    lines[definition + 1 : definition + 1] = comments
    return "\n".join(lines) + "\n"


def standalone_source(entry: Entry) -> str:
    source = textwrap.dedent(inspect.getsource(entry.function))
    # @register 호출은 한 줄일 수도 여러 줄일 수도 있으므로 실제 def부터 잘라낸다.
    source = source[source.index("def ") :]
    source = re.sub(
        rf"^def {re.escape(entry.function.__name__)}\(",
        "def solution(",
        source,
        count=1,
    )
    source = inject_function_comments(source, entry)
    if entry.variant == "recommended":
        provenance = "이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다."
    else:
        provenance = (
            "온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.\n"
            f"참고: https://school.programmers.co.kr/learn/courses/30/lessons/{entry.lesson_id}/questions\n"
            f"공개 풀이 모음: {SHARED_REFERENCE}"
        )
    header = f'''"""{entry.approach}.

복잡도: {entry.complexity}
{provenance}
"""

'''
    imports = standalone_imports(source)
    imports_block = imports + "\n\n" if imports else ""
    return header + imports_block + source


def render_hints(entry: Entry, category: str) -> str:
    pedagogy = PEDAGOGY[entry.lesson_id]
    pseudocode = "\n".join(
        f"{index}. {step}" for index, step in enumerate(pedagogy.steps, start=1)
    )
    return f"""# 단계별 힌트

한 번에 전부 열지 말고, 막힌 뒤 현재 단계 하나만 확인하세요.

<details>
<summary>1단계 — 복잡도 목표</summary>

- 유형: `{category}`
- 목표: `{entry.complexity}` 안에서 동작하는 구조를 찾으세요.

</details>

<details>
<summary>2단계 — 핵심 접근</summary>

`{entry.approach}` 방식을 검토하세요. 입력을 읽는 순간 무엇을 저장하고, 언제 답이
확정되는지 두 문장으로 먼저 적어 보세요.

</details>

<details>
<summary>3단계 — 상태·불변식</summary>

코드를 쓰기 전에 아래 두 문장을 자신의 말로 설명할 수 있는지 확인하세요.

- 상태 정의: {pedagogy.state}
- 핵심 불변식: {pedagogy.invariant}

</details>

<details>
<summary>4단계 — 구현 순서 의사코드</summary>

정답 코드는 노출하지 않습니다. 아래 순서만 보고 자신의 변수와 제어문으로 옮기세요.

{pseudocode}

</details>
"""


def render_sources(lesson_id: int) -> str:
    return f"""# 풀이 출처와 재작성 범위

이 폴더의 코드는 특정 온라인 정답 파일을 복사한 것이 아닙니다. 널리 알려진
알고리즘 발상을 참고하여 Python 함수로 독립 작성했습니다. 따라서 아래 링크는
아이디어 비교·추적용이며, 현재 코드의 원문 출처라고 주장하지 않습니다.

- 공식 문제: <https://school.programmers.co.kr/learn/courses/30/lessons/{lesson_id}>
- 문제별 풀이 Q&A: <https://school.programmers.co.kr/learn/courses/30/lessons/{lesson_id}/questions>
- 공개 풀이 데이터 스냅숏: <{SHARED_REFERENCE_DATA}>
- 스냅숏 commit: `{SHARED_REFERENCE_COMMIT}`
- 확인일: 2026-08-03

공개 스냅숏은 JavaScript 중심이며 일부 문제만 포함합니다. `alternative.py`는 그
파일의 번역본이나 사본이 아니라, 문제별로 흔한 다른 접근을 독립 재구현한 코드입니다.
"""


def render_readme(lesson_id: int, title: str, entries: list[Entry]) -> str:
    pedagogy = PEDAGOGY[lesson_id]
    rows = []
    for entry in entries:
        filename = f"{entry.variant}.py"
        label = "효율적인 권장 풀이" if entry.variant == "recommended" else "공개 풀이 접근(재작성)"
        note = (
            "실전 제출의 기준 풀이"
            if entry.variant == "recommended"
            else entry.note or "같은 문제를 다른 상태 표현으로 비교하는 풀이"
        )
        rows.append(
            f"| [{label}](./{filename}) | {entry.approach} | `{entry.complexity}` | {note} |"
        )
    return f"""# {title} — 예시 풀이

정답을 보기 전에 자신의 풀이를 완성하고, D+1 재풀이까지 끝낸 뒤 비교하는 것을
권장합니다. 아래 코드는 인터넷 코드를 그대로 복제하지 않고 공개적으로 널리 쓰이는
접근을 바탕으로 이 저장소를 위해 독립 작성했습니다.

| 파일 | 접근 | 복잡도 | 용도 |
|---|---|---|---|
{chr(10).join(rows)}

## 풀이별 해설

### `recommended.py` — 효율적인 권장 풀이

- 핵심 사고: {entries[0].approach}
- 복잡도: `{entries[0].complexity}`
- 용도: 문제 제한을 먼저 계산한 뒤 실전 제출 답안의 기준으로 삼습니다.
- 읽는 법: 코드 주석에서 핵심 상태와 목표 복잡도를 확인하고, `HINTS.md`의 마지막
  단계와 자신의 구현 순서를 비교하세요.

### `alternative.py` — 공개 풀이 접근을 주석과 함께 재작성

- 핵심 사고: {entries[1].approach}
- 복잡도: `{entries[1].complexity}`
- 적용 범위: {entries[1].note or "문제의 최대 제한에서도 실행 가능한 대안"}
- 문제별 주의: {pedagogy.pitfall}
- 출처 정책: [SOURCES.md](./SOURCES.md)에 정확한 스냅숏과 재작성 범위를 기록했습니다.

## 비교 방법

1. 두 파일에서 상태 정의와 핵심 불변식을 찾습니다.
2. 같은 입력을 어떤 순서로 처리하는지 손으로 추적합니다.
3. 최대 제한에서 시간·공간 차이를 계산합니다.
4. 대안 풀이가 느리다고 표시된 경우 작은 입력의 정답 오라클로만 사용합니다.

## 인터넷 참고

- [프로그래머스 문제별 풀이 Q&A](https://school.programmers.co.kr/learn/courses/30/lessons/{lesson_id}/questions)
- [공개 풀이 모음 저장소]({SHARED_REFERENCE})

참고 링크의 코드는 작성자별 스타일과 복잡도가 다릅니다. 정답 여부만 믿지 말고 현재
제한에서의 복잡도와 경계 처리를 직접 검증하세요.
"""


def main() -> int:
    directories = {
        problem_id(path.parent): path.parent
        for path in ROOT.glob("[0-9][0-9]_*/**/tests.json")
    }
    missing = sorted(set(directories) - {lesson_id for lesson_id, _ in ENTRIES})
    if missing:
        print(f"아직 풀이가 등록되지 않은 문제: {missing}")
    pedagogy_missing = sorted(set(directories) - set(PEDAGOGY))
    pedagogy_extra = sorted(set(PEDAGOGY) - set(directories))
    if pedagogy_missing or pedagogy_extra:
        raise ValueError(
            f"교육 데이터 ID 불일치: missing={pedagogy_missing}, extra={pedagogy_extra}"
        )

    generated = 0
    for lesson_id, directory in directories.items():
        variants = [
            ENTRIES[(lesson_id, variant)]
            for variant in ("recommended", "alternative")
            if (lesson_id, variant) in ENTRIES
        ]
        if not variants:
            continue
        solution_dir = directory / "solutions"
        solution_dir.mkdir(exist_ok=True)
        for entry in variants:
            (solution_dir / f"{entry.variant}.py").write_text(
                standalone_source(entry), encoding="utf-8"
            )
            generated += 1
        problem_readme_path = directory / "README.md"
        problem_readme = problem_readme_path.read_text(encoding="utf-8")
        title = problem_readme.splitlines()[0][2:]
        (solution_dir / "README.md").write_text(
            render_readme(lesson_id, title, variants), encoding="utf-8"
        )
        (solution_dir / "SOURCES.md").write_text(
            render_sources(lesson_id), encoding="utf-8"
        )
        (directory / "HINTS.md").write_text(
            render_hints(variants[0], directory.parent.name), encoding="utf-8"
        )
        link_line = "- 주석 포함 예시 풀이: [solutions/README.md](./solutions/README.md)"
        if link_line not in problem_readme:
            problem_readme = problem_readme.replace(
                "- 오프라인 문제 명세: [PROBLEM.md](./PROBLEM.md)",
                "- 오프라인 문제 명세: [PROBLEM.md](./PROBLEM.md)\n" + link_line,
            )
            problem_readme = problem_readme.replace(
                "3. 저장한 뒤 저장소 루트에서 아래 명령을 실행합니다.",
                "3. 저장한 뒤 저장소 루트에서 아래 명령을 실행합니다.\n"
                "4. 통과 후 `solutions/README.md`와 두 예시 답안을 비교하며 복기합니다.",
            )
            problem_readme_path.write_text(problem_readme, encoding="utf-8")
    print(f"예시 풀이 생성: {generated}개 파일")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
