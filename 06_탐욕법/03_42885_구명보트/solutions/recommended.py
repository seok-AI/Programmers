"""가벼운 사람과 무거운 사람을 투 포인터로 짝지음.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(people, limit):
    # 이 구현의 선택: 가벼운 사람과 무거운 사람을 투 포인터로 짝지음
    # 상태 정의: 정렬된 사람의 가장 가벼운 쪽과 가장 무거운 쪽 포인터를 둔다.
    # 핵심 불변식: 가장 무거운 사람은 현재 단계에서 반드시 한 보트를 사용하며, 가능할 때 가벼운 사람과 태우는 것이 최선이다.
    ordered = sorted(people)
    light, heavy = 0, len(ordered) - 1
    boats = 0
    while light <= heavy:
        if light < heavy and ordered[light] + ordered[heavy] <= limit:
            light += 1
        heavy -= 1
        boats += 1
    return boats
