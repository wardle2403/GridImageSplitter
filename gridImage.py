import os
from tkinter import Tk, Canvas, Button, Label, Entry, filedialog, IntVar, Frame
from PIL import Image, ImageTk, ImageDraw

def split_image(image_path, cols, rows, grid_x_start, grid_x_end, grid_y_start, grid_y_end, output_folder="output_images"):
    main_image = Image.open(image_path)
    grid_width = (grid_x_end - grid_x_start) // cols
    grid_height = (grid_y_end - grid_y_start) // rows
    os.makedirs(output_folder, exist_ok=True)

    count = 0
    for row in range(rows):
        for col in range(cols):
            left = grid_x_start + col * grid_width
            upper = grid_y_start + row * grid_height
            right = left + grid_width
            lower = upper + grid_height
            cropped_image = main_image.crop((left, upper, right, lower))
            output_path = os.path.join(output_folder, f"{count}.png")
            cropped_image.save(output_path)
            count += 1

    print(f"Images saved to folder: {output_folder}")

def update_canvas():
    global tk_image, canvas

    cols_val = cols_var.get()
    rows_val = rows_var.get()
    grid_x_start_val = grid_x_start_var.get()
    grid_x_end_val = grid_x_end_var.get()
    grid_y_start_val = grid_y_start_var.get()
    grid_y_end_val = grid_y_end_var.get()

    overlay = img.copy()
    draw = ImageDraw.Draw(overlay)
    grid_width = (grid_x_end_val - grid_x_start_val) // cols_val
    grid_height = (grid_y_end_val - grid_y_start_val) // rows_val

    for i in range(cols_val + 1):
        x = grid_x_start_val + i * grid_width
        draw.line([(x, grid_y_start_val), (x, grid_y_end_val)], fill="red", width=2)
    for i in range(rows_val + 1):
        y = grid_y_start_val + i * grid_height
        draw.line([(grid_x_start_val, y), (grid_x_end_val, y)], fill="red", width=2)

    tk_image = ImageTk.PhotoImage(overlay)
    canvas.create_image(0, 0, anchor="nw", image=tk_image)

def on_slice():
    split_image(image_path, cols_var.get(), rows_var.get(), grid_x_start_var.get(), grid_x_end_var.get(), grid_y_start_var.get(), grid_y_end_var.get())

def open_image():
    global img, tk_image, image_path, canvas

    image_path = filedialog.askopenfilename()
    img = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(img)
    canvas.config(width=img.width, height=img.height)
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    update_canvas()

def increment(var):
    var.set(var.get() + 1)
    update_canvas()

def decrement(var):
    var.set(var.get() - 1)
    update_canvas()

root = Tk()
root.title("Image Grid Splitter")
root.geometry("800x600")
root.configure(bg="#f9f9f9")

cols_var = IntVar(value=8)
rows_var = IntVar(value=7)
grid_x_start_var = IntVar(value=172)
grid_x_end_var = IntVar(value=842)
grid_y_start_var = IntVar(value=102)
grid_y_end_var = IntVar(value=927)

def create_param_control(label_text, var, row, col):
    label = Label(root, text=label_text, bg="#f9f9f9", font=("Arial", 12, "bold"))
    label.grid(row=row, column=col, sticky="e", padx=5,pady=10)

    entry = Entry(root, textvariable=var, width=5, font=("Arial", 12), justify="center")
    entry.grid(row=row, column=col + 1, padx=5)

    button_frame = Frame(root, bg="#f9f9f9")
    button_frame.grid(row=row, column=col + 2, padx=5, sticky="w")

    Button(button_frame, text="▲", command=lambda: increment(var), width=4, height=1, bg="#6BBE45", fg="white", font=("Arial", 6, "bold"), relief="flat").pack(side="top", padx=2)
    Button(button_frame, text="▼", command=lambda: decrement(var), width=4, height=1, bg="#E63946", fg="white", font=("Arial", 6, "bold"), relief="flat").pack(side="top", padx=2)

create_param_control("Columns:", cols_var, 1, 0)
create_param_control("Rows:", rows_var, 1, 3)
create_param_control("Grid X Start:", grid_x_start_var, 2, 0)
create_param_control("Grid X End:", grid_x_end_var, 2, 3)
create_param_control("Grid Y Start:", grid_y_start_var, 3, 0)
create_param_control("Grid Y End:", grid_y_end_var, 3, 3)

open_btn = Button(root, text="Open Image", command=open_image, bg="#2A9D8F", fg="white", font=("Arial", 12, "bold"), relief="raised")
open_btn.grid(row=4, column=0, columnspan=2, pady=10)

slice_btn = Button(root, text="Slice Image", command=on_slice, bg="#F1C40F", fg="white", font=("Arial", 12, "bold"), relief="raised")
slice_btn.grid(row=4, column=3, columnspan=2, pady=10)

canvas = Canvas(root, bg="#ffffff")
canvas.grid(row=5, column=0, columnspan=6, sticky="nsew")

root.mainloop()
