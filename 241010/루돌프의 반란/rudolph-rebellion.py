# 2024.10.10 16:03 시작
import sys
import math

# sys.stdin = open("./input.txt", "r")


class Santa:
    def __init__(self, id, x, y, status):
        self.id = id
        self.x = x
        self.y = y
        # -1: 탈락, 0: 일반, 1: 스턴
        self.status = status
        self.stun_time = 0
        self.score = 0


def find_nearest_santa(r_x, r_y):
    nearest_s = None
    nearest_distance = math.inf

    for santa in santas:
        if santa.status == -1:
            continue

        distance = (r_x - santa.x) ** 2 + (r_y - santa.y) ** 2

        if distance < nearest_distance:
            nearest_s = santa
            nearest_distance = distance
        elif distance == nearest_distance:
            if santa.x > nearest_s.x:
                nearest_s = santa
                nearest_distance = distance
            elif santa.x == nearest_s.x:
                if santa.y > nearest_s.y:
                    nearest_s = santa
                    nearest_distance = distance

    return nearest_s


def move_rudolph(r_x, r_y, santa):
    dx = santa.x - r_x
    if dx != 0:
        dx //= abs(dx)
    dy = santa.y - r_y
    if dy != 0:
        dy //= abs(dy)

    next_rx = r_x + dx
    next_ry = r_y + dy

    # 충돌 발생
    if next_rx == santa.x and next_ry == santa.y:
        maps[santa.x][santa.y] = 0
        santa.score += C
        santa.x += dx * C
        santa.y += dy * C

        if 0 <= santa.x < N and 0 <= santa.y < N:
            santa.status = 1
            santa.stun_time = 2
            after_effect(santa, dx, dy)
        else:
            santa.status = -1

    maps[r_x][r_y] = 0
    maps[next_rx][next_ry] = 99

    return next_rx, next_ry


def move_santas(r_x, r_y):
    for santa in santas:
        if santa.status == -1 or santa.status == 1:
            continue

        dx, dy = find_direction(santa.x, santa.y, r_x, r_y)
        # print(f"id:{santa.id} x:{santa.x} y:{santa.y} {(dx, dy)}")
        if dx is None and dy is None:
            continue

        next_x = santa.x + dx
        next_y = santa.y + dy

        # 비어 있을 때
        if maps[next_x][next_y] == 0:
            maps[santa.x][santa.y] = 0
            maps[next_x][next_y] = santa.id
            santa.x = next_x
            santa.y = next_y

        # 루돌프 있을 때
        elif maps[next_x][next_y] == 99:
            maps[santa.x][santa.y] = 0
            santa.score += D
            santa.x = next_x - dx * D
            santa.y = next_y - dy * D
            if 0 <= santa.x < N and 0 <= santa.y < N:
                santa.status = 1
                santa.stun_time = 2
                after_effect(santa, -dx, -dy)
            else:
                santa.status = -1


def find_direction(s_x, s_y, r_x, r_y):
    min_dist = abs(s_x - r_x) ** 2 + abs(s_y - r_y) ** 2
    direction_x = None
    direction_y = None

    for dx, dy in zip(dxs, dys):
        next_x = s_x + dx
        next_y = s_y + dy

        if 0 <= next_x < N and 0 <= next_y < N:
            if maps[next_x][next_y] == 0 or maps[next_x][next_y] == 99:
                new_dist = abs(next_x - r_x) ** 2 + abs(next_y - r_y) ** 2
                if new_dist < min_dist:
                    min_dist = new_dist
                    direction_x = dx
                    direction_y = dy

    return direction_x, direction_y


def after_effect(cur_santa, dx, dy):
    while True:
        next_santa_i = maps[cur_santa.x][cur_santa.y] - 1
        if next_santa_i == -1:
            maps[cur_santa.x][cur_santa.y] = cur_santa.id
            break
        maps[cur_santa.x][cur_santa.y] = cur_santa.id
        cur_santa = santas[next_santa_i]
        cur_santa.x += dx
        cur_santa.y += dy
        if cur_santa.x < 0 or cur_santa.x >= N or cur_santa.y < 0 or cur_santa.y >= N:
            cur_santa.status = -1
            break


def round_finish():
    alive_santa_count = 0

    for santa in santas:
        if santa.status == -1:
            continue
        if santa.status == 1:
            santa.stun_time -= 1
            if santa.stun_time == 0:
                santa.status = 0

        alive_santa_count += 1
        santa.score += 1

    return alive_santa_count


def get_scores():
    scores = ""
    for santa in santas:
        scores += f"{santa.score} "

    return scores.strip()


N, M, P, C, D = map(int, input().split())

dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]
maps = [[0] * N for _ in range(N)]
santas = []
rudolph_x, rudolph_y = map(int, input().split())
rudolph_x -= 1
rudolph_y -= 1
maps[rudolph_x][rudolph_y] = 99

for i in range(P):
    santa_id, pos_x, pos_y = map(int, input().split())
    pos_x -= 1
    pos_y -= 1
    santas.append(Santa(santa_id, pos_x, pos_y, 0))
    maps[pos_x][pos_y] = santa_id
santas.sort(key=lambda santa: santa.id)

for t in range(M):
    # print(f"Turn {t} start")
    # for r in maps:
    #     print(*r, sep="  ")

    nearest_santa = find_nearest_santa(rudolph_x, rudolph_y)
    if nearest_santa is None:
        break

    rudolph_x, rudolph_y = move_rudolph(rudolph_x, rudolph_y, nearest_santa)
    # print("------rudolph move----------")
    # for r in maps:
    #     print(*r, sep="  ")
    move_santas(rudolph_x, rudolph_y)
    # print("-------santa move-----------")
    # for r in maps:
    #     print(*r, sep="  ")
    santa_count = round_finish()
    if santa_count == 0:
        break

print(get_scores())