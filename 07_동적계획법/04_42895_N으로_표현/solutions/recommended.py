"""사용 횟수별 만들 수 있는 수의 집합 DP.

복잡도: O(8^3*S^2) worst time, O(8*S) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(N, number):
    # 이 구현의 선택: 사용 횟수별 만들 수 있는 수의 집합 DP
    # 상태 정의: dp[i]를 N을 정확히 i번 사용해 만들 수 있는 모든 수의 집합으로 둔다.
    # 핵심 불변식: dp[i]에는 이어 붙인 수와 dp[j], dp[i-j]의 사칙연산 결과가 모두 들어간다.
    possible = [set() for _ in range(9)]
    for count in range(1, 9):
        possible[count].add(int(str(N) * count))
        for left_count in range(1, count):
            right_count = count - left_count
            for left in possible[left_count]:
                for right in possible[right_count]:
                    possible[count].update((left + right, left - right, left * right))
                    if right:
                        possible[count].add(left // right)
        if number in possible[count]:
            return count
    return -1
