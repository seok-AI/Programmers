"""고정 배열과 top 포인터로 단조 스택 구현.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42883/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(number, k):
    # 이 구현의 선택: 고정 배열과 top 포인터로 단조 스택 구현
    # 상태 정의: 앞에서부터 선택한 숫자를 스택에 두고 아직 삭제 가능한 개수 k를 유지한다.
    # 핵심 불변식: 스택은 삭제 예산으로 제거할 수 있었던 더 작은 앞자리를 모두 제거한 상태이다.
    buffer = [""] * len(number)
    top = 0
    removals = k
    for digit in number:
        while removals and top and buffer[top - 1] < digit:
            top -= 1
            removals -= 1
        buffer[top] = digit
        top += 1
    return "".join(buffer[: top - removals])
