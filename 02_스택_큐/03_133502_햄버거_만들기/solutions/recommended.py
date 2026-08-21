"""최근 네 재료를 스택에서 즉시 제거.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(ingredient):
    # 이 구현의 선택: 최근 네 재료를 스택에서 즉시 제거
    # 상태 정의: 아직 햄버거로 제거되지 않은 재료의 순서를 스택에 둔다.
    # 핵심 불변식: 새 재료로 완성될 수 있는 패턴은 스택 맨 위 네 칸뿐이다.
    stack = []
    burgers = 0
    for item in ingredient:
        stack.append(item)
        if len(stack) >= 4 and stack[-4:] == [1, 2, 3, 1]:
            del stack[-4:]
            burgers += 1
    return burgers
