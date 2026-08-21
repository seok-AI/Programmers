"""구간별 최솟값·최댓값을 함께 저장하는 구간 DP.

복잡도: O(n^3) time, O(n^2) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import math

def solution(arr):
    # 이 구현의 선택: 구간별 최솟값·최댓값을 함께 저장하는 구간 DP
    # 상태 정의: min[i][j], max[i][j]를 i번째 수부터 j번째 수까지 식의 최소·최대값으로 둔다.
    # 핵심 불변식: 모든 분할 위치와 양쪽 극값 조합을 보면 뺄셈에서 필요한 반대 극값까지 빠짐없이 포함된다.
    numbers = list(map(int, arr[::2]))
    operators = arr[1::2]
    count = len(numbers)
    minimum = [[math.inf] * count for _ in range(count)]
    maximum = [[-math.inf] * count for _ in range(count)]
    for index, value in enumerate(numbers):
        minimum[index][index] = maximum[index][index] = value

    for length in range(2, count + 1):
        for left in range(count - length + 1):
            right = left + length - 1
            for split in range(left, right):
                if operators[split] == "+":
                    candidates = (
                        minimum[left][split] + minimum[split + 1][right],
                        maximum[left][split] + maximum[split + 1][right],
                    )
                else:
                    # 뺄셈의 최대는 왼쪽 최대 - 오른쪽 최소다.
                    candidates = (
                        minimum[left][split] - maximum[split + 1][right],
                        maximum[left][split] - minimum[split + 1][right],
                    )
                minimum[left][right] = min(minimum[left][right], *candidates)
                maximum[left][right] = max(maximum[left][right], *candidates)
    return maximum[0][count - 1]
