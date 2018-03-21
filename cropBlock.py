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
    message = stringToMatrix(msg)
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
        wc.append([''])
        for j in range(0, height):
            if (i + j) % 2 == 0:
                wc[i] += '0'
            else:
                wc[i] += '1'
    return wc


def generateBC(width=8, height=8):
    bc = []
    for i in range(0, width):
        bc.append([''])
        for j in range(0, height):
            if (i + j) % 2 == 0:
                bc[i] += '1'
            else:
                bc[i] += '0'
    return bc


def conjugateBitPlane(plane, width=8, height=8):
    str1 = stringToMatrix(plane)
    wc8 = generateWC()
    for i in range(0, width):
        for j in range(0, height):
            # xor
            if str1[i][j] == wc8[i][j]:
                str1[i][j] = '0'
            else:
                str1[i][j] = '1'
    
    return matrixToString(str1)


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

def addDummyMsg(msg,numberMod):
    while msg % numberMod > 0:
        msg += " "
    return msg

# validation pass
def seqBPCS(ListBitPlane, msg, listComp):
    i = 0
    newListBitPlane = []
    msg = addDummyMsg(msg)
    startMsg = 0
    for Bitplane in ListBitPlane:
        newBitPlane = []
        for plane in Bitplane:
            if listComp[i] > THRESHOLD and startMsg < len(msg): 
                newPlane = []
                for char in msg[startMsg:startMsg+8]:
                    newPlane.append(format(char, '08b'))
                if calculateMessageComplexity(msg[startMsg:startMsg+8]) > THRESHOLD:
                    newBitPlane.append(newPlane)
                else:
                    newBitPlane.append(conjugateBitPlane(newPlane))                    
                startMsg += 8
            else:
                newBitPlane.append(plane)
            i+=1
        newListBitPlane.append(newBitPlane)
    return newListBitPlane
    
def seedBPCS(ListBitPlane, msg, seed, listComp): 


img = Image.open('morata.png')
rgb_img = img.convert('RGB')
# pix = img.load()

cropImage = cropBlock(rgb_img, 8, 8)
print(cropImage)

ListBitPlane = []
for iImage in cropImage:
    for jImage in iImage:
        bitPlane = convertToBitplane(jImage, 8, 8)
        ListBitPlane.extend(bitPlane)

# msg = input("pesan : ")


# print(ListBitPlane)
# lists = ['1010101001010101101010100101010110101010010101011010101001010101']
# print(calculateBMComplexity(lists))
# print(crop)
# print(matrixToString(['123', '234', '123'], 3, 3))
