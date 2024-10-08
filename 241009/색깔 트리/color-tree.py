# 2024.10.08 19:34 시작
import sys

# sys.stdin = open('./input.txt', 'r')


class Node:
    def __init__(self, mid, pid, color, max_depth):
        self.mid = mid
        self.pid = pid
        self.color = color
        self.child = []
        self.max_depth = max_depth


def add_node(mid, pid, color, max_depth):
    node = Node(mid, pid, color, max_depth)
    nodes[mid] = node

    if pid == -1:
        roots.append(node)
    else:
        nodes[pid].child.append(node)


def change_color(node, color, max_depth=101):
    max_depth = min(max_depth, node.max_depth)
    if node.max_depth <= 0:
        return

    node.color = color

    for child in node.child:
        change_color(child, color, max_depth - 1)


def get_score(node, max_depth=101):
    if node is None:
        return 0, set()

    max_depth = min(max_depth, node.max_depth)
    if max_depth <= 0:
        return 0, set()

    total_score = 0
    colors = {node.color}

    for child in node.child:
        score, child_colors = get_score(child, max_depth - 1)
        total_score += score
        colors = colors.union(child_colors)

    total_score += len(colors) ** 2
    return total_score, colors


roots: list[Node] = []
nodes: list[None | Node] = [None] * 100_001
Q = int(input())

for _ in range(Q):
    commands = list(map(int, input().split()))

    # 노드 추가
    if commands[0] == 100:
        m_id, p_id, c, d = commands[1:]
        add_node(m_id, p_id, c, d)
        pass
    # 색깔 변경
    elif commands[0] == 200:
        m_id, c = commands[1:]

        if nodes[m_id]:
            change_color(nodes[m_id], c)
    # 색깔 조회
    elif commands[0] == 300:
        m_id = commands[1]
        if nodes[m_id]:
            print(nodes[m_id].color)
    # 점수 조회
    elif commands[0] == 400:
        answer = 0
        for root in roots:
            answer += get_score(root)[0]
        print(answer)