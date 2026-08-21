"""종류별 (선택+미선택) 경우를 곱함.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import Counter

def solution(clothes):
    # 이 구현의 선택: 종류별 (선택+미선택) 경우를 곱함
    # 상태 정의: 의상 종류별 개수와 그 종류를 입지 않는 한 가지 선택을 센다.
    # 핵심 불변식: 처리한 종류들의 선택 조합 수에는 ‘모두 미선택’인 조합이 정확히 하나 포함된다.
    counts = Counter(kind for _, kind in clothes)
    combinations_count = 1
    for count in counts.values():
        combinations_count *= count + 1  # 이 종류를 입지 않는 한 경우 포함
    return combinations_count - 1  # 아무것도 입지 않는 경우 제외
