"""요청 시각 정렬 + 실행 시간 우선 힙.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import heapq

def solution(jobs):
    # 이 구현의 선택: 요청 시각 정렬 + 실행 시간 우선 힙
    # 상태 정의: 현재 시각까지 요청된 작업을 실행 시간 기준 최소 힙에 둔다.
    # 핵심 불변식: 힙에는 이미 도착했지만 시작하지 않은 작업만 있고, 루트가 다음 SJF 작업이다.
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
