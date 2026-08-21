"""최소 힙에서 가장 작은 두 음식 반복 혼합.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import heapq

def solution(scoville, K):
    # 이 구현의 선택: 최소 힙에서 가장 작은 두 음식 반복 혼합
    # 상태 정의: 아직 남은 음식의 매운 정도를 최소 힙으로 관리한다.
    # 핵심 불변식: 매 단계 힙의 루트가 전체의 최솟값이며, 이것이 K 이상이면 모두 조건을 만족한다.
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
