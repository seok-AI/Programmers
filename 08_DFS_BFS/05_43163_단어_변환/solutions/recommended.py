"""한 글자 차이인 단어를 BFS로 탐색.

복잡도: O(n^2*L) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import deque

def solution(begin, target, words):
    # 이 구현의 선택: 한 글자 차이인 단어를 BFS로 탐색
    # 상태 정의: 단어를 정점, 한 글자만 다른 관계를 간선으로 보고 BFS 거리를 둔다.
    # 핵심 불변식: 큐에서 처음 꺼낸 단어의 단계 수는 begin에서 그 단어까지의 최소 변환 횟수이다.
    if target not in words:
        return 0
    queue = deque([(begin, 0)])
    visited = set()
    while queue:
        current, steps = queue.popleft()
        if current == target:
            return steps
        for index, word in enumerate(words):
            if index not in visited and sum(left != right for left, right in zip(current, word)) == 1:
                visited.add(index)
                queue.append((word, steps + 1))
    return 0
