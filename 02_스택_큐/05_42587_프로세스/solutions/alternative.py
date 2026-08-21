"""매 회차 큐의 최대 우선순위와 비교.

복잡도: O(n^2) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42587/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(priorities, location):
    # 이 구현의 선택: 매 회차 큐의 최대 우선순위와 비교
    # 상태 정의: 대기 큐의 (원래 인덱스, 우선순위)와 남은 최대 우선순위를 유지한다.
    # 핵심 불변식: 큐 앞 작업은 남은 작업 중 더 높은 우선순위가 없을 때만 실행된다.
    queue = deque(enumerate(priorities))
    executed = 0
    while queue:
        item = queue.popleft()
        if queue and item[1] < max(priority for _, priority in queue):
            queue.append(item)
            continue
        executed += 1
        if item[0] == location:
            return executed
