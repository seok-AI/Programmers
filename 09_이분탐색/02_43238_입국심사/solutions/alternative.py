"""첫 가능 시간을 찾는 닫힌 구간 이분탐색.

복잡도: O(k log answer) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43238/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(n, times):
    # 이 구현의 선택: 첫 가능 시간을 찾는 닫힌 구간 이분탐색
    # 상태 정의: 시간 t 안에 각 심사관이 처리할 수 있는 사람 수의 합을 가능성 판정으로 쓴다.
    # 핵심 불변식: t가 충분하면 그보다 큰 시간도 충분하므로 가능 여부는 단조롭게 false에서 true로 바뀐다.
    left, right = 1, max(times) * n
    answer = right
    while left <= right:
        middle = (left + right) // 2
        if sum(middle // duration for duration in times) >= n:
            answer = middle
            right = middle - 1
        else:
            left = middle + 1
    return answer
