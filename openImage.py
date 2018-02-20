from PIL import Image


def crop(width, height):
    blocklist = []
    for i in range(0, imgwidth, width):
        templist = []
        blocklist.append(templist)

    for i in range(0, imgwidth, width):
        for j in range(0, imgheight, height):
            box = (i, j, i + height, j + width)
            blocklist[int(i / width)].append(img.crop(box))


img = Image.open('resource/morata.png')
rgb_img = img.convert('RGB')
# pix = img.load()

imgwidth, imgheight = img.size
crop(40, 40)

x = []

for i in range(0, 24):
    x.append('')

print(imgwidth, imgheight)

for i in range(0, imgwidth):
    for j in range(0, imgheight):
        r, g, b = rgb_img.getpixel((i, j))

        rBinary = format(r, '08b')
        for k in range(0, 8):
            x[k] += rBinary[k]

        gBinary = format(g, '08b')
        for k in range(0, 8):
            x[k + 8] += gBinary[k]

        bBinary = format(b, '08b')
        for k in range(0, 8):
            x[k + 16] += bBinary[k]

baca = int(input("Tampilkan plane ke berapa? "))

k = x[baca]
y = [k[i:i + imgheight] for i in range(0, len(k), imgheight)]

newImg = Image.new('1', (imgwidth, imgheight))
for i in range(0, imgwidth):
    for j in range(0, imgheight):
        newImg.putpixel((i, j), int(y[i][j]))

newImg.show()
