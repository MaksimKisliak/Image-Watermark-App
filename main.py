from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox


class WatermarkApp:
    def __init__(self, master):
        self.master = master
        master.title("Watermark App")

        # Creating frames
        self.original_frame = Frame(master)
        self.watermark_frame = Frame(master)
        self.output_frame = Frame(master)

        # Creating widgets for original frame
        self.original_label = Label(
            self.original_frame, text="Original Image", font=("Helvetica", 16)
        )
        self.original_button = Button(
            self.original_frame, text="Choose an image", command=self.choose_original
        )

        # Creating widgets for watermark frame
        self.watermark_label = Label(
            self.watermark_frame, text="Watermark Image", font=("Helvetica", 16)
        )
        self.watermark_button = Button(
            self.watermark_frame, text="Choose an image", command=self.choose_watermark
        )

        # Creating widgets for output frame
        self.output_label = Label(
            self.output_frame, text="Output Image", font=("Helvetica", 16)
        )
        self.add_button = Button(
            self.master, text="Add watermark", command=self.add_watermark
        )
        self.save_button = Button(
            self.master, text="Save image", command=self.save_image
        )

        # Packing frames
        self.original_frame.grid(row=0, column=0, padx=10, pady=10)
        self.watermark_frame.grid(row=0, column=1, padx=10, pady=10)
        self.output_frame.grid(row=0, column=2, padx=10, pady=10)

        # Packing widgets
        self.original_label.pack(side=TOP, padx=10, pady=10)
        self.original_button.pack(side=TOP, pady=10)
        self.watermark_label.pack(side=TOP, padx=10, pady=10)
        self.watermark_button.pack(side=TOP, pady=10)
        self.output_label.place(x=0, y=0)
        self.add_button.grid(row=1, column=0, padx=10, pady=10)
        self.save_button.grid(row=2, column=0, padx=10, pady=10)

        # Variables
        self.original_image_path = None
        self.watermark_image_path = None
        self.original_image = None
        self.watermark_image = None
        self.output_image = None

    def choose_original(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image", filetypes=(("png files", "*.png"), ("all files", "*.*"))
        )
        if file_path:
            self.original_image_path = file_path
            self.original_image = Image.open(self.original_image_path)
            self.original_image.thumbnail((400, 400))
            self.original_image = ImageTk.PhotoImage(self.original_image)
            self.original_label.configure(image=self.original_image)

    def choose_watermark(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image", filetypes=(("png files", "*.png"), ("all files", "*.*"))
        )
        if file_path:
            self.watermark_image_path = file_path
            self.watermark_image = Image.open(self.watermark_image_path)
            self.watermark_image.thumbnail((400, 400))
            self.watermark_image = ImageTk.PhotoImage(self.watermark_image)
            self.watermark_label.configure(image=self.watermark_image)

    def add_watermark(self):
        if self.original_image_path and self.watermark_image_path:
            # Create PIL Image objects for original and watermark images
            original_image = Image.open(self.original_image_path)
            watermark_image = Image.open(self.watermark_image_path)

            # Create output image
            output_image = Image.new("RGBA", original_image.size)
            output_image.paste(original_image, (0, 0))
            output_image.paste(
                watermark_image,
                (
                    original_image.size[0] - watermark_image.size[0],
                    original_image.size[1] - watermark_image.size[1],
                ),
                mask=watermark_image,
            )
            self.output_image = ImageTk.PhotoImage(output_image)
            self.output_label.configure(image=self.output_image)
            messagebox.showinfo("Watermark added", "Watermark has been added successfully!")

    def save_image(self):
        if self.output_image:
            # Ask user to choose a file path to save the output image
            file_path = filedialog.asksaveasfilename(
                title="Save image",
                filetypes=(("png files", "*.png"), ("all files", "*.*")),
            )
            if file_path:
                # Save the output image to the chosen file path
                output_image = Image.open(self.original_image_path)
                output_image.paste(Image.open(self.watermark_image_path), (0, 0),
                                   mask=Image.open(self.watermark_image_path).convert('RGBA'))
                output_image.save(file_path)


root = Tk()
app = WatermarkApp(root)
root.mainloop()
