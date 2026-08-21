"""기능별 완료일 계산 후 비감소 배포 경계 그룹화.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

import math

def solution(progresses, speeds):
    # 이 구현의 선택: 기능별 완료일 계산 후 비감소 배포 경계 그룹화
    # 상태 정의: 각 기능의 완료일과 현재 배포 묶음의 기준 완료일을 유지한다.
    # 핵심 불변식: 현재 묶음에는 선두 기능의 완료일까지 끝나는 연속 기능만 들어간다.
    days = [math.ceil((100 - progress) / speed) for progress, speed in zip(progresses, speeds)]
    answer = []
    release_day = days[0]
    batch = 0
    for day in days:
        if day <= release_day:
            batch += 1
        else:
            answer.append(batch)
            release_day = day
            batch = 1
    answer.append(batch)
    return answer
