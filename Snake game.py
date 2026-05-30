import os
import random
import time
import sys

try:
    import msvcrt
except ImportError:
    msvcrt = None

WIDTH = 40
HEIGHT = 20
FRAME_DELAY = 0.1

GREEN = '\033[32m'
RED = '\033[31m'
BLACK = '\033[30m'
RESET = '\033[0m'

KEY_UP = 'UP'
KEY_DOWN = 'DOWN'
KEY_LEFT = 'LEFT'
KEY_RIGHT = 'RIGHT'

DIRECTION_KEYS = {
    'w': KEY_UP,
    'W': KEY_UP,
    'H': KEY_UP,
    's': KEY_DOWN,
    'S': KEY_DOWN,
    'P': KEY_DOWN,
    'a': KEY_LEFT,
    'A': KEY_LEFT,
    'K': KEY_LEFT,
    'd': KEY_RIGHT,
    'D': KEY_RIGHT,
    'M': KEY_RIGHT,
}

OPPOSITE = {
    KEY_UP: KEY_DOWN,
    KEY_DOWN: KEY_UP,
    KEY_LEFT: KEY_RIGHT,
    KEY_RIGHT: KEY_LEFT,
}


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()


def get_key():
    if not msvcrt:
        return None
    if not msvcrt.kbhit():
        return None

    ch = msvcrt.getwch()
    if ch in ('\x00', '\xe0'):
        ch = msvcrt.getwch()
    return DIRECTION_KEYS.get(ch)


def draw_board(snake, food, score):
    board = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for x, y in snake:
        board[y][x] = f'{GREEN}o{RESET}'
    head_x, head_y = snake[0]
    board[head_y][head_x] = f'{GREEN}O{RESET}'

    fx, fy = food
    board[fy][fx] = f'{RED}@{RESET}'

    top_border = BLACK + 'X' * (WIDTH + 2) + RESET
    print(top_border)
    for row in board:
        print(BLACK + 'X' + RESET + ''.join(row) + BLACK + 'X' + RESET)
    print(top_border)
    print(f' Score: {GREEN}{score}{RESET}   Controls: WASD / arrows   Ctrl+C to quit')


def random_food_position(snake):
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if (x, y) not in snake:
            return x, y


def move_snake(direction, snake, grow=False):
    head_x, head_y = snake[0]
    if direction == KEY_UP:
        head_y -= 1
    elif direction == KEY_DOWN:
        head_y += 1
    elif direction == KEY_LEFT:
        head_x -= 1
    elif direction == KEY_RIGHT:
        head_x += 1

    new_head = (head_x, head_y)
    new_snake = [new_head] + snake
    if not grow:
        new_snake.pop()
    return new_snake


def snake_hits_wall(head):
    x, y = head
    return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT


def snake_hits_self(snake):
    return snake[0] in snake[1:]


def main():
    snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - 1, HEIGHT // 2), (WIDTH // 2 - 2, HEIGHT // 2)]
    direction = KEY_RIGHT
    food = random_food_position(snake)
    score = 0
    last_key = direction

    clear_screen()
    print('SNAKE GAME')
    print('Use W/A/S/D or arrow keys to move. Eat @ to grow. Avoid walls and yourself. Press Ctrl+C to quit.')
    print('Press any key to start...')
    if msvcrt:
        while not msvcrt.kbhit():
            time.sleep(0.05)
        msvcrt.getwch()
    else:
        input()

    try:
        while True:
            key = get_key()
            if key and key != OPPOSITE.get(direction):
                last_key = key

            if last_key != direction and last_key != OPPOSITE.get(direction):
                direction = last_key

            snake = move_snake(direction, snake)
            head = snake[0]

            if snake_hits_wall(head) or snake_hits_self(snake):
                clear_screen()
                draw_board(snake, food, score)
                print(f'\nGame Over! Final score: {RED}{score}{RESET}')
                break

            if head == food:
                score += 1
                snake = move_snake(direction, snake, grow=True)
                food = random_food_position(snake)

            clear_screen()
            draw_board(snake, food, score)
            time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        clear_screen()
        print('Game interrupted. Thanks for playing!')


if __name__ == '__main__':
    main()
