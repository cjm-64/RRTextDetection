import time
import cv2
import easyocr
import matplotlib.pyplot as plt
import os
import pandas as pd
import math
import xlwt
import openpyxl
import collections

# Each entry to list is: ['filename', 'text', 'text_n', 'box_area', 'nondrant']

def writeToExcel(text):
    output_name = 'output.xlsx'

    out_df = pd.DataFrame(text, columns=['filename', 'text', 'text_n', 'box_area (%)', 'nondrant'])
    out_df.to_excel(output_name, index=False)

def findTextLocInImage(Sx,Sy,Ex,Ey, rows, cols):
    Midx = ((Ex-Sx)/2)+Sx
    Midy = ((Ey-Sy)/2)+Sy
    vertslices = math.floor(cols/3)
    horzslices = math.floor(rows/3)
    Col_loc = []
    Row_loc = []
    if Midx < vertslices:
        # First Column
        Col_loc.append([1, 4, 7])
    elif vertslices < Midx and Midx <= vertslices*2:
        # Second Column
        Col_loc.append([2, 5, 8])
    else:
        # Third column
        Col_loc.append([3, 6, 9])

    if Midy < horzslices:
        # First row
        Row_loc.append([1, 2, 3])
    elif horzslices < Midy and Midy <= horzslices*2:
        # Second row
        Row_loc.append([4, 5, 6])
    else:
        # Third Row
        Row_loc.append([7, 8, 9])

    print("Centroid Location: ", (list(set(Col_loc[0]).intersection(Row_loc[0]))[0]))
    return (list(set(Col_loc[0]).intersection(Row_loc[0]))[0])


def textSearch(img, reader, line_col, file, img_with_TD):
    text = reader.readtext(img, workers=len(os.sched_getaffinity(0)))
    n = 0
    if not text:
        print("No text")
        img_with_TD.append([file, "No Text", n, 0, 0])
    for t in text:
        placeholder = []
        rows, cols, chan = img.shape
        img_pixels = rows*cols
        boundbox, imgtext, score = t
        Start_x = math.floor(boundbox[0][0])
        Start_y = math.floor(boundbox[0][1])
        End_x = math.floor(boundbox[2][0])
        End_y = math.floor(boundbox[2][1])
        cv2.rectangle(img,
                      (Start_x, Start_y),
                      (End_x, End_y),
                      line_col,
                      5)
        box_height = End_y - Start_y
        box_width = End_x - Start_x
        box_area = box_height*box_width
        box_area_pct = (box_area/img_pixels)*100
        placeholder = [file, imgtext, n, box_area_pct]
        placeholder.append(findTextLocInImage(Start_x, Start_y,End_x, End_y, rows, cols))

        img_with_TD.append(placeholder)
        n += 1

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

def main():
    # creat list of to fill with lists of info
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