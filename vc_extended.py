import sys
import random

def inputFile(nameOfFile): 
	lineString = open(nameOfFile,'r').readline()
	print(lineString)
	return lineString

# get ascii number from charachter
def getAsciiNumber(ch):
	return ord(ch)

# get charachter from ascii number
def getChar(number):
	return chr(number)

# lowercase
def lower(str):
	return str.lower()

# uppercase
def upper(str):
	return str.upper()

# last element deleted
def getStringExcpLastElment(str):
	return str[0:len(str)-1]

# output to file string param
def outputFile(strOut,nameOfFile):
	file = open(nameOfFile,"w")
	file.write(strOut)
	file.close()

# is Alphabet
def isAlphabet(ch):
	return (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') 

# delete no Alphabet Char
def deleteAllCharNonAlphabet(str):
	for i in range(256):
		if not isAlphabet(getChar(i)):
			str = str.replace(getChar(i),"")
	return str

# no "space" char exisiting in str
def print5char(str):
	start = 0
	while start+5 < len(str):
		print(str[start:start+5],end=" ")
		start+=5
	print(str[start:len(str)])

# plaintext as column
# key as row
def generateMatrixVigenere(length):
	mat = []
	for i in range(length):
		mat.append([])
		for j in range(length):
			mat[i].append((i + j ) % length)
	return mat


# asumsion cipher A , plain a (covert)
# for matrix Cipher Vigenere 26 return charachter encrypt
# ch alphabet
# key alphabet
def cipherTextVCAlpha(matVC,ch,key):
	return getChar(matVC[getAsciiNumber(lower(key))-getAsciiNumber('a')][getAsciiNumber(lower(ch))-getAsciiNumber('a')] + getAsciiNumber('A'))

# decrypt
def cipherTextVCAlphaDec(matVC,cipher,key):
	return getChar(matVC[getAsciiNumber(lower(key))-getAsciiNumber('a')].index(getAsciiNumber(cipher)-getAsciiNumber('A')) + getAsciiNumber('a'))

# for matrix Cipher Vigenere 256 return charachter encrypt
# ch alphabet
# key alphabet
def cipherTextVCAscii(matVC,ch,key):
	return getChar(matVC[getAsciiNumber(key)][getAsciiNumber(ch)])

# decrypt
def cipherTextVCAsciiDec(matVC,cipher,key):
	return getChar(matVC[getAsciiNumber(key)].index(getAsciiNumber(cipher)))

def prosesEncrpytVC(key,str,op):
	# karena algo vc biasa key matrix pasti sama
	res = []
	mat = generateMatrixVigenere(op)
	if op == 26:
		key = deleteAllCharNonAlphabet(key)
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start1 < len(str):
			if isAlphabet(str[start1]):
				res.append(cipherTextVCAlpha(mat,lower(str[start1]),key[start2 % lenKey]))
				start2+=1
			else:
				res.append(str[start1])
			start1+=1

	elif op == 256:
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start1 < len(str):
			res.append(cipherTextVCAscii(mat,lower(str[start1]),key[start2 % lenKey]))
			start2+=1
			start1+=1
	return "".join(res)

def prosesDecryptVC(key,cipher,op):
	# karena algo vc biasa key matrix pasti sama
	res = []
	mat = generateMatrixVigenere(op)
	if op == 26:
		key = deleteAllCharNonAlphabet(key)
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start1 < len(cipher):
			if isAlphabet(cipher[start1]):
				res.append(cipherTextVCAlphaDec(mat,cipher[start1],key[start2 % lenKey]))
				start2+=1
			else:
				res.append(cipher[start1])
			start1+=1

	elif op == 256:
		start1 = 0
		start2 = 0
		lenKey = len(key)
		while start1 < len(cipher):
			res.append(cipherTextVCAsciiDec(mat,cipher[start1],key[start2 % lenKey]))
			start2+=1
			start1+=1
	return "".join(res)

print("####### Vigenere Cipher Extended #########")
plaintext = input("Input Plaintext : ")
key = input("Input Key : ")
res1 = prosesEncrpytVC(key,plaintext,256)
print("####### Output Chipper Text biasa #######")
print(res1)
print()
print()
print()
print()
print()
print("############ Decripyting ############")
print("Cipher text : " + res1)
res3 = prosesDecryptVC(key,res1,256)
print("plain text : " + res3)	