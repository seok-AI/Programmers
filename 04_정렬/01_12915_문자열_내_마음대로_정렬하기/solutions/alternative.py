"""사전순 선행 정렬 뒤 안정 정렬.

복잡도: O(m log m) time, O(m) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/12915/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(strings, n):
    # 이 구현의 선택: 사전순 선행 정렬 뒤 안정 정렬
    # 상태 정의: 문자열의 n번째 문자와 문자열 전체를 한 쌍의 정렬 키로 사용한다.
    # 핵심 불변식: 첫 키가 같을 때 전체 문자열 오름차순이 동률을 정확히 해소한다.
    # Python 정렬은 안정적이므로 두 번째 정렬의 동률에서 사전순이 보존된다.
    ordered = sorted(strings)
    ordered.sort(key=lambda word: word[n])
    return ordered
