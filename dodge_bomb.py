import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1600, 900

delta = {  # 練習3:移動用辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(obj_rct: pg.Rect):
    """
    引数はこうかとんRectか爆弾Rect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def kk_theta(key_tuple: tuple):  # 演習1
    """
    こうかとんの飛ぶ方向を切り替える関数
    引数key_tuple:押下キーに対する移動量の合計タプル
    戻り値:rotozoomしたこうかとんのSurface
    """
    kk_img = pg.image.load("ex02/fig/3.png")

    zero = pg.transform.rotozoom(kk_img, 0, 2.0)  # 0
    z45 = pg.transform.rotozoom(kk_img, 45, 2.0)  # 45
    mz45 = pg.transform.rotozoom(kk_img, -45, 2.0)  # -45
    z90 = pg.transform.rotozoom(kk_img, 90, 2.0)  # 90
    fz90 = pg.transform.flip(z90, True, False)  # 90左右反転
    mz90 = pg.transform.flip(z90, False, True)  # -90上下反転
    fz45 = pg.transform.flip(z45, True, False)  # 135(45左右反転)
    mfz45 = pg.transform.flip(mz45, True, False)  # 225(-45左右反転)
    fzero = pg.transform.flip(zero, True, False)  # 180
    theta_img = {
        (-5, 0): zero,
        (-5, 5): z45,
        (0, 5): fz90,
        (5, 5): fz45,
        (5, 0): fzero,
        (5, -5): mfz45,
        (0, -5): mz90,
        (-5, -5): mz45,
    }
    if key_tuple in theta_img:
        return theta_img[key_tuple]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)  # 練習3:練習３：こうかとんの初期座標を設定する

    """爆弾"""
    bd_img = pg.Surface((20, 20))  # 練習1:爆弾Surface を作成
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  # 練習1:surfaceからrectを抽出
    bd_img.set_colorkey((0, 0, 0))  # 爆弾Surface の黒い部分を透明にする
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)  # 練習1:爆弾Surfaceをランダムな位置に配置
    vx, vy = +5, +5  # 練習2:爆弾を移動させるための変数

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bd_rct):
            print("Game Over")
            return
        screen.blit(bg_img, [0, 0])
        """こうかとん"""
        # accs = [a for a in range(1, 11)]  # 加速度のリスト
        # for r in range(1, 11):
        #     bb_img = pg.Surface((20 * r, 20 * r))
        #     pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        #     bb_imgs.append(bb_img)

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 練習3:横方向の合計移動量
                sum_mv[1] += mv[1]  # 練習3縦方向の合計移動量
                kk_img = kk_theta(mv)
            kk_rct.move_ip(sum_mv[0], sum_mv[1])  # 練習3:移動させる
        if check_bound(kk_rct) != (True, True):  # 練習4:はみ出し判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)  # 演習3:移動後の座標に表示
        """爆弾"""
        bd_rct.move_ip(vx, vy)  # 練習2:爆弾Rect のmove_ip vx , vy メソッドで速度に応じて位置を移動させる
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 練習4:横方向にはみ出たら
            vx *= -1
        if not tate:  # 練習4:縦方向にはみ出たら
            vy *= -1
        screen.blit(bd_img, bd_rct)  # 練習1:while ループの中でblit して，表示されるか確認
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
