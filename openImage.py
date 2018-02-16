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


img = Image.open('C:/Users/mnaufal75/foto.png')
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

        # rBinary = '{0:08b}'.format(r)
        rBinary = format(r, '08b')
        for k in range(0, 8):
            x[k] += rBinary[k]

        # gBinary = '{0:08b}'.format(g)
        gBinary = format(g, '08b')
        for k in range(0, 8):
            x[k + 8] += gBinary[k]

        bBinary = format(b, '08b')
        # bBinary = '{0:08b}'.format(b)
        for k in range(0, 8):
            x[k + 16] += bBinary[k]
        # pix[i, j] = (0, 0, 0)

baca = int(input("Tampilkan plane ke berapa? "))

k = x[baca]
y = [k[i:i + imgheight] for i in range(0, len(k), imgheight)]

newImg = Image.new('1', (imgwidth, imgheight))
for i in range(0, imgwidth):
    for j in range(0, imgheight):
        newImg.putpixel((i, j), int(y[i][j]))
        # newImg[i, j] = y[ij]
newImg.show()
# print(x[0])
# newImg = Image.frombytes('1', (width, height), b'x[0]')
# newImg.show()
# for i in range(0, width):
#     for j in range(0, height):
#         newImg.putpixel((i, j), 0)

# image = Image.open(io.BytesIO(b'x[0]'))
# image.show()

# stream = io.BytesIO(b'x[0]')
# print(stream)

# image = Image.open(x[0])
# draw = ImageDraw.Draw(image)
# image.save('image.png')
# newImg.show()
# img.show()
