"""작은 앞자리 숫자를 제거하는 단조 감소 스택.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(number, k):
    # 이 구현의 선택: 작은 앞자리 숫자를 제거하는 단조 감소 스택
    # 상태 정의: 앞에서부터 선택한 숫자를 스택에 두고 아직 삭제 가능한 개수 k를 유지한다.
    # 핵심 불변식: 스택은 삭제 예산으로 제거할 수 있었던 더 작은 앞자리를 모두 제거한 상태이다.
    stack = []
    removals = k
    for digit in number:
        while removals and stack and stack[-1] < digit:
            stack.pop()
            removals -= 1
        stack.append(digit)
    if removals:
        del stack[-removals:]
    return "".join(stack)
