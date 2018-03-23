#encoding=utf-8
#create date 2016/5/22
#update 2016/9/21
#support iOS 10

# 可生成各个版本的icon和screenshot，以及android和ios，需要在python环境运行并导入图片
# action为icon时需要传入icon名称，当action为screenshot时可自动获取同级目录下的所有图片并生成相应版本的图片
# 参考自http://www.cocoachina.com/ios/20160922/17619.html
# 使用的 Pillow

#icon ios                  python tool.py icon mask.png ios
#screenshot ios            python tool.py screenshot ios


import os
import sys
from PIL import Image

iosSizes = ['20@1x','20@2x','20@3x','29@1x','29@2x','29@3x','40@1x','40@2x','40@3x','60@2x','60@3x','60@3x','76@1x','76@2x','167@1x']
androidSizes = [32,48,72,96,144,192]
androidNames = ['ldpi','mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']

sizesiOS = [(640,960),(640, 1136),(750, 1334),(1242, 2208),(1536, 2048),(2048, 2732)]
foldersiOS = ['iPhone4s','iPhone5','iPhone6','iPhone6plus','iPad','iPadLarge']

sizesAndroid = [(480,800),(720,1280),(1080,1920)]
foldersAndroid = ['480x800','720x1280','1080x1920']

def processIcon(filename,platform):
	icon = Image.open(filename).convert("RGBA")
	if icon.size[0] != icon.size[1]:
		print 'Icon file must be a rectangle!'
		return
	if platform == 'android':
		#安卓圆角
		mask = Image.open('mask.png')
		r,g,b,a = mask.split()
		icon.putalpha(a)
		if not os.path.isdir('androidIcon'):
			os.mkdir('androidIcon')
		index = 0
		for size in androidSizes:
			im = icon.resize((size,size),Image.BILINEAR)
			im.save('androidIcon/icon-'+ androidNames[index]+'.png')
			index = index + 1
	else:
		if not os.path.isdir('iosIcon'):
			os.mkdir('iosIcon')
		for size in iosSizes:
			originalSize = int(size.split('@')[0])#原始尺寸
			multiply = int(size.split('@')[1][0:1])#倍数
			im = icon.resize((originalSize*multiply,originalSize*multiply),Image.BILINEAR)
			im.save('iosIcon/icon'+size+'.png')
	print 'Congratulations!It\'s all done!'

def walk_dir(dir,platform):
	files = os.listdir(dir)
	for name in files:
		if name.split('.')[-1] == 'jpg' or name.split('.')[-1] == 'png':#处理jpg和png
			produceImage(name,platform)
	print 'Congratulations!It\'s all done!'

def produceImage(filename,platform):
	print 'Processing:' + filename
	img = Image.open(filename)
	index = 0
	sizes = sizesiOS
	folders = foldersiOS
	if platform == 'android':#默认ios，如果是安卓
		sizes = sizesAndroid
		folders = foldersAndroid
	for size in sizes:
		if not os.path.isdir(folders[index]):
			os.mkdir(folders[index])
		if img.size[0] > img.size[1]:#如果是横屏，交换坐标
			im = img.resize((size[1],size[0]),Image.BILINEAR)
			im.save(folders[index]+'/'+filename)
		else:
			im = img.resize(size,Image.BILINEAR)
			im.save(folders[index]+'/'+filename)
		index = index + 1

action = sys.argv[1]#action:icon or screenshot
if action == 'screenshot':	
	platform = sys.argv[2]#platform
	if platform == 'ios':
		walk_dir('./','ios')
	elif platform == 'android':
		walk_dir('./','android')
	else:
		print 'Hey,Platform can only be "ios" or "android" !'
elif action == 'icon':
	filename = sys.argv[2]#image filename
	platform = sys.argv[3]#platform
	if not os.path.exists(filename):
		print 'Hey,File Not Found!'
	else:
		if platform == 'ios':
			processIcon(filename,'ios')
		elif platform == 'android':
			processIcon(filename,'android')
		else:
			print 'Hey,Platform can only be "ios" or "android" !'
else:
	print 'Hey,action can only be "icon" or "screenshot" !'
