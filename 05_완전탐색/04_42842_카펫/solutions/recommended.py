"""전체 격자의 약수 쌍에서 테두리 조건 확인.

복잡도: O(sqrt(area)) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import math

def solution(brown, yellow):
    # 이 구현의 선택: 전체 격자의 약수 쌍에서 테두리 조건 확인
    # 상태 정의: 전체 칸 수의 약수 쌍을 가능한 (세로, 가로) 크기로 본다.
    # 핵심 불변식: 정답 크기에서는 전체 넓이가 brown+yellow이고 안쪽 넓이가 yellow이다.
    area = brown + yellow
    for height in range(3, math.isqrt(area) + 1):
        if area % height == 0:
            width = area // height
            if (width - 2) * (height - 2) == yellow:
                return [width, height]
