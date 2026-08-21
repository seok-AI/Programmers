"""주어진 시간에 처리 가능한 사람 수로 최소 시간 이분탐색.

복잡도: O(k log answer) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(n, times):
    # 이 구현의 선택: 주어진 시간에 처리 가능한 사람 수로 최소 시간 이분탐색
    # 상태 정의: 시간 t 안에 각 심사관이 처리할 수 있는 사람 수의 합을 가능성 판정으로 쓴다.
    # 핵심 불변식: t가 충분하면 그보다 큰 시간도 충분하므로 가능 여부는 단조롭게 false에서 true로 바뀐다.
    low, high = 0, min(times) * n
    while low + 1 < high:
        middle = (low + high) // 2
        processed = sum(middle // duration for duration in times)
        if processed >= n:
            high = middle
        else:
            low = middle
    return high
