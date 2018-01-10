import png
import sys

filename = sys.argv[1]
messageRed = sys.argv[2]
messageGreen = sys.argv[3]
messageBlue = sys.argv[4]

imageReader = png.Reader(filename)

image = imageReader.asRGBA()

width = image[0]
height = image[1]
pixels = list(image[2])

binaryRed = ""
binaryGreen = ""
binaryBlue = ""

for letter in messageRed:
    binaryRed += '{0:08b}'.format(ord(letter))

for letter in messageBlue:
    binaryBlue += '{0:08b}'.format(ord(letter))

for letter in messageGreen:
    binaryGreen += '{0:08b}'.format(ord(letter))


if width*height < len(binaryRed) or width*height < len(binaryBlue) or width*height < len(binaryGreen):
    print("Error! Image is too small!")
    sys.exit(1)

finishedEncoding = False
counter = 0

for i in range(height):

    row = pixels[i]

    for j in range(width):
        if counter < len(binaryRed):
            row[4*j] = 2*int(row[4*j]/2) + (1 if binaryRed[counter] == '1' else 0)

        if counter < len(binaryGreen):
            row[4 * j + 1] = 2*int(row[4 * j + 1] / 2) + (1 if binaryGreen[counter] == '1' else 0)

        if counter < len(binaryBlue):
            row[4 * j + 2] = 2*int(row[4 * j + 2] / 2) + (1 if binaryBlue[counter] == '1' else 0)

        counter += 1

imageWriter = png.Writer(width=width, height=height,alpha=True)
outputFile = open(filename.split(".")[0] + "_out.png", "wb")

imageWriter.write(outputFile, pixels)

outputFile.close()
