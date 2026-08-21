"""경로 압축과 union by size를 포함한 Union-Find 참조 구현."""


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.component_size = [1] * size

    def find(self, node: int) -> int:
        # 루트까지 올라간 모든 노드를 한 번에 루트에 연결한다.
        while node != self.parent[node]:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, left: int, right: int) -> bool:
        """서로 다른 집합을 합치면 True, 이미 같으면 False를 반환한다."""
        left_root, right_root = self.find(left), self.find(right)
        if left_root == right_root:
            return False
        if self.component_size[left_root] < self.component_size[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        self.component_size[left_root] += self.component_size[right_root]
        return True


def kruskal(node_count: int, edges: list[list[int]]) -> int | None:
    """[비용, 정점1, 정점2] 간선의 MST 비용. 연결 불가능하면 None."""
    groups = UnionFind(node_count)
    total = selected = 0
    for cost, left, right in sorted(edges):
        if groups.union(left, right):
            total += cost
            selected += 1
            if selected == node_count - 1:
                return total
    return 0 if node_count <= 1 else None


if __name__ == "__main__":
    assert kruskal(3, [[1, 0, 1], [2, 1, 2], [10, 0, 2]]) == 3
    assert kruskal(3, [[1, 0, 1]]) is None
    print("Union-Find 스니펫 자체 검증 PASS")
