import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


class ChronoLensApp:
    # Time Machine Aesthetic Palette
    COLOR_BG = "#1C1815"  # Dark Walnut
    COLOR_PANEL = "#2B241F"  # Antique Wood
    COLOR_ACCENT = "#C59B27"  # Polished Brass
    COLOR_TEXT = "#F2E8DC"  # Parchment White
    COLOR_BTN = "#3D322A"  # Deep Leather
    COLOR_BTN_HOVER = "#54453A"

    FONT_TITLE = ("Times New Roman", 18, "bold italic")
    FONT_LABEL = ("Georgia", 11)
    FONT_MONO = ("Courier", 10, "bold")

    def __init__(self, root):
        self.root = root
        self.root.title("ChronoLens: Photographic Time Machine")
        self.root.configure(bg=self.COLOR_BG)
        self.root.geometry("880x560")
        self.root.resizable(False, False)

        # Header Title Banner
        header = Frame(root, bg=self.COLOR_BG)
        header.pack(fill=X, pady=12)

        title_lbl = Label(
            header,
            text="⌛ CHRONOLENS: TEMPORAL PHOTOGRAPHY ⌛",
            font=self.FONT_TITLE,
            fg=self.COLOR_ACCENT,
            bg=self.COLOR_BG,
        )
        title_lbl.pack()

        # Control Panel Dashboard
        control_panel = Frame(
            root, bg=self.COLOR_PANEL, bd=2, relief="ridge", padx=15, pady=10
        )
        control_panel.pack(fill=X, padx=20, pady=5)

        # File Import Button
        self.load_btn = Button(
            control_panel,
            text="📜 Import Subject",
            font=self.FONT_MONO,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_BTN,
            activebackground=self.COLOR_BTN_HOVER,
            activeforeground=self.COLOR_ACCENT,
            relief="groove",
            bd=3,
            cursor="hand2",
            command=self.load_image,
        )
        self.load_btn.pack(side=LEFT, padx=10)

        # Era Selection Dropdown Menu
        Label(
            control_panel,
            text="Destination Era:",
            font=self.FONT_LABEL,
            fg=self.COLOR_ACCENT,
            bg=self.COLOR_PANEL,
        ).pack(side=LEFT, padx=(15, 5))

        self.era_options = [
            "Daguerreotype (1840s)",
            "Tintype (1860s)",
            "Sepia Portrait Studio (1900s–1920s)",
            "Kodachrome Summer (1970s)",
            "Disposable Flash (1990s)",
        ]
        self.filter_var = StringVar(value=self.era_options[0])
        self.filter_menu = OptionMenu(
            control_panel, self.filter_var, *self.era_options, command=self.apply_filter
        )
        self.filter_menu.config(
            font=self.FONT_MONO,
            bg=self.COLOR_BTN,
            fg=self.COLOR_TEXT,
            activebackground=self.COLOR_BTN_HOVER,
            activeforeground=self.COLOR_ACCENT,
            bd=2,
            highlightthickness=0,
        )
        self.filter_menu["menu"].config(
            bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, font=self.FONT_MONO
        )
        self.filter_menu.pack(side=LEFT, padx=5)

        # Temporal Dial (Intensity/Kernel Slider)
        # self.kernel_slider = Scale(
        #     control_panel,
        #     from_=1,
        #     to=15,
        #     orient=HORIZONTAL,
        #     label="Temporal Dial",
        #     font=("Courier", 8),
        #     bg=self.COLOR_PANEL,
        #     fg=self.COLOR_TEXT,
        #     troughcolor=self.COLOR_BG,
        #     activebackground=self.COLOR_ACCENT,
        #     highlightthickness=0,
        #     command=self.apply_filter
        # )
        # self.kernel_slider.set(3)
        # self.kernel_slider.pack(side=RIGHT, padx=10)

        # Viewport Display Area
        canvas_frame = Frame(root, bg=self.COLOR_BG)
        canvas_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Original Photo Viewport
        self.canvas_orig = Canvas(
            canvas_frame,
            width=400,
            height=400,
            bg="#0D0B0A",
            highlightbackground=self.COLOR_ACCENT,
            highlightthickness=2,
        )
        self.canvas_orig.pack(side=LEFT, expand=True)

        # Processed Photo Viewport
        self.canvas_filtered = Canvas(
            canvas_frame,
            width=400,
            height=400,
            bg="#0D0B0A",
            highlightbackground=self.COLOR_ACCENT,
            highlightthickness=2,
        )
        self.canvas_filtered.pack(side=RIGHT, expand=True)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not path:
            return
        img = cv2.imread(path)
        if img is None:
            return
        self.image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.display_image(self.image, self.canvas_orig)
        self.apply_filter()

    def apply_filter(self, _=None):
        if not hasattr(self, "image"):
            return

        # Selected drop-down value: self.filter_var.get()
        # Slider value: self.kernel_slider.get()

        era = self.filter_var.get()

        if era == "Daguerreotype (1840s)":
            filtered = self.daguerreotype(self.image)
        elif era == "Tintype (1860s)":
            filtered = self.tintype(self.image)
        elif era == "Sepia Portrait Studio (1900s–1920s)":
            filtered = self.sepia_portrait_studio(self.image)
        elif era == "Kodachrome Summer (1970s)":
            filtered = self.kodachrome_summer(self.image)
        elif era == "Disposable Flash (1990s)":
            filtered = self.disposable_flash(self.image)
        else:
            filtered = self.image.copy()

        self.display_image(filtered, self.canvas_filtered)

    # Filter Presets
    def daguerreotype(self, image):
        h, w = image.shape[:2]
        image = cv2.undistort(
            image,
            np.array([[w, 0, w / 2], [0, w, h / 2], [0, 0, 1]], np.float32),
            np.array([-0.15, 0, 0, 0, 0], np.float32),
        )  # barrel lens curve
        image = cv2.medianBlur(image, 5)  # soft long-exposure smudge
        sepia = np.clip(
            cv2.transform(
                image.astype(np.float32),
                np.array(
                    [
                        [0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131],
                    ]
                ),
            ),
            0,
            255,
        )  # sepia tone
        y, x = np.mgrid[0:h, 0:w]
        mask = np.clip(
            1 - 0.5 * (((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2),
            0,
            1,
        )  # vignette
        return np.clip(sepia * mask[..., None], 0, 255).astype(np.uint8)

    def tintype(self, img):
        h, w = img.shape[:2]
        pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        pts2 = np.float32([[0, h * 0.03], [w, 0], [0, h], [w * 0.98, h * 0.97]])
        img = cv2.warpPerspective(
            img, cv2.getPerspectiveTransform(pts1, pts2), (w, h)
        )  # curled-plate warp
        img = cv2.bilateralFilter(img, 9, 75, 75)  # smooth but defined
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.merge(
            [gray, gray, np.clip(gray.astype(np.int16) + 10, 0, 255).astype(np.uint8)]
        )  # cool silver tint
        noise = np.random.normal(0, 10, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(
            np.uint8
        )  # scratch/dust grain
        y, x = np.mgrid[0:h, 0:w]
        mask = np.clip(
            1 - 0.6 * (((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2),
            0,
            1,
        )
        return np.clip(img.astype(np.float32) * mask[..., None], 0, 255).astype(
            np.uint8
        )  # heavy vignette

    def sepia_portrait_studio(self, img):
        img = cv2.GaussianBlur(img, (0, 0), 1.2)  # soft studio-lens focus
        edges = cv2.Sobel(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), cv2.CV_8U, 1, 1)
        img = cv2.addWeighted(
            img, 0.9, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB), 0.1, 0
        )  # subtle etched detail
        sepia = np.clip(
            cv2.transform(
                img.astype(np.float32),
                np.array(
                    [
                        [0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131],
                    ]
                ),
            ),
            0,
            255,
        ).astype(np.uint8)  # sepia
        ycrcb = cv2.cvtColor(sepia, cv2.COLOR_RGB2YCrCb)
        ycrcb[:, :, 0] = cv2.createCLAHE(clipLimit=1.5).apply(
            ycrcb[:, :, 0]
        )  # soft period contrast
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)

    def kodachrome_summer(self, img):
        h, w = img.shape[:2]
        img = cv2.warpAffine(
            img,
            cv2.getRotationMatrix2D((w / 2, h / 2), np.random.uniform(-2, 2), 1),
            (w, h),
        )  # snapshot tilt
        img = cv2.bilateralFilter(img, 7, 60, 60)  # slide-film smoothness
        img = np.clip(img.astype(np.float32) * [1.15, 1.0, 0.95], 0, 255).astype(
            np.uint8
        )  # warm red/yellow push
        noise = np.random.normal(0, 8, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(
            np.uint8
        )  # fine film grain
        y, x = np.mgrid[0:h, 0:w]
        mask = np.clip(
            1 - 0.35 * (((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2),
            0,
            1,
        )
        return np.clip(img.astype(np.float32) * mask[..., None], 0, 255).astype(
            np.uint8
        )  # light vignette

    def disposable_flash(self, img):
        img = img.copy()
        img = cv2.GaussianBlur(img, (0, 0), 0.8)  # Cheap plastic lens softness
        img = (img // 32 * 32).astype(np.uint8)  # Posterize / reduced color depth
        ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)  # Harsh flash contrast
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        img = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
        leak = np.zeros_like(img, dtype=np.float32)  # Warm light leak

        h, w = img.shape[:2]
        cv2.circle(
            leak,
            (int(w * 0.85), int(h * 0.15)),
            int(min(w, h) * 0.35),
            (60, 140, 255),
            -1,
        )

        leak = cv2.GaussianBlur(leak, (0, 0), 40)

        return np.clip(
            cv2.addWeighted(img.astype(np.float32), 1.0, leak, 0.4, 0), 0, 255
        ).astype(np.uint8)

    def display_image(self, image, canvas):
        # Scales photo proportionally inside 400x400 bounds
        h, w = image.shape[:2]
        scale = min(400 / w, 400 / h)
        new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))

        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        image_pil = Image.fromarray(resized)
        image_tk = ImageTk.PhotoImage(image_pil)

        canvas.delete("all")
        canvas.create_image(200, 200, anchor=CENTER, image=image_tk)
        canvas.image = image_tk


root = Tk()
app = ChronoLensApp(root)
root.mainloop()
