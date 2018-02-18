from PIL import Image


cropList = []


def crop(input, height, width):
    # im = Image.open(input)
    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = img.crop(box)
            # a.show()
            cropList[i].append(a)


img = Image.open('C:/Users/mnaufal75/foto.bmp')
rgb_img = img.convert('RGB')
# pix = img.load()

imgwidth, imgheight = img.size
crop(rgb_img, 8, 8)

x = []

for i in range(0, 24):
    x.append('')

width, height = img.size
for i in range(0, width):
    for j in range(0, height):
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
y = [k[i:i + height] for i in range(0, len(k), height)]

newImg = Image.new('1', (width, height))
for i in range(0, width):
    for j in range(0, height):
        newImg.putpixel((i, j), int(y[i][j]))

# newImg.show()
