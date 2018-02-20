from PIL import Image
import sys
import getopt

THRESHOLD = 0.3


def cropBlock(input, height=8, width=8):
    # im = Image.open(input)
    cropList = []
    width, height = input.size
    imgheight, imgwidth = 8, 8
    for i in range(0, height, imgheight):
        cropList.append([])

    for i in range(0, height, imgheight):
        for j in range(0, width, imgwidth):
            box = (j, i, j + imgwidth, i + imgheight)
            a = input.crop(box)
            # a.show()
            cropList[int(i / imgheight)].append(a)

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


def matrixToString(mx, width=8, height=8):
    strs = ''
    for i in range(0, width):
        for j in range(0, height):
            strs += mx[i][j]
    return ''.join(strs)


# bitPlane 24x24 , width=8, height=8
# list of 24 complexity
def calculateBMComplexity(bitPlane, width=8, height=8):
    listComp = []
    for plane in bitPlane:
        comp = 0
        pl = stringToMatrix(plane)
        for i in range(0, width):
            for j in range(0, height):
                if j < width - 1:
                    if (pl[i][j] != pl[i][j + 1]):
                        comp += 1
                if i < height - 1:
                    if (pl[i][j] != pl[i + 1][j]):
                        comp += 1
        listComp.append(comp / (width * (height - 1) + height * (width - 1)))
    return listComp


def calculateMessageComplexity(msg, width=8, height=8):
    comp = 0
    message = msg
    for i in range(0, width):
        for j in range(0, height):
            if j < width - 1:
                if (message[i][j] != message[i][j + 1]):
                    comp += 1
            if i < height - 1:
                if (message[i][j] != message[i + 1][j]):
                    comp += 1
    return comp / (width * (height - 1) + height * (width - 1))


def generateWC(width=8, height=8):
    wc = []
    for i in range(0, width):
        wc.append([])
    for i in range(0, width):
        for j in range(0, height):
            if (i + j) % 2 == 0:
                wc[i].append('0')
            else:
                wc[i].append('1')
        wc[i] = ''.join(wc[i])
    return wc


def generateBC(width=8, height=8):
    bc = []
    for i in range(0, width):
        bc.append([])
    for i in range(0, width):
        for j in range(0, height):
            if (i + j) % 2 == 0:
                bc[i].append('0')
            else:
                bc[i].append('1')
        bc[i] = ''.join(bc[i])
    return bc


def conjugateBitPlane(bitPlane, width=8, height=8):
    str1 = stringToMatrix(bitPlane)
    wc8 = generateWC()
    for i in range(0, width):
        for j in range(0, height):
            # xor
            if str1[i][j] == wc8[i][j]:
                str1[i][j] = '0'
            else:
                str1[i][j] = '1'
    return str1


def conjugateMessage(msg, width=8, height=8):
    str_ = msg
    wc8 = generateWC()
    for i in range(0, width):
        ls = list(str_[i])
        for j in range(0, height):
            # xor
            if ls[j] == wc8[i][j]:
                ls[j] = '0'
            else:
                ls[j] = '1'
        str_[i] = ''.join(ls)
    return str_


# def isPossible(bitPlane, image, plaintext):
    # listComp = calculateBMComplexity(bitPlane)
def isPossible(ListAllComplexity, image, plaintext):
    w, h = image.size
    sizeLength = str(len(plaintext))
    sizeMessage = len(plaintext) / 8
    if len(plaintext) % 8 > 0:
        sizeMessage += 1
    sizeMap = sizeMessage / 8
    if sizeMessage % 8 > 0:
        sizeMap += 1
    count = 0
    for i in ListAllComplexity:
        if i > THRESHOLD:
            count += 1
    return count > (sizeLength + sizeMap + sizeMessage)


def PBCtoCGC(bitPlane, width=8, height=8):
    bp = stringToMatrix(bitPlane, width, width)
    for i in range(0, width):
        for j in range(0, height):
            tmp = bp[i][j]
            if i > 0:
                # xor
                if tmp == bp[i][j - 1]:
                    bp[i][j] = '0'
                else:
                    bp[i][j] = '1'
    return matrixToString(bp)


def CGCtoPBC(bitPlane, width=8, height=8):
    bp = stringToMatrix(bitPlane, width, width)
    for i in range(0, width):
        for j in range(0, height):
            tmp = bp[i][j]
            if i > 0:
                # xor
                if tmp == bp[i][j - 1]:
                    bp[i][j] = '0'
                else:
                    bp[i][j] = '1'
    return matrixToString(bp)


def showImage(k, width=8, height=8):
    y = [k[i:i + height] for i in range(0, len(k), height)]

    newImg = Image.new('1', (width, height))
    for i in range(0, width):
        for j in range(0, height):
            newImg.putpixel((i, j), int(y[i][j]))
    newImg.show()


def generatorMessage(msg):
    msgBlock = []
    for i in range(0, len(msg), 8):
        x = msg[i:i + 8]
        # or j in range(0, 8, 8):
        strs = ['{0:08b}'.format(ord(c)) for c in x]
        if calculateMessageComplexity(strs, 8, 8) < THRESHOLD:
            strs = conjugateMessage(strs, 8, 8)
        msgBlock.append(strs)
    # yield strs
    return msgBlock


def a(str_, width=8, height=8):
    y = [str_[i:i + height] for i in range(0, len(str_), height)]
    newImg = Image.new('1', (width, height))
    for i in range(0, width):
        for j in range(0, height):
            newImg.putpixel((i, j), int(y[i][j]))
    return newImg


def encryptMessage(inputFile, messageFile, key, outputFile):
    img = Image.open(inputFile)
    rgb_img = img.convert('RGB')
    width, height = img.size

    msg = ''
    panjangMessage = 0
    with open(messageFile) as f:
        while True:
            c = f.read(1)
            panjangMessage += 1
            msg += c
            if not c:
                break

    g = generatorMessage(msg)
    cropImage = cropBlock(rgb_img, 8, 8)

    for i in range(0, len(cropImage)):
        for j in range(0, len(cropImage[i])):
            bitplane = convertToBitplane(cropImage[i][j], 8, 8)
            complexity = calculateBMComplexity(bitplane, 8, 8)
            for k, c in enumerate(complexity):
                if float(c) >= THRESHOLD and g:
                    # print(g)
                    bitplane[k] = ''.join(g[0])
                    g.pop(0)
            gambar = zip(*bitplane)
            x = list(gambar)
            # print(x[1])
            newImg = Image.new('RGB', (width, height))
            for k in range(0, 64):
                pixel = ''.join(x[k])
                red, green, blue = int(pixel[0:8], 2), int(pixel[8:16], 2), int(pixel[16:24], 2)
                xPixel = k // 8
                yPixel = k % 8
                newImg.putpixel((xPixel, yPixel), (red, green, blue))
                # print(red, green, blue)
                cropImage[i][j] = newImg

    print(width, height)
    newImg = Image.new('RGB', (width, height))
    y_offset = 0
    for i in cropImage:
        x_offset = 0
        for j in i:
            newImg.paste(j, (x_offset, y_offset))
            x_offset += 8
        y_offset += 8
    newImg.save(outputFile)
    # y = [k[i:i + height] for i in range(0, len(k), height)]
    # newImg = Image.new('1', (width, height))
    # for i in range(0, width):
    #     for j in range(0, height):
    #         newImg.putpixel((i, j), int(y[i][j]))
    # newImg.show()


def decryptMessage(inputFile, key, outputFile):
    img = Image.open(inputFile)
    rgb_img = img.convert('RGB')


def mainProgram():
    inputFile, outputFile, messageFile, key = '', '', '', ''
    encrypt = False
    decrypt = False
    myopts, args = getopt.getopt(sys.argv[1:], "edi:o:m:k:")

    for i, j in myopts:
        if i == '-e':
            encrypt = True
        elif i == '-d':
            decrypt = True
        elif i == '-i':
            inputFile = j
        elif i == '-o':
            outputFile = j
        elif i == '-m':
            messageFile = j
        elif i == '-k':
            key = j
        else:
            print("Usage: %s -i input -o output" % sys.argv[0])

    if (encrypt):
        encryptMessage(inputFile, messageFile, key, outputFile)
    elif (decrypt):
        decryptMessage(inputFile, messageFile, key, outputFile)


mainProgram()

# img = Image.open('morata.png')
# rgb_img = img.convert('RGB')
# # pix = img.load()

# cropImage = cropBlock(rgb_img, 8, 8)
# print(cropImage)

# ListBitPlane = []
# for iImage in cropImage:
#     for jImage in iImage:
#         bitPlane = convertToBitplane(jImage, 8, 8)
#         ListBitPlane.extend(bitPlane)
# print(ListBitPlane)
# lists = ['1010101001010101101010100101010110101010010101011010101001010101']
# print(calculateBMComplexity(lists))
# print(crop)
# print(matrixToString(['123', '234', '123'], 3, 3))
