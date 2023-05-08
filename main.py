import time
import cv2
import easyocr
import matplotlib.pyplot as plt
import os
import multiprocessing

def textSearch(img, reader, line_col):
    text = reader.readtext(img)
    for t in text:
        boundbox, text, score = t
        cv2.rectangle(img, (round(boundbox[0][0]), round(boundbox[0][1])), (round(boundbox[2][0]), round(boundbox[2][1])), line_col, 5)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    # input("Press Enter to continue...")

def showANDtell(reader, line_col, folder):
    file = '101695140125063282961832005960060675282_1.jpg'
    img = cv2.imread(os.path.join(folder,file))
    start = time.time()
    textSearch(img, reader, line_col)
    print(time.time()-start)

def main():
    workers = multiprocessing.Pool()


    for worker in workers:
        print(worker)

    # reader = easyocr.Reader(['en'], gpu=False)
    line_col = (0,255,0)

    folder = 'Images'

    # showANDtell(reader, line_col, folder)


    # n = 0
    # tot_time = 0
    # for file in os.listdir(folder):
    #     print(file)
    #     if file.endswith(".jpg"):
    #         img = cv2.imread(os.path.join(folder,file))
    #         start = time.time()
    #         textSearch(img, reader, line_col)
    #         print(time.time() - start)
    #         tot_time += time.time() - start
    #         n+=1
    # avg_time = tot_time/n
    # print("Total time: ", tot_time)
    # print("Avg time: ", avg_time)









# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    print("Hello World\n")