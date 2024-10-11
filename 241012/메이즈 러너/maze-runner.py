# 2024.10.11 23:30 시작

# import sys
import math


# sys.stdin = open('input.txt', 'r')


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exit = False


# 상하좌우
dxs = [-1, 1, 0, 0]
dys = [0, 0, -1, 1]


def move_players(exit_x, exit_y):
    count = 0
    for player in players:
        if player.exit:
            continue

        for dx, dy in zip(dxs, dys):
            cur_x, cur_y = player.x, player.y
            next_x, next_y = cur_x + dx, cur_y + dy

            # 범위 확인
            if 0 <= next_x < N and 0 <= next_y < N:
                cur_dist = abs(exit_x - cur_x) + abs(exit_y - cur_y)
                next_dist = abs(exit_x - next_x) + abs(exit_y - next_y)

                # 거리 확인
                if next_dist < cur_dist:
                    # 벽 확인
                    if maps[next_x][next_y] == 0:
                        player.x = next_x
                        player.y = next_y
                        count += 1
                        # 탈출 확인
                        if player.x == exit_x and player.y == exit_y:
                            player.exit = True
                        break

    return count


def is_all_exit():
    for player in players:
        if not player.exit:
            return False
    return True


def find_box(exit_x, exit_y):
    max_r = -1
    max_c = -1
    min_width = math.inf

    for player in players:
        if player.exit:
            continue

        cur_width = max(abs(exit_x - player.x) + 1, abs(exit_y - player.y) + 1)
        r = max(max(exit_x, player.x) - cur_width + 1, 0)
        c = max(max(exit_y, player.y) - cur_width + 1, 0)

        if cur_width < min_width:
            min_width = cur_width
            max_r = r
            max_c = c
        elif cur_width == min_width:
            if r < max_r:
                min_width = cur_width
                max_r = r
                max_c = c
            elif r == max_r:
                if c < max_c:
                    min_width = cur_width
                    max_r = r
                    max_c = c
            pass

    return max_r, max_c, min_width


def rotate_exit(r, c, width, exit_x, exit_y):
    return exit_y - c + r, width - 1 - exit_x + r + c


def rotate_wall(r, c, width):
    before_wall = [[0] * width for _ in range(width)]
    for x in range(width):
        for y in range(width):
            before_wall[x][y] = maps[r + x][c + y]

    after_wall = [[0] * width for _ in range(width)]
    for x in range(width):
        for y in range(width):
            after_wall[y][width - x - 1] = max(before_wall[x][y] - 1, 0)

    for x in range(width):
        for y in range(width):
            maps[r + x][c + y] = after_wall[x][y]


def rotate_players(r, c, width):
    for player in players:
        if player.exit:
            continue

        if r <= player.x <= r + width - 1 and c <= player.y <= c + width - 1:
            x = player.y - c + r
            y = width - 1 - player.x + r + c
            player.x = x
            player.y = y


# N: 미로의 크기 (4≤N≤10)
# M: 참가자 수 (1≤M≤10)
# K: 게임 시간 (1≤K≤100)
N, M, K = map(int, input().split())

maps = []
for _ in range(N):
    maps.append(list(map(int, input().split())))

players = []
for _ in range(M):
    p = list(map(int, input().split()))
    players.append(Player(p[0] - 1, p[1] - 1))

exit_x, exit_y = map(int, input().split())
exit_x -= 1
exit_y -= 1

answer = 0
for t in range(K):
    answer += move_players(exit_x, exit_y)
    if is_all_exit():
        break
    r, c, width = find_box(exit_x, exit_y)
    rotate_wall(r, c, width)
    rotate_players(r, c, width)
    exit_x, exit_y = rotate_exit(r, c, width, exit_x, exit_y)

print(answer)
print(f"{exit_x + 1} {exit_y + 1}")