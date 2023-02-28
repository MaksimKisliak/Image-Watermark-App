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
        self.watermark_opacity_label = Label(
            self.watermark_frame, text="Opacity", font=("Arial", 12)
        )
        self.watermark_opacity_scale = Scale(
            self.watermark_frame, from_=0, to=100, orient=HORIZONTAL, command=self.adjust_opacity
        )

        # Creating widgets for output frame
        self.output_label = Label(
            self.output_frame, text="Watermarked Image", font=("Arial", 16)
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
        self.original_label.grid(row=0, column=0, padx=5, pady=5)
        self.original_button.grid(row=1, column=0, padx=5, pady=5)

        # Packing widgets for watermark frame
        self.watermark_label.grid(row=0, column=0, padx=5, pady=5)
        self.watermark_button.grid(row=1, column=0, padx=5, pady=5)
        self.watermark_opacity_label.grid(row=2, column=0, padx=5, pady=5)
        self.watermark_opacity_scale.grid(row=3, column=0, padx=5, pady=5)

        # Position the "Add Watermark" button below the watermark frame
        self.add_button.grid(row=4, column=1, pady=10)

        # Packing widgets for output frame
        self.output_label.grid(row=0, column=0, padx=5, pady=5)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        # Position the output frame below the original frame
        self.output_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10)

        # Variables
        self.original_image_path = None
        self.watermark_image_path = None
        self.original_image = None
        self.watermark_image = None
        self.watermark_opacity = 100
        self.output_image = None

    def choose_original(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image", filetypes=(("png files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*"))
        )
        if file_path:
            self.original_image_path = file_path
            self.original_image = Image.open(self.original_image_path)
            self.original_image.thumbnail((400, 400))
            self.original_image = ImageTk.PhotoImage(self.original_image)
            self.original_label.configure(image=self.original_image)

    def choose_watermark(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image", filetypes=(("png files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*"))
        )
        if file_path:
            self.watermark_image_path = file_path
            self.watermark_image = Image.open(self.watermark_image_path)
            self.watermark_image.thumbnail((400, 400))
            self.watermark_image = ImageTk.PhotoImage(self.watermark_image)
            self.watermark_label.configure(image=self.watermark_image)
            self.watermark_opacity_scale.set(100)
            self.watermark_opacity = 100

    def adjust_opacity(self, value):
        self.watermark_opacity = int(value)

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

            # Calculate the opacity of the watermark image
            opacity = int(255 * self.watermark_opacity / 100)
            watermark_image.putalpha(opacity)

            # Paste the watermark image onto the output image at the desired position and opacity
            x = (original_image.size[0] - watermark_image.size[0]) // 2
            y = (original_image.size[1] - watermark_image.size[1]) // 2
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
                filetypes=(("png files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*")),
                defaultextension=".jpg"
            )
            if file_path:
                # Save the output image to the chosen file path with its original dimensions
                self.output_image.save(file_path)


root = Tk()
app = WatermarkApp(root)
root.mainloop()