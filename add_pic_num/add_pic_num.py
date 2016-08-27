#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont

def add_pic_num(filename, output,num=1):
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('wqy-microhei.ttc', int(img.size[0]*0.3))
    position = (img.size[0]-img.size[0]/5, 5)
    # print position
    draw.text(position, str(num), font=font, fill=(255,0,0))
    img.save(output)

if __name__ == '__main__':
    add_pic_num('2.jpg', '4.jpg', 3)
