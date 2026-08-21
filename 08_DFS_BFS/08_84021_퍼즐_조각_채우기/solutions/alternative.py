"""각 도형의 네 회전 중 사전순 최소 좌표를 표준 모양으로 사용.

복잡도: O(n^2) time, O(n^2) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/84021/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import Counter

def solution(game_board, table):
    # 이 구현의 선택: 각 도형의 네 회전 중 사전순 최소 좌표를 표준 모양으로 사용
    # 상태 정의: 각 빈칸·조각 연결요소를 평행이동과 네 회전에 무관한 표준 좌표 튜플로 바꾼다.
    # 핵심 불변식: 좌표를 원점 이동하고 (행,열)→(열,-행)을 네 번 적용한 형식의 최솟값은 같은 도형끼리 같다.
    def extract(board, value):
        size = len(board)
        seen = set()
        shapes = []
        for row in range(size):
            for column in range(size):
                if board[row][column] != value or (row, column) in seen:
                    continue
                shape = []
                stack = [(row, column)]
                seen.add((row, column))
                while stack:
                    cell = stack.pop()
                    shape.append(cell)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        neighbor = (cell[0] + dr, cell[1] + dc)
                        if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size and board[neighbor[0]][neighbor[1]] == value and neighbor not in seen:
                            seen.add(neighbor)
                            stack.append(neighbor)
                shapes.append(shape)
        return shapes

    def shifted(shape):
        top = min(row for row, _ in shape)
        left = min(column for _, column in shape)
        return tuple(sorted((row - top, column - left) for row, column in shape))

    def canonical(shape):
        forms = []
        current = shape
        for _ in range(4):
            form = shifted(current)
            forms.append(form)
            # 회전 뒤 shifted를 다시 적용하므로 음수 좌표도 같은 원점으로 정렬된다.
            current = [(column, -row) for row, column in form]
        return min(forms)

    available = Counter(canonical(shape) for shape in extract(table, 1))
    filled = 0
    for hole in extract(game_board, 0):
        shape = canonical(hole)
        if available[shape]:
            available[shape] -= 1
            filled += len(hole)
    return filled
