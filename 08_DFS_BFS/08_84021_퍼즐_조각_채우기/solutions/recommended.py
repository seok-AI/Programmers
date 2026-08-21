"""빈칸/조각 컴포넌트를 추출하고 회전 정규화해 매칭.

복잡도: O(n^2) time, O(n^2) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import Counter, deque

def solution(game_board, table):
    # 이 구현의 선택: 빈칸/조각 컴포넌트를 추출하고 회전 정규화해 매칭
    # 상태 정의: 각 빈칸·조각 연결요소를 평행이동과 네 회전에 무관한 표준 좌표 튜플로 바꾼다.
    # 핵심 불변식: 좌표를 원점 이동하고 (행,열)→(열,-행)을 네 번 적용한 형식의 최솟값은 같은 도형끼리 같다.
    def components(board, target):
        size = len(board)
        visited = [[False] * size for _ in range(size)]
        result = []
        for start_row in range(size):
            for start_column in range(size):
                if visited[start_row][start_column] or board[start_row][start_column] != target:
                    continue
                queue = deque([(start_row, start_column)])
                visited[start_row][start_column] = True
                cells = []
                while queue:
                    row, column = queue.popleft()
                    cells.append((row, column))
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        next_row, next_column = row + dr, column + dc
                        if 0 <= next_row < size and 0 <= next_column < size and not visited[next_row][next_column] and board[next_row][next_column] == target:
                            visited[next_row][next_column] = True
                            queue.append((next_row, next_column))
                result.append(cells)
        return result

    def normalize(cells):
        min_row = min(row for row, _ in cells)
        min_column = min(column for _, column in cells)
        return tuple(sorted((row - min_row, column - min_column) for row, column in cells))

    def rotations(cells):
        current = list(cells)
        result = []
        for _ in range(4):
            normalized = normalize(current)
            result.append(normalized)
            # (행, 열) -> (열, -행)은 원점 기준 90도 회전이다.
            current = [(column, -row) for row, column in normalized]
        return result

    pieces = Counter()
    for piece in components(table, 1):
        # 네 회전의 사전순 최솟값을 택하면 시작 방향과 무관한 표준 키가 된다.
        pieces[min(rotations(piece))] += 1
    answer = 0
    for hole in components(game_board, 0):
        key = min(rotations(hole))
        if pieces[key]:
            pieces[key] -= 1
            answer += len(hole)
    return answer
