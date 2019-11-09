import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv.imread('SMB_World_1-3_NES_1.png')
img_gray = cv.imread('SMB_World_1-3_NES_1.png', 0)

templates = {"koopa": (cv.imread('koopa2.png', 0), (0, 0, 255), 0.45),
             "coin": (cv.imread('coin.png', 0), (0, 255, 0), 0.8),
             "goomba": (cv.imread('goomba.png', 0), (0, 0, 255), 0.8),
             }


"""
cv.imshow('image', img_gray)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imshow('image', template_gray)
cv.waitKey(0)
cv.destroyAllWindows()
"""


# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF']#, 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            #'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

for meth in methods:
    img = img_gray.copy()
    method = eval(meth)
    # Apply template Matching
    #res = cv.matchTemplate(img, template_gray, method)
    #min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #    top_left = min_loc
    #else:
    #    top_left = max_loc

    for template in templates:
        temp, color, threshold = templates[template]
        w, h = temp.shape[::-1]

        res = cv.matchTemplate(img_gray, temp, cv.TM_CCOEFF_NORMED)#, mask=(temp < 255)*255)

        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), color, 1)
    cv.imshow('res.png', img_rgb)
    cv.waitKey(0)
    cv.destroyAllWindows()

    """
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img, cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
    """