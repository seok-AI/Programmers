"""가격이 처음 떨어지는 시점을 단조 스택으로 확정.

복잡도: O(n) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(prices):
    # 이 구현의 선택: 가격이 처음 떨어지는 시점을 단조 스택으로 확정
    # 상태 정의: 아직 가격 하락 시점을 만나지 못한 인덱스를 가격 비내림 순서의 스택에 둔다.
    # 핵심 불변식: 스택의 각 인덱스는 현재 시점까지 더 낮은 가격이 나오지 않았다.
    answer = [0] * len(prices)
    stack = []
    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            previous = stack.pop()
            answer[previous] = index - previous
        stack.append(index)
    last = len(prices) - 1
    while stack:
        previous = stack.pop()
        answer[previous] = last - previous
    return answer
