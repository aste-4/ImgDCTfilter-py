from PIL import Image
import numpy as np
import random


def basis(k, n, N):  # DCT行列作成用基底関数
    a = np.sqrt(1/2) if k == 0 else 1
    c = np.sqrt(2/N)*a*np.cos((2*n+1)*k*np.pi/(2*N))
    return c


def DCTNxN(ImgArrayNxN):  # DCT変換
    N = ImgArrayNxN.shape[0]
    DCT = np.array([[basis(k, n, N) for n in range(N)] for k in range(N)])
    buf = np.zeros_like(ImgArrayNxN)
    np.dot(DCT, ImgArrayNxN, out=buf)
    np.dot(buf, DCT.T, out=buf)
    return buf


def IDCTNxN(DCTArrayNxN):  # IDCT変換
    N = DCTArrayNxN.shape[0]
    DCT = np.array([[basis(k, n, N) for n in range(N)] for k in range(N)])
    buf = np.zeros_like(DCTArrayNxN)
    np.dot(DCT.T, DCTArrayNxN, out=buf)
    np.dot(buf, DCT, out=buf)
    return buf


def LPF(DCTArray, border):
    for y in range(DCTArray.shape[0]):
        for x in range(DCTArray.shape[1]):
            DCTArray[y][x] = DCTArray[y][x] if x+y < border else 0.


def HPF(DCTArray, border):
    for y in range(DCTArray.shape[0]):
        for x in range(DCTArray.shape[1]):
            DCTArray[y][x] = DCTArray[y][x] if x+y > border else 0.


# ImgArrayをsizeの正方に分割して度合いborderのFilterをかける
def DCTsplitFilter(ImgArray, size, Filter, border):
    for y in range(0, ImgArray.shape[0]-size+1, size):
        for x in range(0, ImgArray.shape[1]-size+1, size):
            im_DCTNxN = DCTNxN(ImgArray[y:y+size, x:x+size])
            Filter(im_DCTNxN, border)
            im_IDCTNxN = IDCTNxN(im_DCTNxN)
            stack_h = im_IDCTNxN if x == 0 \
                else np.hstack((stack_h, im_IDCTNxN))
        im_IDCT = stack_h if y == 0 else np.vstack((im_IDCT, stack_h))
    return im_IDCT


def DCTFilter(ImgArrayNxN, Filter, border):
    return DCTsplitFilter(ImgArrayNxN, ImgArrayNxN.shape[0], Filter, border)


def addNoise(ImgArray, ratio=0.01):  # ごま塩ノイズ付加(default:1%)
    y, x = ImgArray.shape
    s = x*y
    for _ in range(np.int(np.round(s*ratio))):
        ImgArray[random.randrange(0, y)][random.randrange(0, x)] \
            = random.randrange(2)*255.


if __name__ == "__main__":
    # グレースケール化して読み込み、np.arrayに
    im_orig = np.array(Image.open('./lena.tiff').convert('L'), np.float)
    im_before = im_orig[:min(im_orig.shape), :min(im_orig.shape)]  # 正方化
    addNoise(im_before)  # ごま塩ノイズ付加
    # 処理前画像保存
    Image.fromarray(im_before.astype(np.uint8)).save('./before.tiff')

    # im_IDCT = DCTsplitFilter(im_before, 8, LPF, 8)
    im_IDCT = DCTFilter(im_before, LPF, im_before.shape[0]//2)

    # 処理後画像保存
    Image.fromarray(np.round(im_IDCT).astype(np.uint8)).save('./after.tiff')
