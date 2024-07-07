import tkinter as tk
from tkinter import Label, filedialog
from PIL import Image, ImageTk
import os


def resizeImage(width : int, height : int) -> tuple(int, int):
    maxWidth = 1140
    maxHeight = 500

    scaleW = maxWidth/width
    scaleH = maxHeight/height

    scale = min(scaleW, scaleH)

    newWidth = int(width * scale)
    newHeight = int(height * scale)
    
    return newWidth, newHeight

def saveImage(file_path : str) -> None:
    global current_img, current_format
    print("saving")
    current_img.save(file_path, current_format.upper())

def imageDisplayer(file_path : str, isOtherPic : bool) -> None:
        global app, label, current, dir_files, rotate, current_img, current_format

        if isOtherPic == True and (current_img != None) and (rotate % 360 != 0):
            rotate = 360
            saveImage(dir_files[current])    

        current = dir_files.index(file_path)
        current_format = file_path.split(".")[-1]

        img = Image.open(file_path)
        temp_img = img.rotate(rotate, expand = True)

        current_img = temp_img

        x, y = resizeImage(temp_img.width, temp_img.height)
        temp_img = temp_img.resize((x, y))

        pic = ImageTk.PhotoImage(temp_img)
    
        app.geometry("1200x630")
        label.config(image=pic)
        label.image = pic
        label.pack()

def imageUploader() -> None:
    global dir_files

    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = filedialog.askopenfilename(filetypes=fileTypes)
    if len(path):
        rootPath = os.path.split(path)[0]
        dir_files = [f"{rootPath}/{f}" for f in os.listdir(rootPath) if os.path.isfile(f"{rootPath}/{f}") and f.endswith((".png", ".jpg", ".jpeg"))]
        imageDisplayer(path, True)
 
    else:
        print("No file is chosen !! Please choose a file.")

def goLeft(event) -> None:
    global dir_files, current
    if current != None:
        if current - 1 >= 0:
            imageDisplayer(dir_files[current - 1], True)
        else :
            imageDisplayer(dir_files[-1], True)

def goRight(event) -> None:
    global dir_files, current
    if current != None:
        if current + 1 <= len(dir_files) - 1:
            imageDisplayer(dir_files[current + 1], True)
        else :
            imageDisplayer(dir_files[0], True)

def rotateRight(event) -> None:
    global dir_files, current, rotate
    if current != None:
        rotate += 90
        imageDisplayer(dir_files[current], False)

def rotateLeft(event) -> None:
    global dir_files, current, rotate
    if current != None:
        rotate -= 90
        imageDisplayer(dir_files[current], False)

if __name__ == "__main__" :
    current_img = None
    dir_files = []
    current = None
    current_format = None
    
    try:
        rotate = 360
        app=tk.Tk()
        
        width = app.winfo_width()
        height = app.winfo_height()
        app.geometry("%dx%d" % (560 * 2, 270 * 2))
        app.title("hello")

        app.configure(bg= "#808080")

        app.option_add("*Label*Background", "white")
        app.option_add("*Button*Background", "lightgreen")

        label = Label(app)
        label.pack(pady= 10)

        uploadButton = tk.Button(app, text= "upload image", command= imageUploader)
        uploadButton.pack(side = tk.BOTTOM, pady= 20)

        app.bind("<Left>", goLeft)
        app.bind("<Right>", goRight)
        app.bind("<Up>", rotateRight)
        app.bind("<Down>", rotateLeft)

        app.mainloop()
    
    finally:
        if current_img != None and rotate % 360 != 0:
            saveImage(dir_files[current])

