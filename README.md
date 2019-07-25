# ImgDCTfilter

## Description
画像に対してDCTによるHPF/LPFをかける。  
処理前画像(./before.tiff)と処理後画像(./after.tiff)を保存する。

## Demo
./lena.tiffにごま塩ノイズを付加した画像にLPF処理を行う場合
```
./ImgDCTfilter.py -s .75 -n .01
```
生成画像 (左:before.tiff, 右:after.tiff)  
<img src="https://user-images.githubusercontent.com/34529552/61883522-95087e00-af35-11e9-99db-7f21ab20e7d5.jpg" width="45%">
<img src="https://user-images.githubusercontent.com/34529552/61883599-b1a4b600-af35-11e9-9243-2db4a0b866b4.jpg" width="45%">

## Requirement
- numpy
- pillow

## Usage
```
usage: ImgDCTfilter.py [-h] [-f FILENAME] [-p {LPF,HPF}] [-s STRENGTH]
                       [-n NOISE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Target image file name (default='./lena.tiff')
  -p {LPF,HPF}, --filter {LPF,HPF}
                        Filter type (default=LPF)
  -s STRENGTH, --strength STRENGTH
                        Filter strength (0~1) (default=0.5)
  -n NOISE, --noise NOISE
                        Ratio of salt and pepper noise added before filter
                        processing (0~1) (default=0)
```