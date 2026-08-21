"""단어 그래프를 미리 만든 뒤 최단거리 BFS.

복잡도: O(n^2*L) time, O(n^2) space
온라인 공개 풀이에서 널리 쓰이는 접근을 학습용으로 독립 재구현했습니다.
참고: https://school.programmers.co.kr/learn/courses/30/lessons/43163/questions
공개 풀이 모음: https://github.com/codeisneverodd/programmers-coding-test
"""

from collections import deque

def solution(begin, target, words):
    # 이 구현의 선택: 단어 그래프를 미리 만든 뒤 최단거리 BFS
    # 상태 정의: 단어를 정점, 한 글자만 다른 관계를 간선으로 보고 BFS 거리를 둔다.
    # 핵심 불변식: 큐에서 처음 꺼낸 단어의 단계 수는 begin에서 그 단어까지의 최소 변환 횟수이다.
    vocabulary = [begin] + list(words)
    if target not in vocabulary:
        return 0
    graph = [[] for _ in vocabulary]
    for left in range(len(vocabulary)):
        for right in range(left + 1, len(vocabulary)):
            if sum(a != b for a, b in zip(vocabulary[left], vocabulary[right])) == 1:
                graph[left].append(right)
                graph[right].append(left)
    queue = deque([(0, 0)])
    visited = {0}
    while queue:
        node, distance = queue.popleft()
        if vocabulary[node] == target:
            return distance
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return 0
