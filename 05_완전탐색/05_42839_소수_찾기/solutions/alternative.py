"""DFS로 수를 만들고 에라토스테네스의 체로 일괄 판정.

복잡도: O(n*n! + M log log M) time, O(M) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42839/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

import math

def solution(numbers):
    # 이 구현의 선택: DFS로 수를 만들고 에라토스테네스의 체로 일괄 판정
    # 상태 정의: 사용한 숫자 인덱스 순열로 만든 모든 정수를 집합에 모은다.
    # 핵심 불변식: 집합은 선행 0이나 중복 숫자 순열이 만든 같은 정수를 한 번만 남긴다.
    made = set()
    used = [False] * len(numbers)

    def build(current):
        if current:
            made.add(int(current))
        for index, digit in enumerate(numbers):
            if not used[index]:
                used[index] = True
                build(current + digit)
                used[index] = False

    build("")
    maximum = max(made, default=0)
    prime = bytearray(b"\x01") * (maximum + 1)
    if maximum >= 0:
        prime[0] = 0
    if maximum >= 1:
        prime[1] = 0
    for value in range(2, math.isqrt(maximum) + 1):
        if prime[value]:
            start = value * value
            prime[start : maximum + 1 : value] = b"\x00" * (((maximum - start) // value) + 1)
    return sum(prime[value] for value in made)
