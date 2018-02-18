from PIL import Image


def cropBlock(input, height=8, width=8):
    # im = Image.open(input)
    cropList = []
    imgwidth, imgheight = img.size
    for i in range(0, imgheight, height):
        cropList.append([])

    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = img.crop(box)
            # a.show()
            cropList[int(i / height)].append(a)

    return cropList


# output bitplane 8x24 list of bitplane 
def convertToBitplane(img, width=8, height=8):
    bitPlane = []
    for i in range(0, 24):
        bitPlane.append([])

    for i in range(0, width):
        for j in range(0, height):
            r, g, b = img.getpixel((i, j))
            rBinary = format(r, '08b')
            for k in range(0, 8):
                bitPlane[k].append(rBinary[k])

            gBinary = format(g, '08b')
            for k in range(0, 8):
                bitPlane[k + 8].append(gBinary[k])

            bBinary = format(b, '08b')
            for k in range(0, 8):
                bitPlane[k + 16].append(bBinary[k])

    for i in range(0, len(bitPlane)):
        bitPlane[i] = ''.join(bitPlane[i])

    return bitPlane


# bitPlane 24x24 , width=8, height=8
# def calculateBMComplexity(bitPlane, width=8, height=8):
#     for plane in bitPlane:

#     return 0


img = Image.open('C:/Users/mnaufal75/foto.png')
rgb_img = img.convert('RGB')
# pix = img.load()

cropImage = cropBlock(rgb_img, 200, 200)


for iImage in cropImage:
    for jImage in iImage:
        bitPlane = convertToBitplane(jImage, 200, 200)
        # print(bitPlane)
        break
    break
# print(crop)