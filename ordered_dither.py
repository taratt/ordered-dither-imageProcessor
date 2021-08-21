from PIL import Image, ImageOps
import os


def createMatrix(x, y, size, value, step, matrix):

    if (size == 1):
        matrix[y][x] = value
    else:
        size = int(size / 2)
        createMatrix(x, y, size, value , 4*step, matrix)
        createMatrix(x + size, y, size, value + 2*step, 4*step, matrix)
        createMatrix(x, y + size, size, value + 3*step, 4*step, matrix)
        createMatrix(x + size, y + size, size, value + step, 4*step, matrix)
        return matrix


imagePath = input('Please enter the image path:')
img = Image.open(imagePath)
img = ImageOps.exif_transpose(img)
file, extension = os.path.splitext(imagePath)
imgData = img.getdata()

grayScaleData = []
for rgb in imgData:
    data = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
    grayScaleData.append(data)


newImage = Image.new("L", img.size)
newImage.putdata(list(grayScaleData))

newImage.save('gray'+extension)
newImage.show()
matrixSize = int(input('Please enter the image size:'))
bayerMatrix = [[0 for i in range(matrixSize)] for i in range(matrixSize)]
bayerMatrix = createMatrix(0, 0, matrixSize, 0, 1, bayerMatrix)

valueMatrix = [[0 for i in range(img.size[0])] for i in range(img.size[1])]
x = 0
for i in range(img.size[1]):
    for j in range(img.size[0]):
        valueMatrix[i][j] = grayScaleData[x]
        x+=1

dithered = []
for x in range(img.size[1]):
    for y in range(img.size[0]):
        i = x % matrixSize
        j = y % matrixSize
        if valueMatrix[x][y] > bayerMatrix[i][j]:
            dithered.append(1)
        else:
            dithered.append(0)


outImage = Image.new("1", img.size)
outImage.putdata(list(dithered))

# newImage.save('output'+extension)
outImage.show()