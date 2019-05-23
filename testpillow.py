__author__ = "KL"

from PIL import Image, ImageDraw, ImageFont


def cropped(inputpic,a):
    img = Image.open(inputpic)
    width, height = img.size
    img = img.resize((int(width/5), int(height/5)), Image.ANTIALIAS)
    # Saved in the same relative location
    print( width, height)
    img.save(a)
    return img

#input picture is the background picture
def edit_photo(input_picture, output_picture):
    # Relative Path
    img  = Image.open(input_picture)
    img2 = Image.open("abc.jpg")
    img3 = Image.open("abc.jpg")

    drawtxt = ImageDraw.ImageDraw(img)
    # Angle given rotate 180 degree
    fnt = ImageFont.load_default()
    drawtxt.multiline_text((125, 250), "Hello\nThis is RockShip", font=fnt, fill=(0,0,0,0))

    # paste picture into background one
    img.paste(img2, (20,20))
    img.paste(img3, (220,20))
    img.save(output_picture)

def auto_generate(path, output):


if __name__ == "__main__":
    #cropped("rockship-logo.png", "abc.jpg")
    edit_photo("rockship-logo.png", "newrockship.png")
    print("Done~")
