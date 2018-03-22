from PIL import Image
import sys
import getopt

THRESHOLD = 0.5


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
        listComp.append(float(comp / (width * (height - 1) + height * (width - 1))))
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
def isPossibleAndGenerateMap(cropImage, image, plaintext):
    ListAllComplexity = []
    mapConjugation = ''
    for i in range(0, len(cropImage)):
        for j in range(0, len(cropImage[i])):
            bitplane = convertToBitplane(cropImage[i][j], 8, 8)
            complexity = calculateBMComplexity(bitplane, 8, 8)
            ListAllComplexity.extend(complexity)
    w, h = image.size
    sizeMessage = len(plaintext) // 64
    if len(plaintext) % 64 > 0:
        sizeMessage += 1
    count = 0
    lmapCon = -1
    for i in ListAllComplexity:
        if i >= THRESHOLD:
            mapConjugation += '1'
            count += 1
        else:
            mapConjugation += '0'
        if count == sizeMessage:
            lmapCon = len(mapConjugation) // 64
            if len(mapConjugation) % 64 > 0:
                lmapCon += 1

    # tambahin map konjugasi dan panjang pesan (asumsi muat 1 bitplane)
    if count > sizeMessage:
        valid = True
    else:
        valid = False
    return (valid, mapConjugation)


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


def showImage(k, width=8, height=8):
    y = [k[i:i + height] for i in range(0, len(k), height)]

<<<<<<< HEAD
cropImage = cropBlock(rgb_img, 8, 8)
print(cropImage)

ListBitPlane = []
for iImage in cropImage:
    for jImage in iImage:
        bitPlane = convertToBitplane(jImage, 8, 8)
        ListBitPlane.extend(bitPlane)

# msg = input("pesan : ")


=======
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
        # if calculateMessageComplexity(strs, 8, 8) < THRESHOLD:
        #     strs = conjugateMessage(strs, 8, 8)
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
    print(msg)           
    g = generatorMessage(msg)
    cropImage = cropBlock(rgb_img, 8, 8)

    # TODO: hitung payload capacity

    # TODO: prepare 1 bitplane for message length
    threshold, mapConjugation = isPossibleAndGenerateMap(cropImage, img, msg)
    if len(mapConjugation) % 64 > 0 :
        while len(mapConjugation) % 64 > 0:
            mapConjugation+="0"
    # TODO: prepare bitplanes for map
    if threshold:
        # print("masuk")
        for i in range(0, len(cropImage)):
            for j in range(0, len(cropImage[i])):
                bitplane = convertToBitplane(cropImage[i][j], 8, 8)
                complexity = calculateBMComplexity(bitplane, 8, 8)
                for k, c in enumerate(complexity):
                    if i == 0 and j == 0 and k == 0:
                        panjangString = "{:064b}".format(panjangMessage)
                        bitplane[k] = panjangString
                        # mapConjugation.append(0)
                    elif i == 0 and j == 0 and ((k == 1) or (k == 2)):
                        bitplane[k] = mapConjugation[0:64]
                        mapConjugation = mapConjugation[64:]
                    elif c >= THRESHOLD and g:
                        #print(k)
                        #print(bitplane[k])
                        print(g)
                        bitplane[k] = ''.join(g[0])
                        print(bitplane[k])
                        print(i, j, k)
                        g.pop(0)
                    elif not g:
                        break

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
    else:
        print("not enough memory image")
    # y = [k[i:i + height] for i in range(0, len(k), height)]
    # newImg = Image.new('1', (width, height))
    # for i in range(0, width):
    #     for j in range(0, height):
    #         newImg.putpixel((i, j), int(y[i][j]))
    # newImg.show()


def decryptMessage(inputFile, key, outputFile):
    img = Image.open(inputFile)
    rgb_img = img.convert('RGB')
    width, height = img.size
    cropImage = cropBlock(rgb_img, 8, 8)
    mapConjugation = ''
    ans = ''
    klen = 3
    for i in range(0, len(cropImage)):
            for j in range(0, len(cropImage[i])):
                bitplane = convertToBitplane(cropImage[i][j], 8, 8)
                for k in range(0,len(bitplane)):
                    if i == 0 and j == 0 and k == 0:
                        panjangMap = int(bitplane[k], 2) -1 
                        print(panjangMap)
                    elif i == 0 and j == 0 and ((k == 1) or (k == 2)):   
                        # print(bitplane[k])
                        mapConjugation += bitplane[k]
                        print(mapConjugation)
                    elif klen < len(mapConjugation):
                        if mapConjugation[klen] == '1':
                            # print(bitplane[k])
                            for l in range(0, 64, 8):
                                ans += chr(int(bitplane[k][l:l + 8], 2))
                                # print(i, j, k, chr(int(bitplane[k][l:l + 8], 2)))
                        klen += 1
                    elif klen >= len(mapConjugation):
                        break
    print(ans[0:panjangMap])

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
        decryptMessage(inputFile, messageFile, key)


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
>>>>>>> fa21aa19dbc14bc73d348c24a0b9f01d35f96d69
# print(ListBitPlane)
# lists = ['1010101001010101101010100101010110101010010101011010101001010101']
# print(calculateBMComplexity(lists))
# print(crop)
# print(matrixToString(['123', '234', '123'], 3, 3))
