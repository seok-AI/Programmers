"""가능한 h를 큰 값부터 직접 검증.

복잡도: O(n^2) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42747/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(citations):
    # 이 구현의 선택: 가능한 h를 큰 값부터 직접 검증
    # 상태 정의: 오름차순 인용 수와 현재 위치부터 남은 논문 수를 비교한다.
    # 핵심 불변식: 현재 인용 수가 남은 논문 수 이상인 첫 위치에서 그 수만큼의 논문이 조건을 만족한다.
    for h in range(len(citations), -1, -1):
        high = sum(citation >= h for citation in citations)
        low = sum(citation <= h for citation in citations)
        if high >= h and low >= len(citations) - h:
            return h
