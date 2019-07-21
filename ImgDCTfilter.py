from PIL import Image
import numpy as np


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


if __name__ == "__main__":
    # グレースケール化して読み込み、np.arrayに
    im_before = np.array(Image.open('./lena.tiff').convert('L'), np.float)
    print(im_before[:8, :8].astype(np.uint8))  # 左上8x8
    Image.fromarray(im_before[:8, :8].astype(np.uint8)).save('./before.tiff')
    im_DCT = DCT8x8(im_before[:8, :8])
    print(np.abs(im_DCT/8).astype(np.uint8))
    DCTsave(im_DCT, './DCT8x8.tiff')
    im_IDCT = IDCT8x8(im_DCT)
    print(np.round(im_IDCT).astype(np.uint8))
    Image.fromarray(np.round(im_IDCT).astype(np.uint8)).save('./after.tiff')

    # NxNを2次元np.arrayであるaの左上から右へ順に切り出す
    # for y in range(0,a.shape[0]-N+1,N):
    #     for x in range(0,a.shape[1]-N+1,N):
    #         a[y:y+N,x:x+N]
