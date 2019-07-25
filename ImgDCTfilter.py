#!/usr/bin/env python
from PIL import Image
import numpy as np
import random
import argparse


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        default='./lena.tiff', help='Target image file name (default=\'./lena.tiff\')')
    parser.add_argument('-p', '--filter', default='LPF',
                        choices=['LPF', 'HPF'], help='Filter type (default=LPF)')
    parser.add_argument('-s', '--strength', type=float,
                        default=0.5, help='Filter strength (0~1) (default=0.5)')
    parser.add_argument('-n', '--noise', type=float,
                        help='Ratio of salt and pepper noise added before filter processing (0~1) (default=0)')
    return parser.parse_args()


def getImg(filename='./lena.tiff'):  # 画像読み込み&グレースケール化&正方化
    im_orig = np.array(Image.open(filename).convert('L'), np.float)
    print('Read {}'.format(filename))
    return im_orig[:min(im_orig.shape), :min(im_orig.shape)]  # 正方化(左上)


def saveImg(ImgArray, filename='./img.tiff'):  # 画像保存
    Image.fromarray(np.round(ImgArray).astype(np.uint8)).save(filename)
    print('Save {}'.format(filename))


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


def LPF(DCTArray, strength):
    if strength != 0:  # strengthが0の時は無処理
        border = np.int(
            np.floor((DCTArray.shape[0]+DCTArray.shape[1]-2)*(1-strength)))
        for y in range(DCTArray.shape[0]):
            for x in range(DCTArray.shape[1]):
                DCTArray[y][x] = DCTArray[y][x] if x+y < border else 0.


def HPF(DCTArray, strength):
    if strength != 0:  # strengthが0の時は無処理
        border = np.int(
            np.floor((DCTArray.shape[0]+DCTArray.shape[1]-2)*strength))
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
    args = parseArgs()
    print('filename:{}, filter:{}, strength:{}, noise:{}'.format(
        args.filename, args.filter, args.strength, args.noise))
    try:
        im_before = getImg(args.filename)  # 画像読み込み
    except FileNotFoundError:  # ファイル存在なし
        print('File not found')
        exit()

    if args.noise != None:
        addNoise(im_before, args.noise)  # ごま塩ノイズ付加
    saveImg(im_before, './before.tiff')  # 処理前画像保存

    filter_type = LPF if args.filter == 'LPF' else HPF if args.filter == 'HPF' else None
    im_after = DCTFilter(im_before, filter_type, args.strength)  # フィルタ処理

    saveImg(im_after, './after.tiff')  # 処理後画像保存
