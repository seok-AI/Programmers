"""다리 길이만큼의 고정 큐를 매초 이동.

복잡도: O(total seconds) time, O(bridge_length) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42583/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(bridge_length, weight, truck_weights):
    # 이 구현의 선택: 다리 길이만큼의 고정 큐를 매초 이동
    # 상태 정의: 다리 위 트럭의 종료 시각과 무게 합, 다음 진입 가능 시각을 관리한다.
    # 핵심 불변식: 현재 시각보다 종료 시각이 이른 트럭은 모두 빠졌고, 다리 위 무게는 제한 이하이다.
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
