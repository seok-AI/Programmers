"""Floyd-Warshall로 모든 승패 도달 관계 계산.

복잡도: O(n^3) time, O(n^2) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(n, results):
    # 이 구현의 선택: Floyd-Warshall로 모든 승패 도달 관계 계산
    # 상태 정의: win[a][b]를 a가 b를 이긴 사실이 직접 또는 간접으로 알려졌는지로 둔다.
    # 핵심 불변식: 중간 선수 k까지 반영한 뒤 행렬은 그 선수들을 경유하는 모든 승패 도달성을 포함한다.
    wins = [[False] * n for _ in range(n)]
    for winner, loser in results:
        wins[winner - 1][loser - 1] = True
    for middle in range(n):
        for winner in range(n):
            if wins[winner][middle]:
                for loser in range(n):
                    wins[winner][loser] |= wins[middle][loser]
    return sum(
        all(player == other or wins[player][other] or wins[other][player] for other in range(n))
        for player in range(n)
    )
