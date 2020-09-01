import pandas as pd
import os
from skimage.measure import compare_ssim
import cv2

def diff(bin_1, bin_2):
    imageA = cv2.imread("../dc90ff8e-4008-41ec-bdd8-f741c2742c7f.png")
    imageB = cv2.imread("../d14b751c-4b15-4656-a79f-ff6c2c5f483b.png")

    print(imageA.shape)
    print(imageB.shape)
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)

    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

diff(0, 0)