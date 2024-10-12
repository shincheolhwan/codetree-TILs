# 2024.10.12 19:00 시작
import sys


# sys.stdin = open('input.txt', 'r')

class Runner:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.catch = False


def change_direction_positions(n):
    top_to_right = set()
    right_to_bottom = set()
    bottom_to_left = set()
    left_to_top = set()

    bottom_to_right = set()
    right_to_top = set()
    top_to_left = set()
    left_to_bottom = set()

    for i in range(1, n // 2 + 1):
        top_to_right.add((i - 1, i))
        left_to_bottom.add((i - 1, i))

    for i in range(n // 2 + 1, n):
        bottom_to_left.add((i, i))
        right_to_top.add((i, i))

    for i in range(0, n // 2):
        left_to_top.add((n - 1 - i, i))
        bottom_to_right.add((n - 1 - i, i))

    for i in range(n // 2 + 1, n):
        right_to_bottom.add((n - 1 - i, i))
        top_to_left.add((n - 1 - i, i))

    return top_to_right, right_to_bottom, bottom_to_left, left_to_top, bottom_to_right, right_to_top, top_to_left, left_to_bottom


def move_runners(tagger_x, tagger_y):
    for runner in runners:
        # 이미 잡힌 경우
        if runner.catch:
            continue

        dist = abs(tagger_x - runner.x) + abs(tagger_y - runner.y)

        if dist <= 3:
            next_x = runner.x + dxs[runner.direction]
            next_y = runner.y + dys[runner.direction]

            # 넘어 가는 경우
            if next_x < 0 or next_x >= n or next_y < 0 or next_y >= n:
                # 상
                if runner.direction == 0:
                    runner.direction = 1

                # 하
                elif runner.direction == 1:
                    runner.direction = 0

                # 좌
                elif runner.direction == 2:
                    runner.direction = 3

                # 우
                elif runner.direction == 3:
                    runner.direction = 2

                next_x = runner.x + dxs[runner.direction]
                next_y = runner.y + dys[runner.direction]

            if next_x != tagger_x or next_y != tagger_y:
                runner.x = next_x
                runner.y = next_y


def move_tagger(tagger_x, tagger_y, tagger_direction, is_reverse):
    next_x = tagger_x + dxs[tagger_direction]
    next_y = tagger_y + dys[tagger_direction]
    next_direction = tagger_direction
    next_reverse = is_reverse

    if next_x == 0 and next_y == 0:
        next_direction = 1
        next_is_reverse = True
        return next_x, next_y, next_direction, next_is_reverse
    elif next_x == n // 2 and next_y == n // 2:
        next_direction = 0
        next_is_reverse = False
        return next_x, next_y, next_direction, next_is_reverse
    else:
        if is_reverse:
            if (next_x, next_y) in bottom_to_right:
                next_direction = 3
            elif (next_x, next_y) in right_to_top:
                next_direction = 0
            elif (next_x, next_y) in top_to_left:
                next_direction = 2
            elif (next_x, next_y) in left_to_bottom:
                next_direction = 1
        else:
            if (next_x, next_y) in top_to_right:
                next_direction = 3
            elif (next_x, next_y) in right_to_bottom:
                next_direction = 1
            elif (next_x, next_y) in bottom_to_left:
                next_direction = 2
            elif (next_x, next_y) in left_to_top:
                next_direction = 0

        return next_x, next_y, next_direction, next_reverse


def catch_runners(tagger_x, tagger_y, tagger_direction):
    count = 0
    catch_positions = {
        (tagger_x, tagger_y),
        (tagger_x + dxs[tagger_direction], tagger_y + dys[tagger_direction]),
        (tagger_x + 2 * dxs[tagger_direction], tagger_y + 2 * dys[tagger_direction])
    }

    for runner in runners:
        if runner.catch:
            continue
        # 잡히는 위치에 있는 경우
        if (runner.x, runner.y) in catch_positions:
            # 나무가 없는 경우
            if tree_map[runner.x][runner.y] == 0:
                count += 1
                runner.catch = True
    return count


# 상하좌우
dxs = [-1, 1, 0, 0]
dys = [0, 0, -1, 1]

n, m, h, k = map(int, input().split())
tree_map = [[0] * n for _ in range(n)]
runners = []

for _ in range(m):
    x, y, d = map(int, input().split())
    x -= 1
    y -= 1
    # 좌우
    if d == 1:
        runners.append(Runner(x, y, 3))
    # 상하
    elif d == 2:
        runners.append(Runner(x, y, 1))

for _ in range(h):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    tree_map[x][y] = 1

t_x = n // 2
t_y = n // 2
t_d = 0
is_reverse = False

(
    top_to_right, right_to_bottom, bottom_to_left, left_to_top,
    bottom_to_right, right_to_top, top_to_left, left_to_bottom
) = change_direction_positions(n)

score = 0
for t in range(1, k + 1):
    move_runners(t_x, t_y)
    t_x, t_y, t_d, is_reverse = move_tagger(t_x, t_y, t_d, is_reverse)
    c = catch_runners(t_x, t_y, t_d)
    score += t * c

print(score)