from PIL import Image
import os
from VectorCompare import VectorCompare, buildvector

# collect character sets for training
v = VectorCompare()
iconset = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
imageset = []

for letter in iconset:
    for img in os.listdir('./python_captcha/iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store": # windows check...
            temp.append(buildvector(Image.open("./python_captcha/iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})

# open source image
image = Image.open("./python_captcha/captcha.gif")
image.convert("P")

image2 = Image.new("P", image.size, 255)
for x in range(image.size[1]):
	for y in range(image.size[0]):
		pix = image.getpixel((y,x))
		if pix == 220 or pix == 227:
			image2.putpixel((y,x),0)
#image2.show()

inletter = False
foundletter = False
start = 0
end = 0
letters = []
for y in range(image2.size[0]): # slice across
    for x in range(image2.size[1]): # slice down
        pix = image2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))
    inletter=False


count = 0
for letter in letters:
    image3 = image2.crop(( letter[0] , 0, letter[1],image2.size[1] ))
    guess = []
    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append( ( v.relation(y[0],buildvector(image3)),x) )
    guess.sort(reverse=True)
    print(guess[0])
    count += 1