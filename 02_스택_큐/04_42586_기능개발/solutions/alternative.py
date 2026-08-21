"""완료일 큐에서 선두 이하를 묶어 배포.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42586/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque
import math

def solution(progresses, speeds):
    # 이 구현의 선택: 완료일 큐에서 선두 이하를 묶어 배포
    # 상태 정의: 각 기능의 완료일과 현재 배포 묶음의 기준 완료일을 유지한다.
    # 핵심 불변식: 현재 묶음에는 선두 기능의 완료일까지 끝나는 연속 기능만 들어간다.
    queue = deque(
        math.ceil((100 - progress) / speed)
        for progress, speed in zip(progresses, speeds)
    )
    answer = []
    while queue:
        release_day = queue.popleft()
        count = 1
        while queue and queue[0] <= release_day:
            queue.popleft()
            count += 1
        answer.append(count)
    return answer
