import sys
from queue import Queue


# sys.stdin = open("./input.txt", "r")


def find_down_pos(cur_x, cur_y, d):
    while True:
        # 1) 남쪽 이동
        next_x, next_y = cur_x + 1, cur_y
        if (
                1 <= next_x < R + 2
                and 1 <= next_y < C - 1
                and maps[next_x][next_y - 1] == 0
                and maps[next_x][next_y + 1] == 0
                and maps[next_x + 1][next_y] == 0
        ):
            cur_x, cur_y = next_x, next_y
            continue
        # 2) 서쪽 회전
        next_x, next_y = cur_x + 1, cur_y - 1
        if (
                1 <= next_x < R + 2
                and 1 <= next_y < C - 1
                and maps[next_x - 2][next_y] == 0
                and maps[next_x - 1][next_y - 1] == 0
                and maps[next_x][next_y] == 0
                and maps[next_x][next_y - 1] == 0
                and maps[next_x + 1][next_y] == 0
        ):
            cur_x, cur_y = next_x, next_y

            d = (d - 1) % 4
            continue

        # 3) 동쪽 회전
        next_x, next_y = cur_x + 1, cur_y + 1
        if (
                1 <= next_x < R + 2
                and 1 <= next_y < C - 1
                and maps[next_x - 2][next_y] == 0
                and maps[next_x - 1][next_y + 1] == 0
                and maps[next_x][next_y] == 0
                and maps[next_x][next_y + 1] == 0
                and maps[next_x + 1][next_y] == 0
        ):
            cur_x, cur_y = next_x, next_y
            d = (d + 1) % 4
            continue

        break

    return cur_x, cur_y, d


def get_gate(cur_x, cur_y, d):
    if d == 0:
        return cur_x - 1, cur_y
    elif d == 1:
        return cur_x, cur_y + 1
    elif d == 2:
        return cur_x + 1, cur_y
    elif d == 3:
        return cur_x, cur_y - 1


def bfs(cur_x, cur_y):
    q = Queue()
    q.put((cur_x, cur_y))
    visited = [[0] * C for _ in range(R + 3)]
    visited[cur_x][cur_y] = 1
    max_x = cur_x

    while True:
        if q.empty():
            break
        cur_x, cur_y = q.get()

        for dx, dy in zip(dxs, dys):
            next_x, next_y = cur_x + dx, cur_y + dy
            # 범위 체크
            if 0 <= next_x < R + 3 and 0 <= next_y < C:
                # 방문 체크
                if visited[next_x][next_y] == 0:
                    # 같은 골렘 이동 or 다른 골렘 게이트 사용
                    if (
                            (maps[next_x][next_y] != 0 and maps[next_x][next_y] == maps[cur_x][cur_y])
                            or
                            (maps[next_x][next_y] != 0 and maps[next_x][next_y] != maps[cur_x][cur_y] and
                             (cur_x, cur_y) in gates)
                    ):
                        visited[next_x][next_y] = 1
                        max_x = max(max_x, next_x)
                        q.put((next_x, next_y))
    return max_x


R, C, K = map(int, input().split())

# 범위 row: 3 ~ R+2
# 범위 column: 0 ~ C-1
maps = [[0] * C for _ in range(R + 3)]
gates = set()
dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]
answer = 0

for i in range(1, K + 1):
    ci, di = map(int, input().split())
    x, y, di = find_down_pos(1, ci - 1, di)
    gate_x, gate_y = get_gate(x, y, di)
    # print(f"pos: ({x - 2}, {y}), gate = ({gate_x - 2}, {gate_y})")

    # 포함 못되는 경우 초기화
    if 0 <= x < 4:
        maps = [[0] * C for _ in range(R + 3)]
        gates = set()
        continue

    maps[x][y] = i
    for dx, dy in zip(dxs, dys):
        maps[x + dx][y + dy] = i
    gates.add((gate_x, gate_y))

    answer += bfs(x, y) - 2

print(answer)