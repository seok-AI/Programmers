"""최소/최대 힙과 활성 ID로 지연 삭제.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import heapq

def solution(operations):
    # 이 구현의 선택: 최소/최대 힙과 활성 ID로 지연 삭제
    # 상태 정의: 같은 삽입 ID를 최소 힙·최대 힙에 넣고 활성 ID 집합으로 삭제 여부를 공유한다.
    # 핵심 불변식: 각 힙의 죽은 루트를 정리한 뒤 루트는 활성 원소의 실제 극값이다.
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
