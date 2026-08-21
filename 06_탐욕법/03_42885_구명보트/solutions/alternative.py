"""정렬 덱의 양끝에서 탑승자를 꺼냄.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42885/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(people, limit):
    # 이 구현의 선택: 정렬 덱의 양끝에서 탑승자를 꺼냄
    # 상태 정의: 정렬된 사람의 가장 가벼운 쪽과 가장 무거운 쪽 포인터를 둔다.
    # 핵심 불변식: 가장 무거운 사람은 현재 단계에서 반드시 한 보트를 사용하며, 가능할 때 가벼운 사람과 태우는 것이 최선이다.
    queue = deque(sorted(people))
    boats = 0
    while queue:
        heaviest = queue.pop()
        if queue and queue[0] + heaviest <= limit:
            queue.popleft()
        boats += 1
    return boats
