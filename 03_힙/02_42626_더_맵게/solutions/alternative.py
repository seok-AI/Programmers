"""정렬 원본 큐와 비감소 생성값 큐 병합.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42626/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(scoville, K):
    # 이 구현의 선택: 정렬 원본 큐와 비감소 생성값 큐 병합
    # 상태 정의: 아직 남은 음식의 매운 정도를 최소 힙으로 관리한다.
    # 핵심 불변식: 매 단계 힙의 루트가 전체의 최솟값이며, 이것이 K 이상이면 모두 조건을 만족한다.
    original = deque(sorted(scoville))
    mixed = deque()

    def pop_smallest():
        if not original:
            return mixed.popleft()
        if not mixed:
            return original.popleft()
        return original.popleft() if original[0] <= mixed[0] else mixed.popleft()

    count = 0
    while len(original) + len(mixed) >= 1:
        smallest = pop_smallest()
        if smallest >= K:
            return count
        if not original and not mixed:
            return -1
        second = pop_smallest()
        mixed.append(smallest + 2 * second)
        count += 1
    return -1
