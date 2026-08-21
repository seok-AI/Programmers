"""기본 지속 시간을 채운 뒤 단조 스택으로 하락 시점 갱신.

복잡도: O(n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42584/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(prices):
    # 이 구현의 선택: 기본 지속 시간을 채운 뒤 단조 스택으로 하락 시점 갱신
    # 상태 정의: 아직 가격 하락 시점을 만나지 못한 인덱스를 가격 비내림 순서의 스택에 둔다.
    # 핵심 불변식: 스택의 각 인덱스는 현재 시점까지 더 낮은 가격이 나오지 않았다.
    last = len(prices) - 1
    answer = [last - index for index in range(len(prices))]
    unresolved = []
    for current, price in enumerate(prices):
        while unresolved and prices[unresolved[-1]] > price:
            previous = unresolved.pop()
            answer[previous] = current - previous
        unresolved.append(current)
    return answer
