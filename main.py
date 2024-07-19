import time
from copy import deepcopy
import random
from pygame.locals import *
import json
import sys
import pygame
import pickle
import pygame.gfxdraw

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

gamestate = {
    "mode": "",
    'timelimit_value': 0,
    'style_now': "",
    'p_time': 0,
    'board': [[]],
    'theme': "",
    'time_now': 0,
    "diffculty": 2048
}

scorestate = {
    "rank_classic": [],
    'rank_timelimit': [],
    "max_score_classic": 0,
    "max_score_timelimit": 0
}


def winCheck(board, status, theme, text_col):
    global gamastate,scorestate
    if status != "PLAY":
        size = c["size"]
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        score_now = scorecal()
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))
        if status == "WIN":
            msg = "YOU WIN!"
            if gamestate['mode'] == "classic":
                scorestate["rank_classic"].append(score_now)
            elif gamestate['mode'] == "timelimit":
                scorestate["rank_timelimit"].append(score_now)
        elif status == "LOSE_TIME":
            msg = "TIME OUT!"
            if gamestate['mode'] == "classic":
                scorestate["rank_classic"].append(score_now)
            elif gamestate['mode'] == "timelimit":
                scorestate["rank_timelimit"].append(score_now)
        else:
            msg = "GAME OVER!"
            if gamestate['mode'] == "classic":
                scorestate["rank_classic"].append(score_now)
            elif gamestate['mode'] == "timelimit":
                scorestate["rank_timelimit"].append(score_now)
        screen.blit(my_font.render(msg, 1, text_col), (180, 210))
        screen.blit(my_font.render(
            "Play again? (y/ n)", 1, text_col), (100, 255))
        screen.blit(my_font.render("OR return to MENU(r)", 1, text_col), (90, 305))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    ranksaver()
                    save(scorestate,"score_state")
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:
                    ranksaver()
                    board = newGame(theme, text_col)
                    return (board, "PLAY")
                if event.type == pygame.KEYDOWN and event.key == K_r:
                    ranksaver()
                    showMenu()
    return (board, status)


def newGame(theme, text_col):
    global gamestate
    gamestate["p_time"] = time.time()
    gamestate['board'] = [[0] * 4 for _ in range(4)]
    #gamestate['board'] = [[8] * 4 ,[64] * 4, [512] * 4, [1024] * 4]
    
    screen.blit(my_font.render("NEW GAME!", 1, text_col), (180, 210))
    display(gamestate["board"], theme)
    #display_board()
    time.sleep(1)
    gamestate['board'] = fillTwoOrFour(gamestate["board"], iter=2)
    display(gamestate["board"], theme)
    #display_board()
    return gamestate['board']


def restart(board, theme, text_col):
    #重开
    global scorestate
    s = pygame.Surface((c["size"], c["size"]), pygame.SRCALPHA)
    s.fill(c["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render(
            "Play again? (y/ n)", 1, text_col), (100, 255))
    screen.blit(my_font.render("OR return to MENU(r)", 1, text_col), (90, 305))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                ranksaver()
                save(scorestate,"score_state")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                ranksaver()
                board = newGame(theme, text_col)
                return board
            if event.type == pygame.KEYDOWN and event.key == K_r:
                showMenu()
            if event.type == pygame.KEYDOWN and event.key == K_n:
                ranksaver()
                save(scorestate,"score_state")
                pygame.quit()
                sys.exit()
def scorecal():
    s = 0
    for i in gamestate["board"]:
        for j in i:
            s += j
    s *= 2
    return s


def display_board():
    global gamestate, scorestate
    s = scorecal()
    font = pygame.font.SysFont(c["font"], 25, bold = 1)
    if gamestate['mode'] == "timelimit":
        time_now = time.time()
        counter = Button(tuple(c["colour"]["light"]["64"]),
                            20, 55, 205, 75, f"COUNTDOWN {int(gamestate['timelimit_value'] * 60 - (time_now - gamestate['p_time']) + 1)}S") #timelimit_value - (time_now - p_time)
        pygame.draw.rect(screen, (205, 193, 180), (15, 50, 215, 85), 0, border_radius = 20)
        counter.draw(screen, BLACK, font)
        gamestate["time_now"] = time_now
    else:
        counter = Button(tuple(c["colour"]["light"]["4"]),
                            20, 55, 365, 75, f"You have unlimited time..")
        pygame.draw.rect(screen, (205, 193, 180), (15, 50, 375, 85), 0, border_radius = 20)
        counter.draw(screen, BLACK, font)
    
    #pygame.draw.rect(screen, (205, 193, 180), (415, 20, 215, 130), 0, border_radius = 20)
    #scoreboard.draw(screen, BLACK, font)

    draw_rounded_rect(screen, pygame.Rect(465, 55, 180, 100), (187,173,160), 7)

    nowscore1 = font.render("SCORE", 1, (238,228,218))
    nowscore2 = font.render(f"{s}", 1, (249,246,242))
    
    if gamestate["mode"] == "classic":
        if(s > scorestate["max_score_classic"]):
            scorestate["max_score_classic"] = s
        maxscore1 = font.render("BEST", 1, (238,228,218))
        maxscore2 = font.render(str(scorestate["max_score_classic"]), 1, (249,246,242))

    elif gamestate["mode"] == "timelimit":
        if(s > scorestate["max_score_timelimit"]):
            scorestate["max_score_timelimit"] = s
        maxscore1 = font.render("BEST", 1, (238,228,218))
        maxscore2 = font.render(str(scorestate["max_score_timelimit"]), 1, (249,246,242))
    screen.blit(nowscore1, (485, 70))
    screen.blit(nowscore2, (580, 70))
    screen.blit(maxscore1, (485, 110))
    screen.blit(maxscore2, (580, 110))

    font = pygame.font.SysFont(c["font"], 25, bold = 1)
    draw_rounded_rect(screen, pygame.Rect(465, 190, 180, 455), (143,122,102), 7)

    #pygame.draw.rect(screen, (205, 193, 180), (455, 180, 190, 460), 0, border_radius = 12)
    #pygame.draw.rect(screen, (239, 213, 117,190), (460, 185, 180, 450), 0, border_radius = 12)

    screen.blit(font.render("Ranking List", True, (249,246,242)), (480,210))
    if gamestate['mode'] == "timelimit":
        scorestate['rank_timelimit'].sort(reverse = True)
        for i in range(0,10):
            try:    
                screen.blit(font.render(f"{scorestate['rank_timelimit'][i]}", True, (249,246,242)), (510, 250 + i * 30))
            except:
                pass
        
    elif gamestate['mode'] == "classic":
        scorestate['rank_classic'].sort(reverse = True)
        for i in range(0,10):
            try:    
                screen.blit(font.render(f"{scorestate['rank_classic'][i]}", True, (249,246,242)), (510, 250 + i * 30))
            except:
                pass
    

def ranksaver():
    global scorestate, gamestate
    if gamestate["mode"] == "classic":
        s = scorecal()
        if s == 8:
            return
        scorestate["rank_classic"].append(s)
    elif gamestate["mode"] == "timelimit":
        s = scorecal()
        if s == 8:
            return
        scorestate["rank_timelimit"].append(s)


def draw_rounded_rect(surface, rect, color, corner_radius, shadow=False, shadow_color=(128, 128, 128), offset=(5, 5)):
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError("Width and height must be > 2 * corner radius")
    
    if shadow:
        shadow_rect = pygame.Rect(rect)
        shadow_rect.topleft = (rect.topleft[0] + offset[0], rect.topleft[1] + offset[1])
        draw_rounded_rect(surface, shadow_rect, shadow_color, corner_radius)

    pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
    
    pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
    
    pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    
    pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)
    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


def display(board, theme):
    global gamestate
    #显示主函数
    screen.fill((250,248,239)) # tuple(c["colour"][theme]["background"])
    #background_image = pygame.image.load('background.jpg').convert() #绘制背景
    #background_image = pygame.transform.scale(background_image, (650, 650))
    #screen.blit(background_image, (0, 0)) 
    box = (c["size"] - 200) // 4
    padding = c["padding"]
    draw_rounded_rect(screen, pygame.Rect(4.5, 190, 456, 456), (187, 173, 160), 3)
    display_board()

    for i in range(4):
        for j in range(4):
            #绘制阴影
            x = 0 + j * box + padding + 8
            y = 200 + i * box + padding - 8
            w = box - 2 * padding
            h = box - 2 * padding
            colour = tuple(c["colour"][theme][str(board[i][j])])
            # colourbehind = tuple(c["colour"][theme][str(board[i][j]) + "behind"])
            draw_rounded_rect(screen, pygame.Rect(x, y, w, h), colour, 3) #, shadow=True, shadow_color=colourbehind, offset=(3, 2))

            '''
            colour = tuple(c["colour"][theme][str(board[i][j]) + "behind"])
            pygame.draw.rect(screen, colour, (2 + j * box + padding,
                                              202 + i * box + padding,
                                              0 + box - 2 * padding,
                                              0 + box - 2 * padding), 0, border_radius = 8)

            colour = tuple(c["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (0 + j * box + padding,
                                              200 + i * box + padding,
                                              0 + box - 2 * padding,
                                              0 + box - 2 * padding), 0, border_radius = 8)
            '''

            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"][theme]["dark"])
                else:
                    text_colour = tuple(c["colour"][theme]["light"])
                
                if gamestate['style_now'] == "朝代模式":
                    screen.blit(my_font.render("{:>4}".format(c["words"][
                        str(board[i][j])]), 1, text_colour),
                        (-32 + j * box + 1 * padding - len("{:>4}".format(c["words"][
                        str(board[i][j])])), 192 + i * box + 7 * padding))
                else:
                    if(board[i][j] <= 1000):
                        nm_font = pygame.font.SysFont(c["font_number"], c["font_size"], bold=True)
                        screen.blit(nm_font.render("{:>4}".format(board[i][j]), 1, text_colour),
                                    (-18 +  j * box + 2.5 * padding + 8, 193 + i * box + 7 * padding - 8))
                    else:
                        nm_font = pygame.font.SysFont(c["font_number"], c["font_size"] - 10, bold=True)
                        screen.blit(nm_font.render("{:>4}".format(board[i][j]), 1, text_colour),
                                    (-7 +  j * box + 2.5 * padding + 8, 196 + i * box + 7 * padding - 8))

                    #screen.blit(nm_font.render("{:>4}".format(board[i][j]), 1, text_colour),
                    #    (-5 + j * box + 2.5 * padding - 0.7 * len(str(board[i][j])), 200 + i * box + 7 * padding))

    pygame.display.update()


def playGame():
    #主函数
    global gamestate, scorestate
    previoustime = time.time()
    status = "PLAY"
    if gamestate["theme"] == "light":
        text_col = tuple(c["colour"][gamestate["theme"]]["dark"])
    else:
        text_col = WHITE
    gamestate["board"] = newGame(gamestate["theme"], text_col)
    

    #loop
    while True:
        status = checkGameStatus(gamestate["board"], gamestate["difficulty"])
        (gamestate['board'], status) = winCheck(gamestate["board"], status, gamestate["theme"], text_col)
        nowtime = time.time()
        if nowtime - previoustime >= 0.5:
            display_board()
            pygame.display.update()
            previoustime = nowtime

        for event in pygame.event.get():

            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                ranksaver()
                save(scorestate,"score_state")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: #n键重开
                if event.key == pygame.K_n:
                    gamestate['board'] = restart(gamestate['board'], gamestate["theme"], text_col)
                if str(event.key) in c["keys"]:
                    key = c["keys"][str(event.key)]

                elif event.key == pygame.K_UP: #检测箭头方向键
                    key = "w"
                elif event.key == pygame.K_DOWN:
                    key = "s"
                elif event.key == pygame.K_LEFT:
                    key = "a"
                elif event.key == pygame.K_RIGHT:
                    key = "d"
                else:
                    continue

                new_board = move(key, deepcopy(gamestate['board']))

                if new_board != gamestate['board']:
                    gamestate['board'] = fillTwoOrFour(new_board)
                    status = checkGameStatus(gamestate['board'], gamestate["difficulty"])
                    (gamestate['board'], status) = winCheck(gamestate['board'], status, gamestate["theme"], text_col)
                    display(gamestate['board'], gamestate["theme"])
                    #display_board()

def move(direction, board):

    if direction == "w":
        return moveUp(board)
    elif direction == "s":
        return moveDown(board)
    elif direction == "a":
        return moveLeft(board)
    elif direction == "d":
        return moveRight(board)


def checkGameStatus(board, max_tile=2048): #检查游戏状态
    global gamestate
    if gamestate['mode'] == "timelimit":
        time_now = time.time()
        if(time_now - int(gamestate['p_time']) >= gamestate['timelimit_value'] * 60):
            return "LOSE_TIME"
    flat_board = [cell for row in board for cell in row]
    if max_tile in flat_board:
        return "WIN"

    for i in range(4):
        for j in range(4):
            if j != 3 and board[i][j] == board[i][j+1] or \
                    i != 3 and board[i][j] == board[i + 1][j]:
                return "PLAY"

    if 0 not in flat_board:
        return "LOSE"
    else:
        return "PLAY"



def fillTwoOrFour(board, iter=1): #随机填充2或4
    for _ in range(iter):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
        while(board[a][b] != 0):
            a = random.randint(0, 3)
            b = random.randint(0, 3)
        if sum([cell for row in board for cell in row]) in (0, 2):
            board[a][b] = 2
        else:
            board[a][b] = random.choice((2, 4))
    return board


def moveLeft(board):

    shiftLeft(board)

    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
                j = 0

    shiftLeft(board)
    return board

def moveUp(board):

    board = rotateLeft(board)
    board = moveLeft(board)
    board = rotateRight(board)
    return board

def moveRight(board):

    shiftRight(board)

    for i in range(4):
        for j in range(3, 0, -1):
            if board[i][j] == board[i][j - 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j - 1] = 0
                j = 0
    shiftRight(board)
    return board


def moveDown(board):
    board = rotateLeft(board)
    board = moveLeft(board)
    shiftRight(board)
    board = rotateRight(board)
    return board


def shiftLeft(board):

    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = nums
        board[i].extend([0] * (4 - count))


def shiftRight(board):

    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = [0] * (4 - count)
        board[i].extend(nums)


def rotateLeft(board):
    b = [[board[j][i] for j in range(4)] for i in range(3, -1, -1)]
    return b


def rotateRight(board):
    b = rotateLeft(board)
    b = rotateLeft(b)
    return rotateLeft(b)

def save(game_state,file_name): #保存游戏参数
    with open(f'{file_name}.pickle', 'wb') as f:
        pickle.dump(game_state, f)

def load_game(file_name):
    with open(f'{file_name}.pickle', 'rb') as f:
        game_state = pickle.load(f)
    return game_state


class Button():
    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, text_col, font):
        draw_rounded_rect(win, pygame.Rect(self.x, self.y, 
                                        self.width, self.height), self.colour, 20)
        
        #drawRoundRect(win, self.colour, (self.x, self.y,
        #                                 self.width, self.height))

        if self.text != "":
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #判断是否选中按钮
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

def showMenu():
    global gamestate, scorestate
    try:
        scorestate = load_game("score_state")
    except:
        pass
    windows = 0
    light_theme = Button(
        tuple(c["colour"]["light"]["2048"]), 180, 270, 95, 75, "light")
    dark_theme = Button(
        tuple(c["colour"]["dark"]["2048"]), 290, 270, 95, 75, "dark")
    
    gamestate["theme"] = ""
    theme_selected = False
    
    _2048 = Button(tuple(c["colour"]["light"]["64"]),
                  510, 370, 95, 75, "2048")
    _1024 = Button(tuple(c["colour"]["light"]["2048"]),
                  400, 370, 95, 75, "1024")
    _512 = Button(tuple(c["colour"]["light"]["2048"]),
                  290, 370, 95, 75, "512")
    _256 = Button(tuple(c["colour"]["light"]["2048"]),
                  180, 370, 95, 75, "256")

    gamestate["timelimit_value"] = 0
    timelimit_selected = False

    mins1 = Button(tuple(c["colour"]["light"]["2048"]),
                  180, 470, 95, 75, "1分钟")
    mins3 = Button(tuple(c["colour"]["light"]["2048"]),
                  290, 470, 95, 75, "3分钟")
    mins5 = Button(tuple(c["colour"]["light"]["2048"]),
                  400, 470, 95, 75, "5分钟")
    mins8 = Button(tuple(c["colour"]["light"]["2048"]),
                  510, 470, 95, 75, "8分钟")

    gamestate["difficulty"] = 0
    diff_selected = False

    mode_classic = Button(tuple(c["colour"]["light"]["2048"]),
                  140, 400, 95, 75, "经典模式")
    mode_timelimit = Button(tuple(c["colour"]["light"]["2048"]),
                  260, 400, 95, 75, "限时挑战")
    mode_vs = Button(tuple(c["colour"]["light"]["2048"]),
                  380, 400, 95, 75, "联机对战")
    gamestate["mode"] = ""
    mode_selected = False

    _continue = Button(tuple(c["colour"]["light"]["2048"]),
                  260, 560, 125, 75, "下一页")


    play = Button(tuple(c["colour"]["light"]["2048"]),
                  260, 560, 125, 75, "开始游戏")
    
    gamestate['style_now'] = "数字模式"
    style1 = Button(tuple(c["colour"]["light"]["64"]),
                  140, 300, 95, 75, "数字模式")
    style2 = Button(tuple(c["colour"]["light"]["2048"]),
                  260, 300, 95, 75, "朝代模式")
    


    
    while True:
        #background_image = pygame.image.load('background.jpg').convert() #菜单界面背景
        #background_image = pygame.transform.scale(background_image, (650, 650))
        #screen.blit(background_image, (0, 0)) 
        screen.fill((187,173,160)) #
        screen.blit(pygame.transform.smoothscale(
            pygame.image.load("images/icon.ico"), (200, 200)), (225, 20))
        font = pygame.font.SysFont(c["font"], 25, bold=True)
        font3 = pygame.font.SysFont(c["font"], 17, bold=True)

        if windows == 0:
            mode_text = font.render("Mode: ", 1, WHITE)
            screen.blit(mode_text, (65, 425))
            mode_classic.draw(screen, BLACK, font3)
            mode_timelimit.draw(screen, BLACK, font3)
            mode_vs.draw(screen, BLACK, font3)
            _continue.draw(screen, BLACK, font3)
            style1.draw(screen, BLACK, font3)
            style2.draw(screen, BLACK, font3)
            pygame.display.update()
            
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):#按q退出
                    ranksaver()
                    save(scorestate,"score_state")
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if mode_classic.isOver(pos):
                        mode_classic.colour = tuple(c["colour"]["light"]["64"])
                        mode_timelimit.colour = tuple(c["colour"]["light"]["2048"])
                        mode_vs.colour = tuple(c["colour"]["light"]["2048"])
                        gamestate['mode'] = "classic"
                        mode_selected = True

                    if mode_timelimit.isOver(pos):

                        mode_classic.colour = tuple(c["colour"]["light"]["2048"])
                        mode_timelimit.colour = tuple(c["colour"]["light"]["64"])
                        mode_vs.colour = tuple(c["colour"]["light"]["2048"])
                        gamestate['mode'] = "timelimit"
                        mode_selected = True

                    if mode_vs.isOver(pos):
                        mode_classic.colour = tuple(c["colour"]["light"]["2048"])
                        mode_timelimit.colour = tuple(c["colour"]["light"]["2048"])
                        mode_vs.colour = tuple(c["colour"]["light"]["64"])
                        gamestate['mode'] = "vs"
                        mode_selected = True

                    if style1.isOver(pos):
                        style1.colour = tuple(c["colour"]["light"]["64"])
                        style2.colour = tuple(c["colour"]["light"]["2048"])
                        gamestate['style_now'] = "数字模式"
                    if style2.isOver(pos):
                        style2.colour = tuple(c["colour"]["light"]["64"])
                        style1.colour = tuple(c["colour"]["light"]["2048"])
                        gamestate['style_now'] = "朝代模式"
                    if _continue.isOver(pos):
                        if mode_selected:
                            windows = 1

                #按钮悬浮变色
                if event.type == pygame.MOUSEMOTION:
                    if not mode_selected:
                        if mode_classic.isOver(pos):
                            mode_classic.colour = tuple(c["colour"]["light"]["64"])
                        else:
                            mode_classic.colour = tuple(c["colour"]["light"]["2048"])
                        
                        if mode_timelimit.isOver(pos):
                            mode_timelimit.colour = tuple(c["colour"]["light"]["64"])
                        else:
                            mode_timelimit.colour = tuple(c["colour"]["light"]["2048"])

                        if mode_vs.isOver(pos):
                            mode_vs.colour = tuple(c["colour"]["light"]["64"])
                        else:
                            mode_vs.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _continue.isOver(pos):
                        _continue.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _continue.colour = tuple(c["colour"]["light"]["2048"])
            

        else:
            theme_text = font.render("主题: ", 1, WHITE)
            screen.blit(theme_text, (100, 295))

            diff_text = font.render("难度: ", 1, WHITE)
            screen.blit(diff_text, (100, 390))

            time_text = font.render("限时: ", 1, WHITE)
                
            #绘制按钮
            light_theme.draw(screen, BLACK, font3)
            dark_theme.draw(screen, (197, 255, 215), font3)
            _2048.draw(screen, BLACK, font3)
            _1024.draw(screen, BLACK, font3)
            _512.draw(screen, BLACK, font3)
            _256.draw(screen, BLACK, font3)
            play.draw(screen, BLACK, font3)
            if gamestate['mode'] == "timelimit":
                mins1.draw(screen, BLACK, font3)
                mins3.draw(screen, BLACK, font3)
                mins5.draw(screen, BLACK, font3)
                mins8.draw(screen, BLACK, font3)
                screen.blit(time_text, (100, 490))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                ranksaver()
                save(scorestate,"score_state")
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN: #按钮被按下
                if light_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                    light_theme.colour = tuple(c["colour"]["light"]["64"])
                    gamestate['theme'] = "light"
                    theme_selected = True

                
                elif dark_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["background"])
                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['theme'] = "dark"
                    theme_selected = True
                
                elif _2048.isOver(pos):
                    _2048.colour = tuple(c["colour"]["light"]["64"])
                    _1024.colour = tuple(c["colour"]["light"]["2048"])
                    _512.colour = tuple(c["colour"]["light"]["2048"])
                    _256.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['difficulty'] = 2048
                    diff_selected = True
                
                elif _1024.isOver(pos):
                    _1024.colour = tuple(c["colour"]["light"]["64"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    _512.colour = tuple(c["colour"]["light"]["2048"])
                    _256.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['difficulty'] = 1024
                    diff_selected = True
                
                elif _512.isOver(pos):
                    _512.colour = tuple(c["colour"]["light"]["64"])
                    _1024.colour = tuple(c["colour"]["light"]["2048"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    _256.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['difficulty'] = 512
                    diff_selected = True
                
                elif _256.isOver(pos):
                    _256.colour = tuple(c["colour"]["light"]["64"])
                    _1024.colour = tuple(c["colour"]["light"]["2048"])
                    _512.colour = tuple(c["colour"]["light"]["2048"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['difficulty'] = 256
                    diff_selected = True

                elif mins1.isOver(pos):
                    mins1.colour = tuple(c["colour"]["light"]["64"])
                    mins3.colour = tuple(c["colour"]["light"]["2048"])
                    mins5.colour = tuple(c["colour"]["light"]["2048"])
                    mins8.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['timelimit_value'] = 1
                    timelimit_selected = True
                elif mins3.isOver(pos):
                    mins3.colour = tuple(c["colour"]["light"]["64"])
                    mins1.colour = tuple(c["colour"]["light"]["2048"])
                    mins5.colour = tuple(c["colour"]["light"]["2048"])
                    mins8.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['timelimit_value'] = 3
                    timelimit_selected = True
                elif mins5.isOver(pos):
                    mins5.colour = tuple(c["colour"]["light"]["64"])
                    mins3.colour = tuple(c["colour"]["light"]["2048"])
                    mins1.colour = tuple(c["colour"]["light"]["2048"])
                    mins8.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['timelimit_value'] = 5
                    timelimit_selected = True
                elif mins8.isOver(pos):
                    mins8.colour = tuple(c["colour"]["light"]["64"])
                    mins3.colour = tuple(c["colour"]["light"]["2048"])
                    mins5.colour = tuple(c["colour"]["light"]["2048"])
                    mins1.colour = tuple(c["colour"]["light"]["2048"])
                    gamestate['timelimit_value'] = 8
                    timelimit_selected = True

                elif play.isOver(pos):
                    if theme_selected and diff_selected and ((gamestate['mode'] == "timelimit" and timelimit_selected)
                                                                                    or gamestate['mode'] != "timelimit"):
                        playGame()



            if event.type == pygame.MOUSEMOTION: #鼠标悬浮变色
                if not theme_selected:
                    if light_theme.isOver(pos):
                        light_theme.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if dark_theme.isOver(pos):
                        dark_theme.colour = tuple(c["colour"]["dark"]["background"])
                    else:
                        dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                
                if not diff_selected:
                    if _2048.isOver(pos):
                        _2048.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _2048.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _1024.isOver(pos):
                        _1024.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _1024.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _512.isOver(pos):
                        _512.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _512.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _256.isOver(pos):
                        _256.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _256.colour = tuple(c["colour"]["light"]["2048"])
                if not timelimit_selected and gamestate['mode'] == "timelimit":
                    
                    if mins1.isOver(pos):
                        mins1.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        mins1.colour = tuple(c["colour"]["light"]["2048"])
                    if mins3.isOver(pos):
                        mins3.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        mins3.colour = tuple(c["colour"]["light"]["2048"])
                    if mins5.isOver(pos):
                        mins5.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        mins5.colour = tuple(c["colour"]["light"]["2048"])
                    if mins8.isOver(pos):
                        mins8.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        mins8.colour = tuple(c["colour"]["light"]["2048"])

                if play.isOver(pos):
                    play.colour = tuple(c["colour"]["light"]["64"])
                else:
                    play.colour = tuple(c["colour"]["light"]["2048"])


if __name__ == "__main__":
    #加载json
    c = json.load(open("constants.json", "r", encoding='utf-8'))

    pygame.init()
    screen = pygame.display.set_mode(
        (c["size"], c["size"]))
    pygame.display.set_caption("2048 by 无言以队")

    #任务栏图标绘制ico
    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
    nm_font = pygame.font.SysFont(c["font_number"], c["font_size"] - 10, bold=True)
    showMenu()
