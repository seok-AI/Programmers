"""최대 4자리 반복 키로 내림차순 정렬.

복잡도: O(n log n) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/42746/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(numbers):
    # 이 구현의 선택: 최대 4자리 반복 키로 내림차순 정렬
    # 상태 정의: 두 문자열 a, b의 배치 우선순위를 a+b와 b+a로 결정한다.
    # 핵심 불변식: 정렬된 모든 이웃 쌍은 왼쪽+오른쪽이 반대 배치보다 작지 않다.
    strings = list(map(str, numbers))
    # 원소 길이가 최대 4이므로 충분히 반복한 앞 4문자가 비교 순서를 결정한다.
    strings.sort(key=lambda value: (value * 4)[:4], reverse=True)
    result = "".join(strings)
    # int 변환은 100,000자리 입력에서 불필요하게 큰 정수를 만들므로 피한다.
    return "0" if result[0] == "0" else result
