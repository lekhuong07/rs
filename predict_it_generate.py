from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

DEFAULT_AVATAR = "https://d38qg0g88iwzaq.cloudfront.net/images/1551953912.png"

import time
import random
import os
from services.storage import storage
from urllib.parse import urljoin


def layer_on_bw(img, img2):
    img = img.convert("RGBA")
    data1 = img.getdata()
    img2 = img2.convert("RGBA")
    data2 = img2.getdata()
    newData = []

    i = 0
    for item in data2:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append(data1[i])
        else:
           newData.append(item)
        i += 1
    img.putdata(newData)
    return img


def generate_picture(category_link, avatar_link, txt):
    #img0 = Image.open('assets/banner_template.png')
    img0 = Image.open('big.png')

    response = requests.get(category_link)
    img1 = Image.open(BytesIO(response.content))

    response = requests.get(avatar_link)
    try:
        img3 = Image.open(BytesIO(response.content))
    except:
        response = requests.get(DEFAULT_AVATAR)
        img3 = Image.open(BytesIO(response.content))

    img0b = img0.copy()

    width, height = img1.size
    img1 = img1.resize((int(width / 3.11), int(height / 3.11)))
    img0.paste(img1, (361, 93))
    img0 = layer_on_bw(img0b, img0)

    width, height = img3.size
    draw = ImageDraw.Draw(img0)
    draw.rectangle(((53, 435), (115, 435+115-55)), fill="black")

    img3 = img3.resize((int(width / (width / 60))+3, int(height / (height / 60))+1))
    img0.paste(img3, (53, 435))

    width, height = img0.size
    fnt = ImageFont.truetype("assets/arial.ttf", 22, encoding="unic")
    text_width, text_height = draw.textsize(txt[0])
    draw.text(((width-text_width)/2-50, 440), txt[0], font=fnt, fill="Yellow")

    fnt1 = ImageFont.truetype("assets/arial.ttf", 20, encoding="unic")
    line1 = txt[1]
    text_width, text_height = draw.textsize(line1)
    draw.text(((width-text_width)/2-50, 465), line1, font=fnt1, fill="White")

    line2 = txt[4] + " was among the " + txt[2] + " who predicted " + txt[3]
    list_line2 = line2.split(" ")
    text_width, text_height = draw.textsize(line2)

    width = (width-text_width)/2 - 75
    for e_text in list_line2:
        e_text_width, e_text_height = fnt1.getsize(e_text)
        if e_text != txt[2] and e_text != list_line2[-1] and e_text != list_line2[-2]:
            draw.text((width, 490), e_text, font=fnt1, fill="White")
        else:
            draw.text((width, 490), e_text, font=fnt1, fill="Yellow")

        width += e_text_width + 5

    img0.show()
    img0.save('in_mem_file.png')

    in_mem_file = BytesIO()
    img0.save(in_mem_file, 'PNG')
    key = 'trophies/{}_{}.{}'.format(int(time.time()), random.randint(0, 1000), 'png')
    in_mem_file.seek(0)

    BUCKET_NAME = os.getenv('BUCKET_NAME')
    CDN_ENDPOINT = os.getenv('CDN_ENDPOINT')
    storage.upload_file_obj(in_mem_file, BUCKET_NAME, key)
    return urljoin('{}'.format(CDN_ENDPOINT), key)

if __name__ == '__main__':
    AVATAR = "https://platform-lookaside.fbsbx.com/platform/profilepic/" \
             "?asid=10156184859638719&height=100&width=100&ext=1559899617&hash=AeQTBogsP-yCDOQq"

    CATEGORY = "https://d3k9eq2976l0ly.cloudfront.net/images/1558678576.png"


    url = generate_picture(CATEGORY, AVATAR, [
        "SINGAPORE FORMULA 1",
        "Which driver will win the 2019 Singapore F1?",
        "5%",
        "Lewis Hamilton.",
        "Novi"
    ])
    print(url)


    '''
    generate_picture(CATEGORY, AVATAR, [
        "SINGAPORE FORMULA 1",
        "Which driver will win the 2019 Singapore F1?",
        "5%",
        "Lewis Hamilton.",
        "Novi"
    ])
    '''