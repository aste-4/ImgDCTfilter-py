from PIL import Image
import numpy as np
import random


def basis(k, n, N):  # DCT行列作成用基底関数
    a = np.sqrt(1/2) if k == 0 else 1
    c = np.sqrt(2/N)*a*np.cos((2*n+1)*k*np.pi/(2*N))
    return c


def DCT8x8(ImgArray8x8):  # DCT変換
    N = 8
    DCT = np.array([[basis(k, n, N) for n in range(N)] for k in range(N)])
    buf = np.zeros((N, N))
    np.dot(DCT, ImgArray8x8, out=buf)
    np.dot(buf, DCT.T, out=buf)
    return buf


def IDCT8x8(DCTArray8x8):  # IDCT変換
    N = 8
    DCT = np.array([[basis(k, n, N) for n in range(N)] for k in range(N)])
    buf = np.zeros((N, N))
    np.dot(DCT.T, DCTArray8x8, out=buf)
    np.dot(buf, DCT, out=buf)
    return buf


def DCTsave(DCTArray8x8, filename):  # DCT変換結果の画像保存
    buf = np.round(np.abs(DCTArray8x8/8)).astype(np.uint8)
    Image.fromarray(buf).save(filename)


def LPF(DCTArray8x8):
    for y in range(8):
        for x in range(8):
            DCTArray8x8[y][x] = DCTArray8x8[y][x] if x+y < 8 else 0.


def HPF(DCTArray8x8):
    for y in range(8):
        for x in range(8):
            DCTArray8x8[y][x] = DCTArray8x8[y][x] if x+y > 1 else 0.


def addNoise(ImgArray):  # ごま塩ノイズ付加(1%)
    y, x = ImgArray.shape
    s = x*y
    for _ in range(s//100):
        ImgArray[random.randrange(0, y)][random.randrange(0, x)] \
            = random.randrange(2)*255.


if __name__ == "__main__":
    # グレースケール化して読み込み、np.arrayに
    im_before = np.array(Image.open('./lena.tiff').convert('L'), np.float)
    addNoise(im_before)  # ごま塩ノイズ付加
    # 処理前画像保存
    Image.fromarray(im_before.astype(np.uint8)).save('./before.tiff')

    # 8x8をim_beforeの左上から右へ順に切り出す
    for y in range(0, im_before.shape[0]-8+1, 8):
        for x in range(0, im_before.shape[1]-8+1, 8):
            im_DCT8x8 = DCT8x8(im_before[y:y+8, x:x + 8])
            LPF(im_DCT8x8)  # Filter processing
            im_IDCT8x8 = IDCT8x8(im_DCT8x8)
            stack_h = im_IDCT8x8 if x == 0 \
                else np.hstack((stack_h, im_IDCT8x8))
        im_IDCT = stack_h if y == 0 else np.vstack((im_IDCT, stack_h))
    # 処理後画像保存
    Image.fromarray(np.round(im_IDCT).astype(np.uint8)).save('./after.tiff')
