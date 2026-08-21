"""a+b와 b+a를 비교하는 사용자 정렬.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from functools import cmp_to_key

def solution(numbers):
    # 이 구현의 선택: a+b와 b+a를 비교하는 사용자 정렬
    # 상태 정의: 두 문자열 a, b의 배치 우선순위를 a+b와 b+a로 결정한다.
    # 핵심 불변식: 정렬된 모든 이웃 쌍은 왼쪽+오른쪽이 반대 배치보다 작지 않다.
    strings = list(map(str, numbers))

    def compare(left, right):
        if left + right > right + left:
            return -1
        if left + right < right + left:
            return 1
        return 0

    result = "".join(sorted(strings, key=cmp_to_key(compare)))
    return "0" if result[0] == "0" else result
