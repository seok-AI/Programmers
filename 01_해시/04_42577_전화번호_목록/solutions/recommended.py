"""정렬 후 인접 전화번호만 비교.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(phone_book):
    # 이 구현의 선택: 정렬 후 인접 전화번호만 비교
    # 상태 정의: 사전순으로 정렬된 전화번호의 이웃 쌍만 비교한다.
    # 핵심 불변식: 어떤 번호가 다른 번호의 접두어라면 정렬 결과에서 그 접두어로 시작하는 첫 번호와 인접한다.
    # 접두어 관계가 있다면 사전순 정렬에서 두 번호가 반드시 인접한다.
    ordered = sorted(phone_book)
    return all(not right.startswith(left) for left, right in zip(ordered, ordered[1:]))
