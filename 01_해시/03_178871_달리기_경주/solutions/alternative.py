"""두 방향 매핑을 명시적으로 동기화.

복잡도: O(n+m) time, O(n) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/178871/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

def solution(players, callings):
    # 이 구현의 선택: 두 방향 매핑을 명시적으로 동기화
    # 상태 정의: 현재 순위 배열과 이름에서 현재 인덱스로 가는 역인덱스를 함께 유지한다.
    # 핵심 불변식: 매 호출 뒤 두 자료구조는 같은 순위를 나타내며, 호출된 선수와 앞 선수만 위치가 바뀐다.
    rank_to_name = dict(enumerate(players))
    name_to_rank = {name: rank for rank, name in rank_to_name.items()}

    for name in callings:
        rank = name_to_rank[name]
        front_name = rank_to_name[rank - 1]
        rank_to_name[rank - 1], rank_to_name[rank] = name, front_name
        name_to_rank[name], name_to_rank[front_name] = rank - 1, rank
    return [rank_to_name[rank] for rank in range(len(players))]
