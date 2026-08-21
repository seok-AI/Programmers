"""빈도표의 키 수로 종류 계산.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/1845/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import Counter

def solution(nums):
    # 이 구현의 선택: 빈도표의 키 수로 종류 계산
    # 상태 정의: 서로 다른 종류 수와 뽑을 수 있는 총 마릿수만 남긴다.
    # 핵심 불변식: 한 종류에서 두 마리 이상 고르는 선택은 종류 수를 늘리지 않는다.
    kinds = Counter(nums)
    capacity = len(nums) // 2
    return capacity if len(kinds) >= capacity else len(kinds)
