# -- Modules --
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
import tkinter.font
import tkinter.messagebox
import time
from PIL import Image, ImageTk, ImageFilter


class PaintApplicationFrame(Frame):
    # ---- Class Variables ----
    x_pos, y_pos = None, None                       # Define variables to X, Y Position of the Mouse as None (as the User hasn't held the mouse down yet)
    x1, y1, x2, y2 = None, None, None, None         # Define variables to X1+2, Y1+2 which is used for Rectangles, Ovals, Arcs (for Top Left to Bottom Right)

    root = Tk()

    # -- Use for Radio buttons --
    radio_btn_int_var = IntVar()                    # Used for Radio buttons
    radio_btn_int_var.set(1)                        # Update the variable (int_var) and set to the value '1'

    menu_bar = Menu(root)                           # Instantiate the Menu bar

    def __init__(self):
        # -- Canvas --
        Frame.__init__(self)

        # -- Menu Bar --
        menu_1 = Menu(self.menu_bar)
        menu_2 = Menu(self.menu_bar)
        menu_1.add_command(label="Insert Image", command=self.insert_image)
        menu_1.add_command(label="Save Image", command=self.save_image)
        menu_1.add_command(label="Exit", command=self.close)

        menu_2.add_command(label="Blur", command=self.blur)
        menu_2.add_command(label="Contour", command=self.contour)
        menu_2.add_command(label="Detailed", command=self.detail)
        menu_2.add_command(label="Black & White", command=self.black_and_white)
        menu_2.add_command(label="Grayscale", command=self.grayscale)
        menu_2.add_command(label="Half-Tone", command=self.half_tone)

        self.menu_bar.add_cascade(label="File", menu=menu_1)
        self.menu_bar.add_cascade(label="Image Effects", menu=menu_2)

        self.root.config(menu=self.menu_bar)

        # -- Window Object Properties --
        entry_width = 13
        button_pad_y = 10
        canvas_width = 1650
        canvas_height = 900
        button_height = 2
        self.root.geometry("1800x900+50+50")
        self.root.title("Face Full of Paint")

        self.canvas = Canvas(self.root, width=canvas_width, height=canvas_height,
                                   bg="white", highlightbackground="black", cursor="cross")     # Assign to Canvas's root
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=TRUE)                                                      # Initialize .pack() layout

        self.canvas.bind("<ButtonPress-1>", self.button_press)                            # Tracking when the Left Mouse Button is released
        self.canvas.bind("<B1-Motion>", self.button_motion)                               # Tracking motion for pencil tool
        self.canvas.bind("<ButtonRelease-1>", self.button_release)                        # Tracing when the Right Mouse Button is pressed

        # -- Labels and Entry Boxes --
        self.label_1 = Label(self.root, text="Drawing Options", bg="black", fg="white")
        self.label_2 = Label(self.root, text="---------------------")
        self.label_3 = Label(self.root, text="Input Your Text to \n "
                                             "Display it Using \n "
                                             "the 'Text Tool'")

        self.entry_1 = Entry(self.root, width=entry_width)

        self.label_1.pack(fill=X, anchor=N)                         # Note: In order to layout as intended, we must place the .pack() in positions where unusual

        # -- Buttons --
        self.btn1 = Button(self.root, text="Set Pen Color", height=button_height, bg="black", fg="white", command=self.set_pen_color)
        self.btn2 = Button(self.root, text="Clear Canvas", command=self.clear_canvas, width=10)

        self.btn1.pack(side=TOP, pady=button_pad_y, anchor=N)
        self.btn2.pack(side=BOTTOM, pady=button_pad_y)

        self.label_2.pack(side=TOP)
        self.label_3.pack(side=TOP)
        self.entry_1.pack(side=TOP, anchor=N)

        # -- Radio Buttons --
        self.r_btn1 = Radiobutton(self.root, variable=self.radio_btn_int_var, text="Pencil Tool", value=1)          # Different values represent separate indexes (i.e. 1 != 2)
        self.r_btn2 = Radiobutton(self.root, variable=self.radio_btn_int_var, text="Line Tool", value=2)            # The different value of 2 does not mean it is in the same group as value=1
        self.r_btn3 = Radiobutton(self.root, variable=self.radio_btn_int_var, text="Oval Tool", value=3)
        self.r_btn4 = Radiobutton(self.root, variable=self.radio_btn_int_var, text="Rectangle Tool", value=4)
        self.r_btn5 = Radiobutton(self.root, variable=self.radio_btn_int_var, text="Text Tool", value=5)

        self.r_btn1.pack(side=TOP, anchor=N)
        self.r_btn2.pack(side=TOP, anchor=N)
        self.r_btn3.pack(side=TOP, anchor=N)
        self.r_btn4.pack(side=TOP, anchor=N)
        self.r_btn5.pack(side=TOP, anchor=N)

    def button_press(self, event):
        x, y, = event.x, event.y
        print("x = {}, y = {}".format(x, y))            # Print the x and y coordinates when HOLDING down Button-1
        # Upon KeyPress
        self.x1 = event.x                               # Identify the starting x and y position
        self.y1 = event.y

    def button_release(self, event):
        # Reset X and Y position upon release
        self.x_pos = None
        self.y_pos = None

        # Determining which Radio button is selected:
        if self.radio_btn_int_var.get() == 2:           # If Radiobutton{x} is selected...
            self.line_tool(event)                       # ...Run the respective function
        elif self.radio_btn_int_var.get() == 3:         # ...Repeat for all other drawing tools
            self.oval_tool(event)
        elif self.radio_btn_int_var.get() == 4:
            self.rectangle_tool(event)
        elif self.radio_btn_int_var.get() == 5:
            self.text_tool(event)

    def button_motion(self, event):
        self.x2 = event.x                                       # Find x and y position upon Button Release
        self.y2 = event.y

        if self.radio_btn_int_var.get() == 1:                   # If the drawing_tool selected is 'pencil'...
            self.pencil_tool(event)                             # ...Run the pencil_draw function

    def pencil_tool(self, event):
        # Check to see if X and Y have a value. If not, then assign an X and Y value
        if self.x_pos is not None and self.y_pos is not None:
            # Create Line(at self x position, self y position, provide a smooth result)
            event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=TRUE, fill=self.color[1])

        # Constantly provide an update of the X and Y position
        self.x_pos = event.x
        self.y_pos = event.y

    def line_tool(self, event):
        # Check to make sure we have an X and Y coordinate to draw a line
        x, y = event.x, event.y
        if None not in (self.x1, self.y1, self.x2, self.y2):                                                            # If there is NO x and y coordinates set when pressing Mouse Down...
            event.widget.create_line(self.x1, self.y1, self.x2, self.y2,  fill=self.color[1])                           # ...Change the event widget to draw a line at the x1 and y1 point, to the x2 and y2 point
        self.x_pos, self.y_pos = x, y

    def oval_tool(self, event):
        oval_width = 1
        if None not in (self.x1, self.y1, self.x2, self.y2):
            event.widget.create_oval(self.x1, self.y1, self.x2, self.y2, width=oval_width, outline=self.color[1])

    def rectangle_tool(self, event):
        rectangle_width = 1
        if None not in (self.x1, self.y1, self.x2, self.y2):
            event.widget.create_rectangle(self.x1, self.y1, self.x2, self.y2, width=rectangle_width, outline=self.color[1])

    def text_tool(self, event):
        text_size = 15
        if None not in (self.x1, self.y1, self.x2, self.y2):
            # .Font(Style, Size, Bold/Not Bold, Italics/Not Italics
            text_font = tkinter.font.Font(family="Arial", size=text_size)
            event.widget.create_text(self.x1, self.y1, font=text_font, text=self.entry_1.get(), fill=self.color[1])

    def set_pen_color(self):
        self.color = colorchooser.askcolor()

    def clear_canvas(self):
        self.canvas.delete("all")                                                # Clears all items on the canvas

    def insert_image(self):
        img_size = (1300, 1000)                                                  # Used to reduce image pixels down to a viewable size
        filename = filedialog.askopenfilename()                                  # Prompt User for the desired image type

        self.selected_image = Image.open(filename)                               # Display the selected image
        self.selected_image.thumbnail(img_size)                                  # Rescale the size of the selected image
        render_image = ImageTk.PhotoImage(self.selected_image)                   # Display the image in TRUECOLOUR

        self.img_label_1 = Label(self.canvas, image=render_image)  # Assign the label with an image
        self.img_label_1.image = render_image  # Display the label with the loaded image
        self.img_label_1.place(x=175, y=75)  # Place desired X and Y position

    def save_image(self):
        # .save(Writing Type, Default Save Type)
        self.selected_image.save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                        ("All Files", "*.*"))))

    def black_and_white(self):
        start = time.time()
        threshold = (75 + 75 + 75)
        black = (0, 0, 0)                                       # Instantiate Black and White variable with appropriate RGB values
        white = (255, 255, 255)
        original_img = self.selected_image
        width, height = original_img.size                       # Width and Height is equal to the size of the Image's width and height
        img_overlay = original_img.load()                       # Render the image so that we can manipulate RGB values

        for x in range(width):                                  # For every pixel in width (x)...
            for y in range(height):                             # For every pixel in height (y)...
                r, g, b = img_overlay[x, y]                     # ...Instantiate RGB values to be applied to the rendered image
                if r + g + b >= threshold:                      # ...If the any RGB value exceeds the RGB threshold found in the width and height...
                    img_overlay[x, y] = black                   # ...The pixels in the rendered image (x, y) become black
                else:                                           # Otherwise, if they don't exceed...
                    img_overlay[x, y] = white                   # ...They become white

        print("Processing Time:", time.time() - start)
        self.selected_image.save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                        ("All Files", "*.*"))))         # Save the image to apply the effects

    def grayscale(self):
        start = time.time()
        image = self.selected_image
        width, height = image.size                                          # Instantiate image Width and Height
        bitmap = image.load()

        # -- Converting each pixel to grayscale --
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))                              # Get pixels x, y
                r = pixel[0]                                                # Assign each RGB value to their appropriate positions
                g = pixel[1]
                b = pixel[2]
                gray = (r * 0.299) + (g * 0.587) + (b * 0.114)              # Convert each RGB value to respective float values
                bitmap[x, y] = (int(gray), int(gray), int(gray))            # Change each x and y pixel to the newly formulated values

        print("Processing Time:", time.time() - start)
        self.selected_image.save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                        ("All Files", "*.*"))))

    def blur(self):
        self.selected_image.filter(ImageFilter.BLUR).save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                                                 ("All Files", "*.*"))))        # Apply the Blur Effect, then save to see the effect

    def contour(self):
        self.selected_image.filter(ImageFilter.CONTOUR).save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                                                    ("All Files", "*.*"))))     # Applies pencil effect

    def detail(self):
        self.selected_image.filter(ImageFilter.DETAIL).save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                                                   ("All Files", "*.*"))))      # Enhances image sharpness

    def half_tone(self):
        image = self.selected_image
        width, height = image.size                  # Instantiate image dimensions
        bitmap = image.load()                       # Instantiate selected image's bitmap

        for x in range(0, width, 4):
            for y in range(0, height, 4):
                # -- Setting up a form of kernel (4x4) --
                p1 = image.getpixel((x, y))                             # At 0,0 (original)
                p2 = image.getpixel((x, y + 1))                         # At 0,1 (original + 1 column) >> right
                p3 = image.getpixel((x + 1, y))                         # At 1,0 (original + 1 row) >> below
                p4 = image.getpixel((x + 1, y + 1))                     # At 1,1 (original + 1 row & column) >> below + right

                # -- Convert each kernel variable to a grayscale value, total them up --
                gray1 = (p1[0] * 0.299) + (p1[1] * 0.587) + (p1[2] * 0.114)
                gray2 = (p2[0] * 0.299) + (p2[1] * 0.587) + (p2[2] * 0.114)
                gray3 = (p3[0] * 0.299) + (p3[1] * 0.587) + (p3[2] * 0.114)
                gray4 = (p4[0] * 0.299) + (p4[1] * 0.587) + (p4[2] * 0.114)

                saturation = (gray1 + gray2 + gray3 + gray4)            # Sum all values together into one variable

                if saturation > 225:                                    # If the saturation color value is greater than 225...
                    bitmap[x, y] = (255, 255, 255)                      # ...Convert the kernel bitmap to White
                    bitmap[x, y + 1] = (255, 255, 255)
                    bitmap[x + 1, y] = (255, 255, 255)
                    bitmap[x + 1, y + 1] = (255, 255, 255)
                elif saturation > 160:                                  # ...Elif the saturation value is greater than 160...
                    bitmap[x, y] = (255, 255, 255)
                    bitmap[x, y + 1] = (0, 0, 0)                        # ...Convert the kernel bitmap to a white pixel
                    bitmap[x + 1, y] = (255, 255, 255)
                    bitmap[x + 1, y + 1] = (255, 255, 255)
                elif saturation > 95:
                    bitmap[x, y] = (255, 255, 255)
                    bitmap[x, y + 1] = (0, 0, 0)
                    bitmap[x + 1, y] = (0, 0, 0)
                    bitmap[x + 1, y + 1] = (255, 255, 255)
                elif saturation > 35:
                    bitmap[x, y] = (0, 0, 0)
                    bitmap[x, y + 1] = (255, 255, 255)
                    bitmap[x + 1, y] = (0, 0, 0)
                    bitmap[x + 1, y + 1] = (0, 0, 0)
                else:
                    bitmap[x, y] = (0, 0, 0)
                    bitmap[x, y + 1] = (0, 0, 0)
                    bitmap[x + 1, y] = (0, 0, 0)
                    bitmap[x + 1, y + 1] = (0, 0, 0)
        self.save_image()

    def close(self):
        exit()

if __name__ == "__main__":
    PaintApplicationFrame().mainloop()


"""
    def edge_detection(self):
        original_img = self.selected_image
        width, height = original_img.size               # Instantiate image width and height
        amount = 25                                     # Instantiate luminance value

        def average(spectrum):
            (r, g, b) = spectrum
            return (r + g + b) // 3                     # Return a floor division of the RGB values added together

        black_pixel = (0, 0, 0)                         # Instantiate color differentials
        white_pixel = (255, 255, 255)
        modified_img = original_img.copy()              # Instantiate to apply all the new effects to the new image

        # For y in range(<image height> - <amount of pixels affected Vertically>)
        for y in range(height - 1):                                     # For every X and Y pixel in the Original Image...
            # For x in range(<amount of pixels affected Horizontally>, <image width>)
            for x in range(1, width):
                original_pixel = original_img.getpixel((x, y))          # Get each X and Y pixel value
                left = original_img.getpixel((x - 1, y))                # Instantiate left column of the image's X and Y pixels
                bottom = original_img.getpixel((x, y + 1))              # Instantiate bottom row of the image's X and Y pixels
                original_luminance = average(original_pixel)            # Instantiate the Original Luminance value to be the resultant of the Average Function
                left_luminance = average(left)                          # Declare a variable to convert every LEFT pixel (horizontal)
                bottom_lum = average(bottom)                            # Repeat the same for every BOTTOM pixel (vertical)
                if abs(original_luminance - left_luminance) > amount or abs(original_luminance - bottom_lum) > amount:      # If the absolute value of the Original Luminance - every horizontal pixel / vertical pixel is greater than the given amount value...
                    modified_img.putpixel((x, y), black_pixel)                                                              # ...Convert the modified image's X and Y pixel to become black
                else:                                                                                                       # If the absolute value is less than the given amount...
                    modified_img.putpixel((x, y), white_pixel)                                                              # ...Convert the modified image's X and Y pixel to become white
        self.selected_image.save(filedialog.asksaveasfile(mode='w', defaultextension='.jpg', filetypes=(("JPG File", "*.jpg"),
                                                                                                        ("All Files", "*.*"))))
"""

"""
    def get_brightest_pixel(self):
        width, height = self.selected_image.size                                # Instantiate width + height to equal to image size
        format_img = self.selected_image.load()                                 # Format image's INDEX and MEMORY into an ARRAY (x, y)
        brightest_x, brightest_y, max_val = 0, 0, 0                             # Instantiate brightest x + y and max_val to be 0

        for x in range(width):                                                  # For every pixel in X and Y range...
            for y in range(height):
                r, g, b = format_img[x, y]                                      # ...RGB value is instantiated to retrieve the X and Y pixel of selected image
                if r + g + b > max_val:                                         # If the RGB value is greater than the maximum value...
                    brightest_x, brightest_y, self.total = x, y, r + g + b      # ...Brightest X and Y value is equal to Maximum width and height, Total is equal to 255*3 (765) = Brightest color value

        # Display the resultant
        print(("Point X = ", brightest_x,
               "Point Y = ", brightest_y), "\n"
              "Brightest Light Value = ", self.total)
"""