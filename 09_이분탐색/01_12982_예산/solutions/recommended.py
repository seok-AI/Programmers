"""신청 금액을 작은 순서로 더해 예산 내 부서 수 최대화.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(d, budget):
    # 이 구현의 선택: 신청 금액을 작은 순서로 더해 예산 내 부서 수 최대화
    # 상태 정의: 현재까지 선택한 부서 수와 사용 예산을 유지한다.
    # 핵심 불변식: 같은 수의 부서를 지원할 때 가장 작은 신청액부터 고른 합이 최소이다.
    supported = 0
    for request in sorted(d):
        if request > budget:
            break
        budget -= request
        supported += 1
    return supported
