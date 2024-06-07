import os
import sys
import random
import pygame
import section2_cfg as cfg

def isGameOver(board, size):
    num_cells = size * size
    return all(board[i] == i for i in range(num_cells - 1))

def moveR(board, blank_cell_idx, num_cols):
    if blank_cell_idx % num_cols != 0:
        board[blank_cell_idx - 1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx - 1]
        return blank_cell_idx - 1
    return blank_cell_idx

def moveL(board, blank_cell_idx, num_cols):
    if (blank_cell_idx + 1) % num_cols != 0:
        board[blank_cell_idx + 1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx + 1]
        return blank_cell_idx + 1
    return blank_cell_idx

def moveD(board, blank_cell_idx, num_cols):
    if blank_cell_idx >= num_cols:
        board[blank_cell_idx - num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx - num_cols]
        return blank_cell_idx - num_cols
    return blank_cell_idx

def moveU(board, blank_cell_idx, num_rows, num_cols):
    if blank_cell_idx < (num_rows - 1) * num_cols:
        board[blank_cell_idx + num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx + num_cols]
        return blank_cell_idx + num_cols
    return blank_cell_idx

def CreateBoard(num_rows, num_cols):
    num_cells = num_rows * num_cols
    board = list(range(num_cells))
    blank_cell_idx = num_cells - 1
    board[blank_cell_idx] = -1

    for _ in range(cfg.RANDOM):
        direction = random.choice(['L', 'R', 'U', 'D'])
        if direction == 'L':
            blank_cell_idx = moveL(board, blank_cell_idx, num_cols)
        elif direction == 'R':
            blank_cell_idx = moveR(board, blank_cell_idx, num_cols)
        elif direction == 'U':
            blank_cell_idx = moveU(board, blank_cell_idx, num_rows, num_cols)
        elif direction == 'D':
            blank_cell_idx = moveD(board, blank_cell_idx, num_cols)
    return board, blank_cell_idx

def GetImagePath(rootdir):
    try:
        imagenames = os.listdir(rootdir)
        if not imagenames:
            raise FileNotFoundError(f"No images found in directory: {rootdir}")
        return os.path.join(rootdir, random.choice(imagenames))
    except FileNotFoundError as e:
        print(e)
        sys.exit()

def ShowMessage(screen, message, width, height, font_size, color, midtop):
    font = pygame.font.Font(cfg.FONT, font_size)
    text = font.render(message, True, color)
    rect = text.get_rect()
    rect.midtop = midtop
    screen.blit(text, rect)

def ShowEndInterface(screen, width, height):
    screen.fill(cfg.BACKGROUNDCOLOR)
    ShowMessage(screen, 'Good Job! You Win!', width, height, width // 20, (233, 150, 122), (width / 2, height / 2.5))

    replay_font = pygame.font.Font(cfg.FONT, width // 30)
    replay_text = replay_font.render('Press R to Replay', True, cfg.BUTTONTEXTCOLOR)
    replay_rect = replay_text.get_rect()
    replay_rect.midtop = (width / 2, height / 1.8)
    
    pygame.draw.rect(screen, cfg.BUTTONCOLOR, replay_rect.inflate(20, 10))
    screen.blit(replay_text, replay_rect)
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN] and (event.key == pygame.K_ESCAPE or event.key == ord('r')):
                return

def ShowStartInterface(screen, width, height):
    screen.fill(cfg.BACKGROUNDCOLOR)
    ShowMessage(screen, 'Hello Kitty Puzzle', width, height, width // 10, cfg.RED, (width / 2, height / 12))
    ShowMessage(screen, 'Press H, M or L to choose your puzzle', width, height, width // 30, cfg.BLUE, (width / 2, height / 2.2))
    ShowMessage(screen, ' H - 5x5 , M - 4x4 , L - 3x3 ', width, height, width // 30, cfg.BLUE, (width / 2, height / 1.8))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('l'):
                    return 3
                elif event.key == ord('m'):
                    return 4
                elif event.key == ord('h'):
                    return 5

def main():
    pygame.init()
    clock = pygame.time.Clock()

    while True:  # Main game loop
        image_path = GetImagePath(cfg.PICTURE_ROOT_DIR)
        game_img_used = pygame.image.load(image_path)
        game_img_used = pygame.transform.scale(game_img_used, cfg.SCREENSIZE)
        game_img_used_rect = game_img_used.get_rect()

        screen = pygame.display.set_mode(cfg.SCREENSIZE)
        pygame.display.set_caption('Funny Puzzle Game')

        size = ShowStartInterface(screen, game_img_used_rect.width, game_img_used_rect.height)
        num_rows, num_cols = size, size

        cell_width = game_img_used_rect.width // num_cols
        cell_height = game_img_used_rect.height // num_rows

        game_board, blank_cell_idx = CreateBoard(num_rows, num_cols)
        is_running = True
        
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, ord('a')]:
                        blank_cell_idx = moveL(game_board, blank_cell_idx, num_cols)
                    elif event.key in [pygame.K_RIGHT, ord('d')]:
                        blank_cell_idx = moveR(game_board, blank_cell_idx, num_cols)
                    elif event.key in [pygame.K_UP, ord('w')]:
                        blank_cell_idx = moveU(game_board, blank_cell_idx, num_rows, num_cols)
                    elif event.key in [pygame.K_DOWN, ord('s')]:
                        blank_cell_idx = moveD(game_board, blank_cell_idx, num_cols)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.mouse.get_pos()
                    x_pos = x // cell_width
                    y_pos = y // cell_height
                    idx = x_pos + y_pos * num_cols
                    if idx == blank_cell_idx - 1:
                        blank_cell_idx = moveR(game_board, blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx + 1:
                        blank_cell_idx = moveL(game_board, blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx + num_cols:
                        blank_cell_idx = moveU(game_board, blank_cell_idx, num_rows, num_cols)
                    elif idx == blank_cell_idx - num_cols:
                        blank_cell_idx = moveD(game_board, blank_cell_idx, num_cols)
            
            if isGameOver(game_board, size):
                game_board[blank_cell_idx] = size * size - 1
                is_running = False

            screen.fill(cfg.BACKGROUNDCOLOR)
            for i in range(size * size):
                if game_board[i] == -1:
                    continue
                x_pos = i // num_cols
                y_pos = i % num_cols
                
                rect = pygame.Rect(y_pos * cell_width, x_pos * cell_height, cell_width, cell_height)
                img_area = pygame.Rect((game_board[i] % num_cols) * cell_width, (game_board[i] // num_cols) * cell_height, cell_width, cell_height)
                
                screen.blit(game_img_used, rect, img_area)
                
            for i in range(num_cols + 1):
                pygame.draw.line(screen, cfg.TILEBORDERCOLOR, (i * cell_width, 0), (i * cell_width, game_img_used_rect.height))
            for i in range(num_rows + 1):
                pygame.draw.line(screen, cfg.TILEBORDERCOLOR, (0, i * cell_height), (game_img_used_rect.width, i * cell_height))
                    
            pygame.display.update()
            clock.tick(cfg.FPS)
                                
        ShowEndInterface(screen, game_img_used_rect.width, game_img_used_rect.height)

if __name__ == "__main__":
    main()
