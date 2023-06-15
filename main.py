import time
import cv2
import easyocr
import matplotlib.pyplot as plt
import os
import pandas as pd
import math
from better_profanity import profanity
import multiprocessing
import xlwt
import openpyxl
# import collections

# Each entry to list is: ['filename',
#                         'text',
#                         'text_n',
#                         'box_area (%)',
#                         'Text Length',
#                         'nondrant',
#                         'is profane']


def writeToExcel(text, curr_path):
    output_loc = os.path.join(curr_path, 'output.xlsx')

    out_df = pd.DataFrame(text, columns=['filename',
                                         'text',
                                         'text_n',
                                         'box_area (%)',
                                         'Text Length',
                                         'is profane',
                                         'nondrant'])
    out_df.to_excel(output_loc, index=False)


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

    # print("Centroid Location: ", (list(set(Col_loc[0]).intersection(Row_loc[0]))[0]))
    return (list(set(Col_loc[0]).intersection(Row_loc[0]))[0])


def textSearch(img, reader, line_col, file, img_with_TD):
    text = reader.readtext(img, workers=multiprocessing.cpu_count())
    n = 0
    if not text:
        # print("No text")
        img_with_TD.append([file, "No Text", n, 0, 0, 0, 0])
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
        # print(imgtext)
        placeholder = [file,
                       imgtext,
                       n,
                       abs(box_area_pct),
                       len(imgtext),
                       profanity.contains_profanity(imgtext),
                       findTextLocInImage(Start_x, Start_y,End_x, End_y, rows, cols)
                       ]

        img_with_TD.append(placeholder)
        n += 1

    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.show()


def main():
    # create list of to fill with lists of info
    img_with_TD = []
    reader = easyocr.Reader(['en'], gpu=False)
    line_col = (0, 255, 0)
    main_dir = 'G:\Dropbox\Dropbox\ResearchRotation\TD_image_groups'

    n = 0
    tot_time = 0
    folderlist = os.listdir(main_dir)
    for folder in folderlist:
        curr_dir = os.path.join(main_dir, folder)
        print(curr_dir)
        # if n > 9:
        #     break
        if os.path.exists(os.path.join(curr_dir, 'output.xlsx')):
            n += 1
            continue
        else:
            filenum = 0
            for file in os.listdir(curr_dir):
                if file.endswith(".jpg"):
                    print("Percent Completion: ", (filenum/len(os.listdir(curr_dir)))*100, "%")
                    start = time.time()
                    img = cv2.imread(os.path.join(curr_dir, file))
                    textSearch(img, reader, line_col, file, img_with_TD)
                    # print(time.time() - start)
                    tot_time += time.time() - start
                    filenum += 1
            print("Total time: ", tot_time)
            print("Avg time: ", tot_time / len(os.listdir(curr_dir)))
            writeToExcel(img_with_TD, curr_dir)
        img_with_TD.clear()
        n += 1


if __name__ == '__main__':
    main()
    print("\nHello World")