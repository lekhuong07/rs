from PIL import Image, ImageDraw, ImageFont
import cv2, glob
import requests
from io import BytesIO


AVATAR = "https://platform-lookaside.fbsbx.com/platform/profilepic/" \
         "?asid=10156184859638719&height=100&width=100&ext=1559899617&hash=AeQTBogsP-yCDOQq"
CATEGORY = "https://d3k9eq2976l0ly.cloudfront.net/images/1558678576.png"

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
clicked = False

import argparse, webbrowser, numpy
APPLE_STORE = "https://www.apple.com/ios/app-store/"
GG_PLAY = "https://play.google.com/store"


def click_and_redirect(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        clicked = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        clicked = False
        if 626 < x < 797 and 12 < y < 59:
            webbrowser.open(APPLE_STORE)
        if 808 < x < 950 and 12 < y < 59:
            webbrowser.open(GG_PLAY)


def redirect_to_link (input_image):
    input_image = cv2.cvtColor(numpy.array(input_image), cv2.COLOR_RGB2BGR)
    clone = input_image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_redirect)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", input_image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'c' key is pressed, break from the loop
        if key == ord("c"):
            break
    cv2.destroyAllWindows()


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
def generate_picture(path, category_link, avatar_link, txt):
    images = [file for file in glob.glob(path)]
    print(images)
    images.sort()
    #get image to work
    img0 = Image.open('big.png')
    response1 = requests.get(category_link)
    img1 = Image.open(BytesIO(response1.content))
    response3 = requests.get(avatar_link)
    img3 = Image.open(BytesIO(response3.content))
    img0b = img0.copy()
    #img0.show()

    #c part:
    width, height = img1.size
    img1 = img1.resize((int(width / 3.11), int(height / 3.11)))
    img0.paste(img1, (361, 93))
    img0 = layer_on_bw(img0b, img0)

    #profile picture part:
    width, height = img3.size
    draw = ImageDraw.Draw(img0)
    draw.rectangle(((53, 435), (115, 435+115-55)), fill="black")
    #Add profile picture on black square
    img3 = img3.resize((int(width / (width / 60))+3, int(height / (height / 60))+1))
    img0.paste(img3, (53, 435))

    #text part:
    img0bt = img0.copy()
    fnt = ImageFont.truetype("arial.ttf", 22, encoding="unic")
    draw.text((width/2 + 350, 440), txt[0], font=fnt, fill="Yellow")

    line1 = "Which driver will win the 2019 Singapore F1?"
    line2 = "Novi was among the " + " "*(len(txt[1])+2) + " who predicted " + " "*(len(txt[2])+2)
    fnt1 = ImageFont.truetype("arial.ttf", 20, encoding="unic")
    draw.text((width / 4 + 300, 470), line1, font=fnt1, fill="White")
    draw.text((width / 4 + 250, 490), line2, font=fnt1, fill=("White"))

    fnt2 = ImageFont.truetype("arial.ttf", 18, encoding="unic")
    draw.text((width / 4 + 435, 492), txt[1], font=fnt2, fill=("Yellow"))
    draw.text((width / 4 + 595, 492), txt[2], font=fnt2, fill=("Yellow"))

    img0.show()
    img0.save("finalresult.png")

    # return img0

if __name__ == '__main__':
    generate_picture(r'*png', CATEGORY, AVATAR, ["SINGAPORE FORMULA 1", "5%", "Lewis Hamilton."])
    #redirect_to_link(test)