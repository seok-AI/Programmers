"""각 번호의 모든 진접두어를 해시 조회.

복잡도: O(total digits) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42577/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(phone_book):
    # 이 구현의 선택: 각 번호의 모든 진접두어를 해시 조회
    # 상태 정의: 사전순으로 정렬된 전화번호의 이웃 쌍만 비교한다.
    # 핵심 불변식: 어떤 번호가 다른 번호의 접두어라면 정렬 결과에서 그 접두어로 시작하는 첫 번호와 인접한다.
    numbers = set(phone_book)
    for number in phone_book:
        # 자기 자신은 비교 대상이 아니므로 마지막 문자는 제외한다.
        for end in range(1, len(number)):
            if number[:end] in numbers:
                return False
    return True
