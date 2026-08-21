"""최소 거리의 가능 여부를 판정하는 매개변수 이분탐색.

복잡도: O(n log distance) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(distance, rocks, n):
    # 이 구현의 선택: 최소 거리의 가능 여부를 판정하는 매개변수 이분탐색
    # 상태 정의: 후보 최소거리 d를 지키며 남길 수 없는 바위 수를 탐욕적으로 센다.
    # 핵심 불변식: 왼쪽부터 이전에 남긴 바위와 거리가 d 미만이면 현재 바위를 제거하는 것이 이후 선택 공간을 최대화한다.
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
