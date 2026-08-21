"""두 힙과 값별 개수로 지연 삭제.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42628/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import Counter
import heapq

def solution(operations):
    # 이 구현의 선택: 두 힙과 값별 개수로 지연 삭제
    # 상태 정의: 같은 삽입 ID를 최소 힙·최대 힙에 넣고 활성 ID 집합으로 삭제 여부를 공유한다.
    # 핵심 불변식: 각 힙의 죽은 루트를 정리한 뒤 루트는 활성 원소의 실제 극값이다.
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
