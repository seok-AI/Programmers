"""큐 순환과 남은 우선순위 빈도표.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import Counter, deque

def solution(priorities, location):
    # 이 구현의 선택: 큐 순환과 남은 우선순위 빈도표
    # 상태 정의: 대기 큐의 (원래 인덱스, 우선순위)와 남은 최대 우선순위를 유지한다.
    # 핵심 불변식: 큐 앞 작업은 남은 작업 중 더 높은 우선순위가 없을 때만 실행된다.
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
