"""아래 행에서 위로 올라오며 최선의 자식 합 선택.

복잡도: O(n^2) time, O(n^2) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(triangle):
    # 이 구현의 선택: 아래 행에서 위로 올라오며 최선의 자식 합 선택
    # 상태 정의: 각 칸에서 바닥까지 내려가 얻을 수 있는 최대 합을 저장한다.
    # 핵심 불변식: 아래 행의 값이 이미 최적이면 현재 칸은 두 자식 중 큰 값만 더하면 최적이다.
    best = [row[:] for row in triangle]
    for row in range(len(best) - 2, -1, -1):
        for column in range(len(best[row])):
            best[row][column] += max(best[row + 1][column], best[row + 1][column + 1])
    return best[0][0]
