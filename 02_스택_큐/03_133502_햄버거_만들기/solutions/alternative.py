"""고정 배열과 top 포인터로 스택 구현.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/133502/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(ingredient):
    # 이 구현의 선택: 고정 배열과 top 포인터로 스택 구현
    # 상태 정의: 아직 햄버거로 제거되지 않은 재료의 순서를 스택에 둔다.
    # 핵심 불변식: 새 재료로 완성될 수 있는 패턴은 스택 맨 위 네 칸뿐이다.
    stack = [0] * len(ingredient)
    top = 0
    burgers = 0
    for item in ingredient:
        stack[top] = item
        top += 1
        if top >= 4 and stack[top - 4 : top] == [1, 2, 3, 1]:
            top -= 4
            burgers += 1
    return burgers
