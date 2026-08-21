"""간선을 하나씩 끊고 BFS로 한쪽 송전탑 수 계산.

복잡도: O(n^2) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

from collections import deque

def solution(n, wires):
    # 이 구현의 선택: 간선을 하나씩 끊고 BFS로 한쪽 송전탑 수 계산
    # 상태 정의: 한 전선을 제외했을 때 임의의 한쪽 연결요소 크기를 센다.
    # 핵심 불변식: 트리에서 간선 하나를 끊으면 정확히 두 컴포넌트가 되고 크기 합은 n이다.
    answer = n
    for removed, _ in enumerate(wires):
        graph = [[] for _ in range(n + 1)]
        for index, (left, right) in enumerate(wires):
            if index != removed:
                graph[left].append(right)
                graph[right].append(left)
        seen = {1}
        queue = deque([1])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        answer = min(answer, abs(n - 2 * len(seen)))
    return answer
