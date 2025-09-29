import pickle
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def showImage(file: np.typing.NDArray):
    count = 0
    max = file.shape[2]
    while True:
        img = file[count]
        cv.imshow('aeiou', img)
        k = cv.waitKey(30)
        if k == ord('q'):
            break
        count += 1
        if count >= max:
            count = 0
    cv.destroyAllWindows()

def calculateCells(file: np.typing.NDArray):
    unique, counts = np.unique(file, return_counts=True)
    for i in range(len(unique)):
        if unique[i] != 0:
            print(f'{unique[i]}: {counts[i]}')
    # a = np.hstack((file.normal(size=1000), file.normal(loc=5, scale=2, size=1000)))
    # a = np.hstack(unique, counts)
    # plt.hist(a, bins='auto')  # arguments are passed to np.histogram
    # plt.title("Histogram with 'auto' bins")
    # plt.show()


with open("volume_TAC", "rb") as file:
    try:
        img: np.typing.NDArray = pickle.load(file)
        calculateCells(img)
        showImage(img)
    except EOFError:
        pass