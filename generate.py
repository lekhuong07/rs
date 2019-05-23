from PIL import Image, ImageChops, ImageDraw
import cv2, glob, os, requests
import numpy as np

def delete_background(path):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    lower_white = np.array([220, 220, 220], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(img, lower_white, upper_white)  # could also use threshold
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
    3, 3)))  # "erase" the small white points in the resulting mask
    mask = cv2.bitwise_not(mask)  # invert mask

    # load background (could be an image too)
    bk = np.full(img.shape, 255, dtype=np.uint8)  # white bk

    # get masked foreground
    fg_masked = cv2.bitwise_and(img, img, mask=mask)

    # get masked background, mask must be inverted
    mask = cv2.bitwise_not(mask)
    bk_masked = cv2.bitwise_and(bk, bk, mask=mask)

    # combine masked foreground and masked background
    final = cv2.bitwise_or(fg_masked, bk_masked)
    mask = cv2.bitwise_not(mask)  # revert mask to origina


def generate_picture(path):
    images = [file for file in glob.glob(path)]
    images.sort()
    print(images)

    img0s   = Image.open(images[0])
    w,h    = img0s.size

    img0   = Image.new('RGB', (w,h))

    #flag
    img1 = Image.open(images[1])
    width, height = img1.size
    img1 = img1.resize((int(width / 3.6), int(height / 3.6)))
    img0.paste(img1, (398, 165))

    img2 = Image.open(images[3])
    width, height = img2.size
    img2 = img2.resize((int(width / 3.5), int(height / 3.5)))
    img0.paste(img2, (10, 12))

    img0 = ImageChops.lighter(img0, img0s)

    # Create a white rgba background
    img0.show()
    #img0.save("result1.png")


    # Saved in the same relative location
    #img = img.convert("RGB")
    #img.save("/home/lekhuong/Downloads/shit.jpg")

'''
dir = ""
data_path = os.path.join(dir, '*g')
'''

if __name__ == '__main__':
    #generate_picture('/home/lekhuong/Downloads/*png')
    delete_background('/home/lekhuong/Downloads/youpredict.png')
