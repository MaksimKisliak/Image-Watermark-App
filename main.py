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
            self.original_frame, text="Original Image", font=("Arial", 16)
        )
        self.original_button = Button(
            self.original_frame, text="Choose an image", command=self.choose_original
        )

        # Creating widgets for watermark frame
        self.watermark_label = Label(
            self.watermark_frame, text="Watermark Image", font=("Arial", 16)
        )
        self.watermark_button = Button(
            self.watermark_frame, text="Choose an image", command=self.choose_watermark
        )

        # Creating widgets for output frame
        self.output_label = Label(
            self.output_frame, text="Proportionally Resized Image", font=("Arial", 16)
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

        # Packing widgets for original frame
        self.original_label.grid(row=0, column=0, padx=10, pady=10)
        self.original_button.grid(row=1, column=0, pady=10)

        # Packing widgets for watermark frame
        self.watermark_label.grid(row=0, column=0, padx=10, pady=10)
        self.watermark_button.grid(row=1, column=0, pady=10)

        # Packing widgets for output frame
        self.output_label.grid(row=0, column=0, padx=10, pady=10)
        self.save_button.grid(row=1, column=2, pady=10)

        self.add_button.grid(row=1, column=1, padx=10)

        # Variables
        self.original_image_path = None
        self.watermark_image_path = None
        self.original_image = None
        self.watermark_image = None
        self.proportional_output_image = None

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

            # Calculate the scale factor to resize the watermark image based on the size of the original image
            scale_factor = max(original_image.size[0] / watermark_image.size[0],
                               original_image.size[1] / watermark_image.size[1])
            new_width = int(watermark_image.size[0] * scale_factor)
            new_height = int(watermark_image.size[1] * scale_factor)

            # Resize the watermark image to match the size of the original image
            watermark_image = watermark_image.resize((new_width, new_height))

            # Create a new transparent image to paste the original image and the watermark image onto it
            output_image = Image.new('RGBA', original_image.size, (0, 0, 0, 0))

            # Paste the original image onto the output image
            output_image.paste(original_image, (0, 0))

            # Paste the watermark image onto the output image multiple times to cover the entire surface of the original image
            for i in range(int(original_image.size[0] / new_width) + 1):
                for j in range(int(original_image.size[1] / new_height) + 1):
                    x = i * new_width
                    y = j * new_height
                    output_image.alpha_composite(watermark_image, (x, y))

            # Save the original size output image to a variable for saving later
            self.output_image = output_image.copy()

            # Resize the output image to fit within the app frame
            output_image.thumbnail((400, 400))

            # Update the output labels with the output images
            self.proportional_output_image = ImageTk.PhotoImage(output_image)
            self.output_label.configure(image=self.proportional_output_image)

            messagebox.showinfo("Watermark added", "Watermark has been added successfully!")

    def save_image(self):
        if self.output_image:
            # Ask user to choose a file path to save the
            file_path = filedialog.asksaveasfilename(
                title="Save image",
                filetypes=(("png files", "*.png"), ("all files", "*.*")),
                defaultextension=".png"
            )
            if file_path:
                # Save the output image to the chosen file path with its original dimensions
                self.output_image.save(file_path)


root = Tk()
app = WatermarkApp(root)
root.mainloop()

