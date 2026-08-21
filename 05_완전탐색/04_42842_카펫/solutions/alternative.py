"""노란 내부 높이를 늘리며 가로 길이 계산.

복잡도: O(sqrt(yellow)) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42842/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

import math

def solution(brown, yellow):
    # 이 구현의 선택: 노란 내부 높이를 늘리며 가로 길이 계산
    # 상태 정의: 전체 칸 수의 약수 쌍을 가능한 (세로, 가로) 크기로 본다.
    # 핵심 불변식: 정답 크기에서는 전체 넓이가 brown+yellow이고 안쪽 넓이가 yellow이다.
    for inner_height in range(1, math.isqrt(yellow) + 1):
        if yellow % inner_height == 0:
            inner_width = yellow // inner_height
            width, height = inner_width + 2, inner_height + 2
            if 2 * width + 2 * height - 4 == brown:
                return [width, height]
