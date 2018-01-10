import png
import sys

filename = sys.argv[1]

imageReader = png.Reader(filename)

image = imageReader.asRGBA()

width = image[0]
height = image[1]
pixels = list(image[2])

binaryRed = ""
binaryGreen = ""
binaryBlue = ""


counter = 0

for i in range(height):

    row = pixels[i]

    for j in range(width):
        binaryRed += str(row[4*j]%2)
        binaryGreen += str(row[4*j+1]%2)
        binaryBlue += str(row[4*j+2]%2)

        counter += 1

binaryRed = [binaryRed[i:i+8] for i in range(0, len(binaryRed), 8)]
binaryGreen = [binaryGreen[i:i+8] for i in range(0, len(binaryGreen), 8)]
binaryBlue = [binaryBlue[i:i+8] for i in range(0, len(binaryBlue), 8)]

redText = "".join([chr(int(x,2)) for x in binaryRed])
greenText = "".join([chr(int(x,2)) for x in binaryGreen])
blueText = "".join([chr(int(x,2)) for x in binaryBlue])

print(redText)
print(greenText)
print(blueText)
