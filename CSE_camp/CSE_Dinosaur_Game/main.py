import pygame  # 導入pygame庫
import sys  # 導入sys庫
import random
import time
import math



# pygame初始化
pygame.init()

# 設定視窗
width = 1138
height = 540
pygame.display.set_caption("CSE Dinosaur Game")    # 設置視窗標題
screen = pygame.display.set_mode((width, height))    # 設置視窗大小

# 設置圖像的幀數率
FPS = 100

# 石頭和背景的移動速度
speed = -2


# 設置字體和文字
font_big = pygame.font.SysFont("Californian FB", 60)
font_small = pygame.font.SysFont("華康兒風體W4", 40)
game_over = font_big.render("Game Over", True, "#000000")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("conlon.png")
        self.surf = pygame.Surface((50, 70))
        self.rect = self.surf.get_rect(center=(190, 445))
        print(self.rect.top)
        print(self.rect.bottom)
        print(self.rect.left)
        print(self.rect.right)

        self.jumpState = 0
        self.jumpSpeed = 0
        self.jumpMove = 0

    def move(self):
        if self.jumpState == 1:
            self.jumpMove = self.jumpSpeed
            self.jumpSpeed += 0.25
            self.jumpMove = (self.jumpMove + self.jumpSpeed)
            if self.jumpSpeed >= 10:
                self.jumpState = 0
            self.rect.move_ip((0, self.jumpMove))

        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                self.jumpState = 1
                self.jumpSpeed = -10
        print("palyer")
        print(self.rect.top)
        print(self.rect.bottom)
        print(self.rect.left)
        print(self.rect.right)
        print("playerrrrr")


class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("stone.png")
        #self.surf = pygame.Surface((60, 35))

        self.rect = self.img.get_rect(center=(1220, 470))


    def move(self):

        global others_speed
        self.rect.move_ip((speed, 0))
        print("stone")
        print(self.rect.top)
        print(self.rect.bottom)
        print(self.rect.left)
        print(self.rect.right)
        print("stonesssssssssssss")
        if self.rect.x <= -82:
            self.rect.x = 1220 + random.randint(0, 200)


class Background():
    def __init__(self):
        self.bg_width = 1138
        x, y = (width/2, height/2)
        self.background_0 = pygame.image.load("BG_00.bmp")
        self.rect_0 = self.background_0.get_rect(center=(x, y))
        self.background_1 = pygame.image.load("BG_01.bmp")
        self.rect_1 = self.background_1.get_rect(center=(x + self.bg_width, y))

    def move(self):
        global others_speed
        if self.rect_0.x <= -self.bg_width:
            self.rect_0.move_ip(self.bg_width * 2, 0)
        else:
            self.rect_0.move_ip(speed, 0)
        if self.rect_1.x <= -self.bg_width:
            self.rect_1.move_ip(self.bg_width * 2, 0)
        else:
            self.rect_1.move_ip(speed, 0)


# 實體化物件
player = Player()
stone = Stone()
background = Background()


# 定義 stone 精靈組
stones = pygame.sprite.Group()
stones.add(stone)

# 所有精靈放
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(stone)


# 主程式
def main():
    global speed

    CLOCK = pygame.time.Clock()

    # 分數
    SCORE = 0

    # 顯示
    while True:
        # 增加分數
        SCORE += 0.1
        # 增加速度
        speed = -2 - 0.5 * math.log2(SCORE)

        # 背景渲染
        screen.blit(background.background_0, background.rect_0)
        screen.blit(background.background_1, background.rect_1)
        # 背景移動
        background.move()
        scores = font_small.render(f"score: {str(int(SCORE))}", True, "#000000")
        screen.blit(scores, (50, 50))

        # 精靈
        for sprite in all_sprites:
            # 精靈移動
            sprite.move()
            # 精靈渲染
            screen.blit(sprite.img, sprite.rect)

            pygame.draw.line(screen, (255, 0, 0), (sprite.rect.right, sprite.rect.top), (sprite.rect.right, sprite.rect.bottom))
            pygame.draw.line(screen, (0, 0, 255), (sprite.rect.left, sprite.rect.top),
                             (sprite.rect.left, sprite.rect.bottom))
            pygame.draw.line(screen, (0, 255, 0), (sprite.rect.right, sprite.rect.top),
                             (sprite.rect.left, sprite.rect.top))
            pygame.draw.line(screen, (0, 255, 0), (sprite.rect.right, sprite.rect.bottom),
                             (sprite.rect.left, sprite.rect.bottom))


        for event in pygame.event.get():  # 從事件佇列中獲取事件
            if event.type == pygame.QUIT:  # 若事件為"退出"
                pygame.quit()  # 退出pygame
                sys.exit()  # 退出系統

        pygame.display.update()  # 更新繪圖視窗的內容

        # 碰撞偵測
        if pygame.sprite.spritecollide(player, stones, False):
            print("collide")
            pygame.mixer.Sound("collision.wav").play()
            print("sleep")
            time.sleep(1)
            print("sleep over")

            screen.fill("#ff0000")
            screen.blit(game_over, (450, 150))
            scores_end = font_big.render("SCORE: "+str(int(SCORE)), True, "#000000")
            screen.blit(scores_end, (450, 250))

            pygame.display.update()
            time.sleep(5)

            pygame.quit()
            sys.exit()

        CLOCK.tick(FPS)  # 依照指定速率CLOCK刷新畫面，若來沒到時間就不刷新



if __name__ == '__main__':
    main()