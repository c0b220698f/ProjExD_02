import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    bd_img = pg.Surface((20, 20))  # 練習1:爆弾Surface を作成
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  # 練習1:surfaceからrectを抽出
    bd_img.set_colorkey((0, 0, 0))  # 爆弾Surface の黒い部分を透明にする
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)  # 練習1:爆弾Surfaceをランダムな位置に配置

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, [900, 400])
        screen.blit(bd_img, bd_rct)  # 練習1:while ループの中でblit して，表示されるか確認
        pg.display.update()
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
