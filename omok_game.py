import pygame

# 1. 게임 초기화
pygame.init()

# 2. 게임 창 설정
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("오목 게임")

# 3. 게임 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (210, 180, 140) # 나무색

# 오목판 설정
BOARD_SIZE = 19
CELL_SIZE = 40
BOARD_MARGIN = 40
GRID_START = BOARD_MARGIN
GRID_END = screen_width - BOARD_MARGIN

# 게임 변수
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)] # 0: 빈칸, 1: 흑돌, 2: 백돌
turn = 1 # 1: 흑돌 차례, 2: 백돌 차례
game_over = False # 게임 종료 여부
winner = 0 # 0: 없음, 1: 흑돌 승, 2: 백돌 승

# 승리 조건 확인 함수
def check_win(r, c, player):
    # 4방향 (가로, 세로, 대각선 2개)에 대한 방향 벡터
    directions = [
        (0, 1),   # 가로
        (1, 0),   # 세로
        (1, 1),   # 우하향 대각선
        (1, -1)   # 우상향 대각선
    ]

    for dr, dc in directions:
        count = 1 # 현재 돌 포함
        # print(f"Checking direction: dr={dr}, dc={dc}")
        # 양방향으로 탐색
        # 정방향
        for i in range(1, 5):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        # 역방향
        for i in range(1, 5):
            nr, nc = r - dr * i, c - dc * i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        
        # print(f"  Current count in this direction: {count}")
        if count >= 5:
            return True
    return False

# 게임 초기화 함수
def reset_game():
    global board, turn, game_over, winner
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    turn = 1
    game_over = False
    winner = 0

# 그리기 함수
def draw_board():
    for i in range(BOARD_SIZE):
        # 가로줄
        pygame.draw.line(screen, BLACK, (GRID_START, GRID_START + i * CELL_SIZE), (GRID_END - CELL_SIZE, GRID_START + i * CELL_SIZE), 1)
        # 세로줄
        pygame.draw.line(screen, BLACK, (GRID_START + i * CELL_SIZE, GRID_START), (GRID_START + i * CELL_SIZE, GRID_END - CELL_SIZE), 1)

def draw_stones():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == 1: # 흑돌
                pygame.draw.circle(screen, BLACK, (GRID_START + c * CELL_SIZE, GRID_START + r * CELL_SIZE), CELL_SIZE // 2 - 2)
            elif board[r][c] == 2: # 백돌
                pygame.draw.circle(screen, WHITE, (GRID_START + c * CELL_SIZE, GRID_START + r * CELL_SIZE), CELL_SIZE // 2 - 2)

# 4. 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 좌클릭
                if not game_over: # 게임이 종료되지 않았을 때만 돌 놓기 허용
                    mouse_x, mouse_y = event.pos
                    # 클릭된 좌표를 격자 인덱스로 변환
                    col = round((mouse_x - GRID_START) / CELL_SIZE)
                    row = round((mouse_y - GRID_START) / CELL_SIZE)

                    # 오목판 범위 내에 있고, 빈 칸일 경우
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == 0:
                        board[row][col] = turn
                        
                        # 승리 판정
                        if check_win(row, col, turn):
                            game_over = True
                            winner = turn
                            print(f"플레이어 {winner} 승리!")
                        else:
                            turn = 3 - turn # 흑(1) -> 백(2), 백(2) -> 흑(1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # 'R' 키를 누르면 게임 재시작
                reset_game()

    # 화면 배경 채우기
    screen.fill(BOARD_COLOR)

    # 오목판 그리기
    draw_board()
    draw_stones()

    # 게임 상태 텍스트 표시
    font = pygame.font.Font(None, 36)
    if game_over:
        text = f"플레이어 {winner} 승리! (R키로 재시작)"
        text_color = BLACK
    else:
        current_player_text = "흑돌" if turn == 1 else "백돌"
        text = f"{current_player_text} 차례"
        text_color = BLACK
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, BOARD_MARGIN // 2))
    screen.blit(text_surface, text_rect)

    # 화면 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()
