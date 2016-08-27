from PIL import Image

res = [1136, 640]

def reset_size(img, res):
    img_size = img.size
    if img_size[0] > res[0] or img_size[1] > res[1]:
        