"""첫 집 포함/제외를 나눠 선형 도둑질 DP 두 번.

복잡도: O(n) time, O(1) extra space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(money):
    # 이 구현의 선택: 첫 집 포함/제외를 나눠 선형 도둑질 DP 두 번
    # 상태 정의: 원형 배열을 첫 집 제외 구간과 마지막 집 제외 구간 두 선형 문제로 나눈다.
    # 핵심 불변식: 선형 구간의 각 위치 최적값은 이전 최적과 두 칸 전 최적+현재 돈 중 큰 값이다.
    def rob(values):
        two_back = one_back = 0
        for value in values:
            two_back, one_back = one_back, max(one_back, two_back + value)
        return one_back

    # 원형에서는 첫 집과 마지막 집을 동시에 고를 수 없다.
    return max(rob(money[:-1]), rob(money[1:]))
