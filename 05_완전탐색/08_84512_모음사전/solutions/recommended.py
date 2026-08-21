"""각 자리의 사전순 가중치로 순번을 바로 계산.

복잡도: O(5) time, O(1) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(word):
    # 이 구현의 선택: 각 자리의 사전순 가중치로 순번을 바로 계산
    # 상태 정의: 각 자리에서 한 글자가 바뀔 때 건너뛰는 하위 단어 수를 가중치로 둔다.
    # 핵심 불변식: i번째 문자 전에는 앞선 문자 블록 수×자리 가중치와 자기 접두어 한 개가 누적된다.
    # 한 글자 아래에는 1+5+25+125+625개 단어가 연속해서 놓인다.
    weights = [781, 156, 31, 6, 1]
    order = {letter: index for index, letter in enumerate("AEIOU")}
    return sum(order[letter] * weights[index] + 1 for index, letter in enumerate(word))
