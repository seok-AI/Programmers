"""세 수의 조합을 열거해 합이 0인지 확인.

복잡도: O(n^3) time, O(1) extra space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from itertools import combinations

def solution(number):
    # 이 구현의 선택: 세 수의 조합을 열거해 합이 0인지 확인
    # 상태 정의: 서로 다른 세 인덱스의 조합만 열거한다.
    # 핵심 불변식: 조합은 같은 세 인덱스의 순서만 다른 중복을 만들지 않는다.
    # 사람의 순서는 중요하지 않으므로 순열이 아닌 조합을 사용한다.
    return sum(a + b + c == 0 for a, b, c in combinations(number, 3))
