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


def isPossible(bitPlane, image, plaintext):
    listComp = calculateBMComplexity(bitPlane)
    w, h = image.size
    for i in listComp:
        None


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

    for i in cropImage:
        for j in i:
            bitplane = convertToBitplane(j, 8, 8)
            complexity = calculateBMComplexity(bitplane, 8, 8)
            for k, c in enumerate(complexity):
                if float(c) >= THRESHOLD and g:
                    print(g)
                    bitplane[k] = ''.join(g[0])
                    g.pop(0)
                    # showImage(bitplane[0], 8, 8)

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
