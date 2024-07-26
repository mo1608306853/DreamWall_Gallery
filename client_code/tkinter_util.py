import tkinter
from PIL import Image, ImageTk, ImageDraw, ImageFont
from method_client import MethodClient

tkinter_tk = None
image_Label = None
always_display = False
count_num = 0
index_num = 0


show_text = ["hello", "Welcome to use"]

def close_tkinter_window():
    if not always_display:
        tkinter_tk.destroy()

def update_image_and_text():
    global tkinter_tk, image_Label, count_num, show_text, index_num, show_text, always_display
    setup_data = MethodClient().read_json()
    show_text = setup_data['show_text']
    always_display = setup_data['always_display']
    try:
        img = Image.open('./show_picture.png')
    except:
        img = Image.open('./show_picture_init.png')
    draw = ImageDraw.Draw(img)
    show_text_len = len(show_text) - 1
    if count_num != show_text_len:
        count_num = show_text_len
        index_num = 0
    if index_num < show_text_len:
        text = f"{show_text[index_num]}"
    else:
        text = f"{show_text[show_text_len]}"
    font = ImageFont.truetype("arial.ttf", 36)
    # font = ImageFont.truetype("./SimSun.ttf", 36)
    # draw.text((100, 100), text, font=font, fill=(253, 230, 224, 255))
    draw.text((100, 100), text, font=font, fill=(0, 0, 0, 255))
    photo = ImageTk.PhotoImage(img)
    image_Label.config(image=photo)
    # Maintain reference to PhotoImage object to prevent garbage collection
    image_Label.image = photo
    tkinter_tk.after(2000, update_image_and_text)
    index_num += 1

def open_tkinter_window():
    global tkinter_tk, image_Label
    tkinter_tk = tkinter.Tk()
    tkinter_tk.iconbitmap('./amd_icon.ico')
    tkinter_tk.title('')
    tkinter_tk.geometry('512x512+95+95')
    img = Image.open('./show_picture.png')
    photo = ImageTk.PhotoImage(img)
    image_Label = tkinter.Label(tkinter_tk, image=photo)
    image_Label.pack()
    # Set a timer here, in milliseconds, divided by 1000 revolutions per second
    tkinter_tk.after(10000, close_tkinter_window)
    update_image_and_text()
    tkinter_tk.mainloop()


if __name__ == "__main__":
    open_tkinter_window()