"""이름-순위 역인덱스로 인접 교환.

복잡도: O(n+m) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(players, callings):
    # 이 구현의 선택: 이름-순위 역인덱스로 인접 교환
    # 상태 정의: 현재 순위 배열과 이름에서 현재 인덱스로 가는 역인덱스를 함께 유지한다.
    # 핵심 불변식: 매 호출 뒤 두 자료구조는 같은 순위를 나타내며, 호출된 선수와 앞 선수만 위치가 바뀐다.
    ranking = list(players)  # 입력 변형을 피한다.
    position = {name: rank for rank, name in enumerate(ranking)}

    for called in callings:
        current = position[called]
        overtaken = ranking[current - 1]
        ranking[current - 1], ranking[current] = called, overtaken
        position[called] = current - 1
        position[overtaken] = current
    return ranking
