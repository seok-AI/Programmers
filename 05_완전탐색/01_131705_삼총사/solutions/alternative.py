"""서로 다른 세 인덱스를 삼중 반복문으로 선택.

복잡도: O(n^3) time, O(1) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/131705/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(number):
    # 이 구현의 선택: 서로 다른 세 인덱스를 삼중 반복문으로 선택
    # 상태 정의: 서로 다른 세 인덱스의 조합만 열거한다.
    # 핵심 불변식: 조합은 같은 세 인덱스의 순서만 다른 중복을 만들지 않는다.
    answer = 0
    for first in range(len(number) - 2):
        for second in range(first + 1, len(number) - 1):
            for third in range(second + 1, len(number)):
                if number[first] + number[second] + number[third] == 0:
                    answer += 1
    return answer
