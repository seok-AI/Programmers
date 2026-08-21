"""각 명함의 긴 변과 짧은 변을 같은 축으로 정렬.

복잡도: O(n) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(sizes):
    # 이 구현의 선택: 각 명함의 긴 변과 짧은 변을 같은 축으로 정렬
    # 상태 정의: 각 명함의 긴 변을 한 축, 짧은 변을 다른 축으로 통일한다.
    # 핵심 불변식: 지금까지 본 명함은 긴 변 최댓값 × 짧은 변 최댓값 지갑에 모두 들어간다.
    long_side = max(max(width, height) for width, height in sizes)
    short_side = max(min(width, height) for width, height in sizes)
    return long_side * short_side
