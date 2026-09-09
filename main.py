import cv2  
import numpy as np  
from tkinter import *  
from tkinter import filedialog  
from PIL import Image, ImageTk  

class ImageFilterApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Image Filter App")  

        # Widgets  
        self.load_btn = Button(root, text="Load Image", command=self.load_image)  
        self.filter_var = StringVar(value="Grayscale")  
        self.filter_menu = OptionMenu(root, self.filter_var, "Grayscale", "Gaussian Blur", "Canny Edge", command=self.apply_filter)  
        self.kernel_slider = Scale(root, from_=1, to=15, orient=HORIZONTAL, label="Kernel Size")  
        self.canvas_orig = Canvas(root, width=400, height=400)  
        self.canvas_filtered = Canvas(root, width=400, height=400)  

        # Layout  
        self.load_btn.pack()  
        self.filter_menu.pack()  
        self.kernel_slider.pack()  
        self.canvas_orig.pack(side=LEFT)  
        self.canvas_filtered.pack(side=RIGHT)  

    def load_image(self):  
        path = filedialog.askopenfilename()  
        self.image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)  
        self.display_image(self.image, self.canvas_orig)  

    def apply_filter(self, _=None):  
        if not hasattr(self, 'image'): return  
        kernel = self.kernel_slider.get()  
        kernel = kernel + 1 if kernel % 2 == 0 else kernel  # Ensure odd kernel  

        choice = self.filter_var.get()  
        if choice == "Grayscale":  
            filtered = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)  
            filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)  
        elif choice == "Gaussian Blur":  
            filtered = cv2.GaussianBlur(self.image, (kernel, kernel), 0)  
        elif choice == "Canny Edge":  
            gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)  
            filtered = cv2.Canny(gray, 100, 200)  
            filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)  

        self.display_image(filtered, self.canvas_filtered)  

    def display_image(self, image, canvas):  
        image_pil = Image.fromarray(image)  
        image_tk = ImageTk.PhotoImage(image_pil)  
        canvas.create_image(0, 0, anchor=NW, image=image_tk)  
        canvas.image = image_tk  # Prevent garbage collection  

root = Tk()  
app = ImageFilterApp(root)  
root.mainloop()  