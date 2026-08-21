"""각 수에 +와 -를 붙이는 재귀 DFS.

복잡도: O(2^n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43165/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(numbers, target):
    # 이 구현의 선택: 각 수에 +와 -를 붙이는 재귀 DFS
    # 상태 정의: 지금까지의 숫자로 만들 수 있는 합별 경우의 수를 상태로 둔다.
    # 핵심 불변식: 숫자 하나를 처리한 뒤 새 상태는 이전 모든 합에 그 수를 더하거나 뺀 결과의 정확한 빈도이다.
    answer = 0

    def search(index, total):
        nonlocal answer
        if index == len(numbers):
            answer += total == target
            return
        search(index + 1, total + numbers[index])
        search(index + 1, total - numbers[index])

    search(0, 0)
    return answer
