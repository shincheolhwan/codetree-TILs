# 2024.10.11 21:02 시작
import sys
from queue import Queue

# sys.stdin = open("./input.txt", "r")


class Knight:
    def __init__(self, id, r, c, h, w, k):
        self.id = id
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.k = k
        self.damage = 0

    def is_dead(self):
        if self.k <= self.damage:
            return True
        else:
            return False


def move_knight(id, direction):
    knight = knights[id]

    if knight.is_dead():
        return knight_maps

    new_maps = []
    for row in knight_maps:
        new_maps.append(row.copy())

    can_move, moved = check_move(knight, direction)
    # print(f"can_move: {can_move}, moved: {moved}")
    if can_move:
        for moved_id in moved:
            cur_knight = knights[moved_id]
            count = 0
            # print(f"id:{cur_knight.id}")
            if direction == 0:
                before_r = cur_knight.r + cur_knight.h - 1
                next_r = cur_knight.r - 1
                for i in range(cur_knight.c, cur_knight.c + cur_knight.w):
                    if new_maps[before_r][i] == cur_knight.id:
                        new_maps[before_r][i] = 0
                    new_maps[next_r][i] = cur_knight.id
                cur_knight.r -= 1
            elif direction == 1:
                before_c = cur_knight.c
                next_c = cur_knight.c + cur_knight.w
                for i in range(cur_knight.r, cur_knight.r + cur_knight.h):
                    if new_maps[i][before_c] == cur_knight.id:
                        new_maps[i][before_c] = 0
                    new_maps[i][next_c] = cur_knight.id
                cur_knight.c += 1
            elif direction == 2:
                before_r = cur_knight.r
                next_r = cur_knight.r + cur_knight.h
                for i in range(cur_knight.c, cur_knight.c + cur_knight.w):
                    if new_maps[before_r][i] == cur_knight.id:
                        new_maps[before_r][i] = 0
                    new_maps[next_r][i] = cur_knight.id
                cur_knight.r += 1
            elif direction == 3:
                before_c = cur_knight.c + cur_knight.w - 1
                next_c = cur_knight.c - 1
                for i in range(cur_knight.r, cur_knight.r + cur_knight.h):
                    if new_maps[i][before_c] == cur_knight.id:
                        new_maps[i][before_c] = 0
                    new_maps[i][next_c] = cur_knight.id
                cur_knight.c -= 1

            if id != moved_id:
                for i in range(cur_knight.r, cur_knight.r + cur_knight.h):
                    for j in range(cur_knight.c, cur_knight.c + cur_knight.w):
                        if chess_maps[i][j] == 1:
                            count += 1
                cur_knight.damage += count

                # print(f"k:{cur_knight.k}, damage:{cur_knight.damage}")
                if cur_knight.is_dead():
                    for i in range(cur_knight.r, cur_knight.r + cur_knight.h):
                        for j in range(cur_knight.c, cur_knight.c + cur_knight.w):
                            new_maps[i][j] = 0

        return new_maps
    else:
        return knight_maps


def check_move(knight, direction):
    moved = {knight.id}
    q = Queue()
    q.put(knight)

    while True:
        if q.empty():
            break

        cur_knight = q.get()
        # 위
        if direction == 0:
            next_r = cur_knight.r - 1
            if 0 <= next_r < L:
                for i in range(cur_knight.c, cur_knight.c + cur_knight.w):
                    if chess_maps[next_r][i] == 2:
                        return False, set()

                    next_knight_id = knight_maps[next_r][i]
                    if next_knight_id != 0 and next_knight_id not in moved:
                        moved.add(next_knight_id)
                        q.put(knights[next_knight_id])
            else:
                return False, set()
        # 오른쪽
        elif direction == 1:
            next_c = cur_knight.c + cur_knight.w
            if 0 <= next_c < L:
                for i in range(cur_knight.r, cur_knight.r + cur_knight.h):
                    if chess_maps[i][next_c] == 2:
                        return False, set()

                    next_knight_id = knight_maps[i][next_c]
                    if next_knight_id != 0 and next_knight_id not in moved:
                        moved.add(next_knight_id)
                        q.put(knights[next_knight_id])
            else:
                return False, set()
        # 아래
        elif direction == 2:
            next_r = cur_knight.r + cur_knight.h
            if 0 <= next_r < L:
                for i in range(cur_knight.c, cur_knight.c + cur_knight.w):
                    if chess_maps[next_r][i] == 2:
                        return False, set()

                    next_knight_id = knight_maps[next_r][i]
                    if next_knight_id != 0 and next_knight_id not in moved:
                        moved.add(next_knight_id)
                        q.put(knights[next_knight_id])
            else:
                return False, set()
        # 왼쪽
        elif direction == 3:
            next_c = cur_knight.c - 1
            if 0 <= next_c < L:
                for i in range(cur_knight.r, cur_knight.r + cur_knight.h):
                    if chess_maps[i][next_c] == 2:
                        return False, set()

                    next_knight_id = knight_maps[i][next_c]
                    if next_knight_id != 0 and next_knight_id not in moved:
                        moved.add(next_knight_id)
                        q.put(knights[next_knight_id])
            else:
                return False, set()
    return True, moved


# L: 체스판의 크기 (3≤L≤40)
# N: 기사의 수 (1≤N≤30)
# Q: 명령의 수 (1≤Q≤100)
L, N, Q = map(int, input().split())

chess_maps = []
for _ in range(L):
    chess_maps.append(list(map(int, input().split())))

knight_maps = [[0] * L for _ in range(L)]
knights: [None | Knight] = [None] * (N + 1)
for id in range(1, N + 1):
    # (r,c): 초기 위치
    # h: 세로 길이
    # w: 가로 길이
    # k: 기사의 체력 (1≤k≤100)
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    for i in range(h):
        for j in range(w):
            knight_maps[r + i][c + j] = id
    knights[id] = Knight(id, r, c, h, w, k)

for t in range(1, Q + 1):
    id, direction = map(int, input().split())
    knight_maps = move_knight(id, direction)

answer = 0
for knight in knights:
    if knight is not None and not knight.is_dead():
        answer += knight.damage

print(answer)