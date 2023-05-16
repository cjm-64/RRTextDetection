import time
import cv2
import easyocr
import matplotlib.pyplot as plt
import os
import pandas as pd
import xlwt
import openpyxl
import collections

# Each entry to list is: ['filename', 'text', 'text_n', 'box_area']

def writeToExcel(text):
    output_name = 'output.xlsx'

    out_df = pd.DataFrame(text, columns=['filename', 'text', 'text_n', 'box_area'])
    out_df.to_excel(output_name, index=False)


def textSearch(img, reader, line_col, file, img_with_TD):
    text = reader.readtext(img, workers=len(os.sched_getaffinity(0)))
    n = 0
    if not text:
        print("No text")
        img_with_TD.append([file, "No Text", n, 0])
    for t in text:
        boundbox, imgtext, score = t
        cv2.rectangle(img,
                      (round(boundbox[0][0]), round(boundbox[0][1])),
                      (round(boundbox[2][0]), round(boundbox[2][1])),
                      line_col,
                      5)
        box_height = round(boundbox[2][1] - boundbox[0][1])
        box_width = round(boundbox[2][0] - boundbox[0][0])
        box_area = box_height*box_width
        img_with_TD.append([file, imgtext, n, box_area])
        n += 1

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

def main():
    # creat list of tuples that have the info we need for each image
    img_with_TD = []
    reader = easyocr.Reader(['en'], gpu=False)
    line_col = (0, 255, 0)
    folder = 'TestingImages'

    n = 0
    tot_time = 0
    folderlist = os.listdir(folder)
    folderlist.sort()
    for file in os.listdir(folder):
        print(file)
        if file.endswith(".jpg"):
            start = time.time()
            img = cv2.imread(os.path.join(folder, file))
            textSearch(img, reader, line_col, file, img_with_TD)
            print(time.time() - start)
            tot_time += time.time() - start
        else:
            break
        n += 1

    print("Total time: ", tot_time)
    print("Avg time: ", tot_time / n)

    print(len(img_with_TD))
    for i in img_with_TD:
        print(i)

    writeToExcel(img_with_TD)

if __name__ == '__main__':
    main()
    print("Hello World\n")