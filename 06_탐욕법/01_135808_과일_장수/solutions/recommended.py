"""점수를 내림차순 정렬해 상자별 최솟값 선택.

복잡도: O(n log n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(k, m, score):
    # 이 구현의 선택: 점수를 내림차순 정렬해 상자별 최솟값 선택
    # 상태 정의: 완전한 상자마다 포함된 최저 점수가 그 상자의 단가를 결정한다.
    # 핵심 불변식: 높은 점수부터 m개씩 묶으면 각 상자의 최솟값을 가능한 한 크게 만든다.
    ordered = sorted(score, reverse=True)
    # 완성된 각 묶음의 마지막 원소가 그 상자의 최저 점수다.
    return sum(ordered[index] * m for index in range(m - 1, len(ordered), m))
