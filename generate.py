from PIL import Image, ImageDraw, ImageFont
import cv2, glob, os, requests
import numpy

import Tkinter as tk
button_flag = True
def click():
    """
    respond to the button click
    """
    global button_flag
    # toggle button colors as a test
    if button_flag:
        button1.config(bg="white")
        button_flag = False
    else:
        button1.config(bg="green")
        button_flag = True


def layer_on_bw(img, img2):
    img = img.convert("RGBA")
    data1 = img.getdata()
    img2  = img2.convert("RGBA")
    data2 = img2.getdata()
    newData = []
    # data 1 original
    # data 2 original with new black background image
    i = 0
    for item in data2:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append(data1[i])
        else:
           newData.append(item)
        i += 1
    img.putdata(newData)
    return img
'''
* corner part is divided into 2 parts:
* predict part 
* purple thing
'''
def layer_on_topcorner(img, img2):
    img = predict_part(img, img2)
    img = purple_thing(img, img2)
    return img

def predict_part(img, img2):
    img = img.convert("RGBA")
    data1 = img.getdata()
    img2 = img2.convert("RGBA")
    data2 = img2.getdata()
    newData = []
    # data 1 is the layer below
    # data 2 is the layer on top
    i = 0
    for item in data2:
        if item[0] > 150 and item[1] > 150 and item[2] < 100:
            newData.append(item)
        else:
            newData.append(data1[i])
        i += 1
    img.putdata(newData)
    # img.show()
    return img

def purple_thing(img, img2):
    img = img.convert("RGBA")
    data1 = img.getdata()
    img2 = img2.convert("RGBA")
    data2 = img2.getdata()
    newData = []
    # data 1 is the layer below
    # data 2 is the layer on top
    i = 0
    for item in data2:
        if item[0] < 200 and item[1] < 200 and item[2] > 200:
            newData.append(data1[i])
        else:
            newData.append(item)
        i += 1
    img.putdata(newData)
    # img.show()
    return img

#path: path to image's folder
#txt: add-in text:
def generate_picture(path, txt):
    images = [file for file in glob.glob(path)]
    images.sort()
    #get image to work
    img0   = Image.open(images[0])
    img1 = Image.open(images[1])
    img2 = Image.open(images[-1])
    img3 = Image.open(images[-2])
    #img0.show()

    #mid part:
    width, height = img1.size
    img1 = img1.resize((int(width / 3.6), int(height / 3.6)))
    img0b = img0.copy()
    img0.paste(img1, (398, 165))
    #img0.show()
    img0 = layer_on_bw(img0b, img0)
    #img0.show()

    #top corner part
    width, height = img2.size
    img2 = img2.resize((int(width / 3), int(height / 3)))
    img2 = img2.crop((0, 8, int(width / 3), int(height / 3)))
    img0.paste(img2, (10, 7))
    img0 = layer_on_topcorner(img0b, img0)
    #img0.show()

    #profile picture part:
    width, height = img3.size
    draw = ImageDraw.Draw(img0)
    draw.rectangle(((58, 435), (115, 435+115-58)), fill="black") # size: (57, 57)
    #Add profile picture on black square
    img3 = img3.resize((int(width / (width/57)), int(height / (height/57))))
    img0.paste(img3, (58, 435))
    #text part:

    img0bt = img0.copy()
    draw.rectangle(((200, 435), (750, 520)), fill="black")
    fnt = ImageFont.truetype("arial.ttf", 22, encoding="unic")
    draw.text((width/2 + 20, 440), txt[0], font=fnt, fill="Yellow")
    #img0 = layer_on_bw(img0bt, img0)
    line1 = "Which driver will win the 2019 Singapore F1?"
    line2 = "Novi was among the " + " "*(len(txt[1])+2) + " who predicted " + " "*(len(txt[2])+2)
    fnt1 = ImageFont.truetype("arial.ttf", 20, encoding="unic")
    draw.text((width / 4 + 100, 470), line1, font=fnt1, fill="White")
    draw.text((width / 4 + 50, 490), line2, font=fnt1, fill=("White"))

    fnt2 = ImageFont.truetype("arial.ttf", 18, encoding="unic")
    draw.text((width / 4 + 235, 492), txt[1], font=fnt2, fill=("Yellow"))
    draw.text((width / 4 + 395, 492), txt[2], font=fnt2, fill=("Yellow"))

    img0.show()
    img0.save("finalresult.png")

if __name__ == '__main__':
    generate_picture(r'C:\Users\Khuong Le\Desktop\rs\*png', ["SINGAPORE FORMULA 1", "5%", "Lewis Hamilton."])
    #layer_onto(r'C:\Users\Khuong Le\Desktop\rs\f1.png', r'C:\Users\Khuong Le\Desktop\rs\big.png')
