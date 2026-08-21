"""크기 k의 최소 힙으로 상위 점수 유지.

복잡도: O(n log k) time, O(k) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import heapq

def solution(k, score):
    # 이 구현의 선택: 크기 k의 최소 힙으로 상위 점수 유지
    # 상태 정의: 현재까지의 상위 k개 점수만 최소 힙에 보관한다.
    # 핵심 불변식: 힙이 k개라면 루트는 현재까지 상위 k개 중 가장 낮은 발표 점수이다.
    hall = []
    answer = []
    for value in score:
        if len(hall) < k:
            heapq.heappush(hall, value)
        elif value > hall[0]:
            heapq.heapreplace(hall, value)
        answer.append(hall[0])
    return answer
