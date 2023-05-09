import time
import cv2
import easyocr
import matplotlib.pyplot as plt
import os
import multiprocessing
import collections

ImageBox = collections.namedtuple('ImageBox', ['filename', 'text', 'text_n', 'box_start_x', 'box_start_y', 'box_end_x', 'box_end_y'])


def textSearch(img, reader, line_col, file):
    text = reader.readtext(img, workers=len(os.sched_getaffinity(0)))
    print(text)
    n = 0
    img_breakdown = []
    if not text:
        print("No text")
        ImageBox(
            filename=file,
            text="No Text",
            text_n=n,
            box_start_x=0,
            box_start_y=0,
            box_end_x=0,
            box_end_y=0
        )
        img_breakdown.append(ImageBox)
    for t in text:
        boundbox, imgtext, score = t
        cv2.rectangle(img, (round(boundbox[0][0]), round(boundbox[0][1])), (round(boundbox[2][0]), round(boundbox[2][1])), line_col, 5)
        ImageBox(
            filename=file,
            text=imgtext,
            text_n=n,
            box_start_x=round(boundbox[0][0]),
            box_start_y=round(boundbox[0][1]),
            box_end_x=round(boundbox[2][0]),
            box_end_y=round(boundbox[2][1])
        )
        img_breakdown.append(ImageBox)
        n += 1
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    # input("Press Enter to continue...")
    return img_breakdown

def showANDtell(reader, line_col, folder):
    file = '101695140125063282961832005960060675282_1.jpg'
    img = cv2.imread(os.path.join(folder,file))
    start = time.time()
    textSearch(img, reader, line_col)
    print(time.time()-start)

def main():
    # creat list of tuples that have the info we need for each image
    img_with_TD = []
    reader = easyocr.Reader(['en'], gpu=False)
    line_col = (0, 255, 0)
    folder = 'Images'

    n = 0
    tot_time = 0
    for file in os.listdir(folder):
        print(file)
        if file.endswith(".jpg") and n<2:
            start = time.time()
            img = cv2.imread(os.path.join(folder, file))
            img_with_TD.append(textSearch(img, reader, line_col, file))
            print(time.time() - start)
            tot_time += time.time() - start
        else:
            break
        n += 1

    print(len(img_with_TD))
    for i in img_with_TD:
        for j in i:
            print(type(j))
            print(j.filename)

    print("Total time: ", tot_time)
    print("Avg time: ", tot_time/n)




    # showANDtell(reader, line_col, folder)

if __name__ == '__main__':
    main()
    print("Hello World\n")