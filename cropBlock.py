from PIL import Image

THRESHOLD = 0.3


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


def stringToMatrix(ls, width=8, height=8):
    y = [ls[i:i + height] for i in range(0, len(ls), width)]
    return y


# bitPlane 24x24 , width=8, height=8
# list of 24 complexity
def calculateBMComplexity(bitPlane, width=8, height=8):
    listComp = []
    for plane in bitPlane:
        comp = 0
        pl = stringToMatrix(plane)
        print(pl)
        for i in range(0, 8):
            for j in range(0, 8):
                if j < 7:
                    if (pl[i][j] != pl[i][j + 1]):
                        comp += 1
                if i < 7:
                    if (pl[i][j] != pl[i + 1][j]):
                        comp += 1
                print(i, j, comp)
        # for i in range(0, len(plane)):
            # if (i + 1) < len(plane):
            #     if (i + 1) % width > 0 and plane[i + 1] != plane[i]:
            #         comp += 1
            # if (i + 8) < len(plane):
            #     if plane[i + 8] != plane[i]:
            #         comp += 1
            # print(i, comp)
        listComp.append(comp / (width * (height - 1) + height * (width - 1)))
    return listComp


img = Image.open('C:/Users/mnaufal75/foto.png')
rgb_img = img.convert('RGB')
# pix = img.load()

cropImage = cropBlock(rgb_img, 200, 200)


# for iImage in cropImage:
#     for jImage in iImage:
#         bitPlane = convertToBitplane(jImage, 200, 200)
#         # print(bitPlane)
#         break
#     break
lists = ['1010101010101010101010101010101010101010101010101010101010101010']
print(calculateBMComplexity(lists))
# print(crop)
