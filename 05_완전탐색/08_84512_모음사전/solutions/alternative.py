"""길이 1..5의 모든 단어를 생성해 사전순 위치 탐색.

복잡도: O(5^5 log 5^5) time, O(5^5) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/84512/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from itertools import product

def solution(word):
    # 이 구현의 선택: 길이 1..5의 모든 단어를 생성해 사전순 위치 탐색
    # 상태 정의: 각 자리에서 한 글자가 바뀔 때 건너뛰는 하위 단어 수를 가중치로 둔다.
    # 핵심 불변식: i번째 문자 전에는 앞선 문자 블록 수×자리 가중치와 자기 접두어 한 개가 누적된다.
    alphabet = "AEIOU"
    words = []
    for length in range(1, 6):
        words.extend("".join(letters) for letters in product(alphabet, repeat=length))
    words.sort()
    return words.index(word) + 1
