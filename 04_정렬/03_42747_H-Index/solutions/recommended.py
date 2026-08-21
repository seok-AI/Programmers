"""정렬한 인용수와 남은 논문 수 비교.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(citations):
    # 이 구현의 선택: 정렬한 인용수와 남은 논문 수 비교
    # 상태 정의: 오름차순 인용 수와 현재 위치부터 남은 논문 수를 비교한다.
    # 핵심 불변식: 현재 인용 수가 남은 논문 수 이상인 첫 위치에서 그 수만큼의 논문이 조건을 만족한다.
    ordered = sorted(citations)
    count = len(ordered)
    for index, citation in enumerate(ordered):
        papers = count - index
        if citation >= papers:
            return papers
    return 0
