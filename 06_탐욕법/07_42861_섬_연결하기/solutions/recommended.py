"""비용순 간선과 Union-Find를 쓰는 Kruskal MST.

복잡도: O(e log e) time, O(n) space
이 저장소를 위해 효율성과 제한 조건을 기준으로 독립 작성한 권장 풀이입니다.
"""

def solution(n, costs):
    # 이 구현의 선택: 비용순 간선과 Union-Find를 쓰는 Kruskal MST
    # 상태 정의: 각 섬의 연결요소 대표를 Union-Find로 관리한다.
    # 핵심 불변식: 선택한 간선은 사이클이 없고, 처리한 비용 이하 간선으로 만들 수 있는 최소 신장 숲이다.
    parent = list(range(n))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    total = selected = 0
    for left, right, cost in sorted(costs, key=lambda edge: edge[2]):
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            continue
        parent[root_right] = root_left
        total += cost
        selected += 1
        if selected == n - 1:
            break
    return total
