import cv2
import numpy as np

image = cv2.imread("../res/waterfall.jpg")
h, w, bpp = np.shape(image)
print(h, w)

water = 160
mark1 = 160
mark2 = 225
red1 = 51
red2 = 180
for y in range(h):
    for x in range(w):
        if image[y][x][0] > water and image[y][x][1] > water and image[y][x][2] > water:
            avg = np.average(image[y][x])
            gb = int((avg-mark1)*(red2-red1)/(mark2-mark1)+red1)
            image[y][x] = (gb, gb, 255)

# cv2.imshow("matrix", image)
# cv2.waitKey(0)
cv2.imwrite("../res/waterfall_new.jpg", image)