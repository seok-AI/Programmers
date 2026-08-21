"""트럭별 진입 시각과 종료 시각을 이벤트로 관리.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import deque

def solution(bridge_length, weight, truck_weights):
    # 이 구현의 선택: 트럭별 진입 시각과 종료 시각을 이벤트로 관리
    # 상태 정의: 다리 위 트럭의 종료 시각과 무게 합, 다음 진입 가능 시각을 관리한다.
    # 핵심 불변식: 현재 시각보다 종료 시각이 이른 트럭은 모두 빠졌고, 다리 위 무게는 제한 이하이다.
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
