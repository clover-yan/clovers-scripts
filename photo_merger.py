from PIL import Image
import os
from time import sleep

def concatenate_images(folder_path, output_path):
    maxwidth = 0
    sumheight = 0
    images = []

    # 获取文件夹下所有图片文件
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            print(img_path)
            img = Image.open(img_path)
            maxwidth = max(maxwidth, img.size[0])
            sumheight += img.size[1]
            images.append(img)

    height = 0

    # 创建一张新的图片，高度为所有图片的高度之和
    result_image = Image.new('RGB', (maxwidth, sumheight))

    # 将所有图片按顺序上下拼接
    for i, img in enumerate(images):
        result_image.paste(img, (0, height))
        height += img.size[1]

    # 保存拼接后的图片
    result_image.save(output_path)


# 调用函数
path = input('请将存放图片的文件夹拖到此处：')
if path[0:2] == '& ':
    path = path[2:]
if path[0] == path[-1] == '"' or path[0] == path[-1] == "'":
    path = path[1:-1]
if path[-1] == '\\':
    path = path[:-1]
concatenate_images(path, f'{path}\\merged.png')
print('合并完成！5 秒后打开。')
sleep(5)

# 用默认程序显示合并后的文件
os.startfile(f'{path}\\merged.png')
