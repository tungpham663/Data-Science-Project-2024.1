import customtkinter as ctk
from tkinter import *
from tkinterdnd2 import *
from PIL import Image
import pickle

from predict import predict

def loadModel():
    model = pickle.load(open('./trained_model/XGBRegressor.pkl', 'rb'))
    return model

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TITLE  = 'LAPTOP PRICE PREDICTION APP'
SIZE ='1000x700'
ICON_PATH = "./UI/images/logo.jpg"

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def get_text(event):
    input.insert('end', event.data)

root = Tk()

root.geometry(SIZE)
root.title(TITLE)
root.iconbitmap(ICON_PATH)

#main frame can scroll
main_frame = ctk.CTkScrollableFrame(root,
                                   width = 1000,
                                   height = 1000,)
                                   #label_text = 'Music Genre Classification',
                                   #label_fg_color = 'pink',
                                   #label_font=("Roboto",30, "bold"))
main_frame.pack(pady=0)

# Input title
input_title_font = ctk.CTkFont(family="Urbani", size = 25, weight= "bold")
input_label = ctk.CTkLabel(main_frame, text= "Choose or Type the value for each feature below and we'll predict its price!", font =input_title_font) 
input_label.pack(pady = 30)

# Create input frame
input_frame = ctk.CTkFrame(main_frame, width = 1000, height = 400)
input_frame.pack(pady=10)

# Manufactiurer choice
manufacturer = ''
def manufacturerChoice(choice):
    global manufacturer
    manufacturer = choice

manufacturer_label = ctk.CTkLabel(input_frame, text="Choose a manufacture:", font = ("Urbani", 12))
manufacturer_label.grid(row=0, column=0, padx = 5, pady=10)

brands = ['Asus', 'HP', 'Dell', 'Lenovo', 'LG', 'Acer', 'MSI', 'Gigabyte']
manufacturer_box = ctk.CTkComboBox(input_frame, values=brands, command=manufacturerChoice, width=100)
manufacturer_box.grid(row=0, column=1, padx=5, pady=10)

# CPU Manufacturer choice
cpu_manufacturer = ''
def cpuManufacturerChoice(choice):
    global cpu_manufacturer
    cpu_manufacturer = choice
    print('cpu_manufacturer:',str(cpu_manufacturer))

cpu_manifacturer_label = ctk.CTkLabel(input_frame, text="Choose a CPU manufacture:", font = ("Urbani", 12))
cpu_manifacturer_label.grid(row=1, column=0, padx = 5, pady=10)

cpu_brands = ['Intel', 'AMD']
cpu_manufacturer_box = ctk.CTkComboBox(input_frame, values=cpu_brands, command=cpuManufacturerChoice, width=100)
cpu_manufacturer_box.grid(row=1, column=1, padx=5, pady=10)

# CPU Brand Modifier choice
cpu_brand_modifier = ''

cpu_brand_modifier_label = ctk.CTkLabel(input_frame, text="Type CPU brand modifier:", font = ("Urbani", 12))
cpu_brand_modifier_label.grid(row=2, column=0, padx = 5, pady=10)

cpu_brand_modifier_box = ctk.CTkTextbox(input_frame, width=50, height=20, corner_radius=5)
cpu_brand_modifier_box.grid(row=2, column=1, padx=5, pady=10)

# CPU Generation choice
cpu_generation = ''

cpu_generation_label = ctk.CTkLabel(input_frame, text="Type CPU generation:", font = ("Urbani", 12))
cpu_generation_label.grid(row=3, column=0, padx = 5, pady=10)

cpu_generation_box = ctk.CTkTextbox(input_frame, width=50, height=20, corner_radius=5)
cpu_generation_box.grid(row=3, column=1, padx=5, pady=10)

# CPU Speed choice
cpu_speed = ''
def cpuSpeedChoice(choice):
    global cpu_speed
    cpu_speed = float(choice)
    print('cpu speed:', cpu_speed)

cpu_speed_label = ctk.CTkLabel(input_frame, text="Choose CPU speed(GHz):", font = ("Urbani", 12))
cpu_speed_label.grid(row=4, column=0, padx = 5, pady=10)

cpu_speed_options = ['5.80', '5.60', '5.50', '5.40', '5.20', '5.10', '5.00', '4.90', '4.80', '4.70', '4.60', '4.55', '4.50', '4.40', '4.30', '3.80']
cpu_speed_box = ctk.CTkComboBox(input_frame, values=cpu_speed_options, command=cpuSpeedChoice, width=100)
cpu_speed_box.grid(row=4, column=1, padx=5, pady=10)

# RAM
ram = ''
def ramChoice(choice):
    global ram
    ram = int(choice)
    print('ram:', ram)

ram_label = ctk.CTkLabel(input_frame, text="Choose RAM(GB):", font = ("Urbani", 12))
ram_label.grid(row=0, column=2, padx = 5, pady=10)

ram_options = ['8', '16', '32', '24', '64']
ram_box = ctk.CTkComboBox(input_frame, values=ram_options, command=ramChoice, width=100)
ram_box.grid(row=0, column=3, padx=5, pady=10)

# RAM Type
ram_type = ''
def ramTypeChoice(choice):
    global ram_type
    ram_type = choice
    print('ram_type:', ram_type)

ram_type_label = ctk.CTkLabel(input_frame, text="Choose RAM Type:", font = ("Urbani", 12))
ram_type_label.grid(row=1, column=2, padx = 5, pady=10)

ram_type_options = ['LPDDR5', 'LPDDR5X', 'DDR5', 'DDR4']
ram_type_box = ctk.CTkComboBox(input_frame, values=ram_type_options, command=ramTypeChoice, width=100)
ram_type_box.grid(row=1, column=3, padx=5, pady=10)

# Bus
bus = ''
def busChoice(choice):
    global bus
    bus = int(choice)
    print('bus:', bus)

bus_label = ctk.CTkLabel(input_frame, text="Choose Bus(MHz):", font = ("Urbani", 12))
bus_label.grid(row=2, column=2, padx = 5, pady=10)

bus_options = ['8533', '7500', '7467', '6400', '5600', '5200', '4800', '3200', '2666']
bus_box = ctk.CTkComboBox(input_frame, values=bus_options, command=busChoice, width=100)
bus_box.grid(row=2, column=3, padx=5, pady=10)

# GPU Manufacturer
gpu_manufacturer = ''
def gpuManufacturerChoice(choice):
    global gpu_manufacturer
    gpu_manufacturer = choice
    print('GPU Manufacturer:', gpu_manufacturer)

gpu_manufacturer_label = ctk.CTkLabel(input_frame, text="Choose GPU Manufacturer:", font = ("Urbani", 12))
gpu_manufacturer_label.grid(row=4, column=2, padx = 5, pady=10)

gpu_manufacturer_options = ['Nvidia', 'Intel', 'Amd', 'Qualcomm']
gpu_manufacturer_box = ctk.CTkComboBox(input_frame, values=gpu_manufacturer_options, command=gpuManufacturerChoice, width=100)
gpu_manufacturer_box.grid(row=4, column=3, padx=5, pady=10)

# Storage
storage = ''
def storageChoice(choice):
    global storage
    storage = int(choice)
    print('Storage:', storage)

storage_label = ctk.CTkLabel(input_frame, text="Choose storage Size(GB):", font = ("Urbani", 12))
storage_label.grid(row=3, column=2, padx = 5, pady=10)

storage_options = ['256', '512', '1000', '2000']
storage_box = ctk.CTkComboBox(input_frame, values=storage_options, command=storageChoice, width=100)
storage_box.grid(row=3, column=3, padx=5, pady=10)

# Screen Size
screen_size = ''
def screenSizeChoice(choice):
    global screen_size
    screen_size = float(choice)
    print('Screen size:', screen_size)

screen_size_label = ctk.CTkLabel(input_frame, text="Choose Screen Size(inch):", font = ("Urbani", 12))
screen_size_label.grid(row=0, column=4, padx = 5, pady=10)

screen_size_options = ['18', '17', '16.1', '16', '15.6', '14', '13.3']
screen_size_box = ctk.CTkComboBox(input_frame, values=screen_size_options, command=screenSizeChoice, width=100)
screen_size_box.grid(row=0, column=5, padx=5, pady=10)

# Screen Resolution
screen_resolution = ''
def screenResolutionChoice(choice):
    global screen_resolution
    screen_resolution = choice
    print('Screen Resolution:', screen_resolution)

screen_resolution_label = ctk.CTkLabel(input_frame, text="Choose Screen Resolution:", font = ("Urbani", 12))
screen_resolution_label.grid(row=1, column=4, padx = 5, pady=10)

screen_resolution_options = ['1080p', '2K', '3K', '4K']
screen_resolution_box = ctk.CTkComboBox(input_frame, values=screen_resolution_options, command=screenResolutionChoice, width=100)
screen_resolution_box.grid(row=1, column=5, padx=5, pady=10)

# Screen Ratio
screen_ratio = ''
def screenRatioChoice(choice):
    global screen_ratio
    screen_ratio = choice
    print('Screen Ratio:', screen_ratio)

screen_ratio_label = ctk.CTkLabel(input_frame, text="Choose Screen Ratio:", font = ("Urbani", 12))
screen_ratio_label.grid(row=4, column=4, padx = 5, pady=10)

screen_ratio_options = ['16:9', '16:10', '3:2']
screen_ratio_box = ctk.CTkComboBox(input_frame, values=screen_ratio_options, command=screenResolutionChoice, width=100)
screen_ratio_box.grid(row=4, column=5, padx=5, pady=10)

# Weight
weight = ''
# def weightChoice(text):
#     global weight
#     weigth = float(text)
#     print('Weight', weight)

weight_label = ctk.CTkLabel(input_frame, text="Type the weight(kg) (a float):", font = ("Urbani", 12))
weight_label.grid(row=2, column=4, padx = 5, pady=10)

weight_box = ctk.CTkTextbox(input_frame, width=50, height=20, corner_radius=5)
weight_box.grid(row=2, column=5, padx=5, pady=10)

# Battery
battery = ''

battery_label = ctk.CTkLabel(input_frame, text="Type the battery(WHrs) (an integer):", font = ("Urbani", 12))
battery_label.grid(row=3, column=4, padx = 5, pady=10)

battery_box = ctk.CTkTextbox(input_frame, width=50, height=20, corner_radius=5)
battery_box.grid(row=3, column=5, padx=5, pady=10)

# Method Choosing Frame
outputMethod = ''
def chooseMethod(choice):
    global outputMethod
    outputMethod = choice
    print(outputMethod)
    

choose_frame = ctk.CTkFrame(main_frame,
                            width=400,
                            height=30)
choose_frame.pack(pady = 5)

choose_label = ctk.CTkLabel(choose_frame, text="Choose a method to predict", font = ("Urbani", 15))
choose_label.grid(row=0, column=0, padx = 10, pady=10)

methods = ["XGBRegressor"]
choose_box = ctk.CTkComboBox(choose_frame, values=methods, command=chooseMethod, width=150)
choose_box.grid(row=0, column=1, padx=10, pady=10)

#result 
def result():
    manufacturer = str(manufacturer_box.get())
    cpu_manufacturer = str(cpu_manufacturer_box.get())
    cpu_brand_modifier = str(cpu_brand_modifier_box.get(1.0, END))
    cpu_generation = str(cpu_generation_box.get(1.0, END))
    cpu_speed = str(cpu_speed_box.get())
    ram = str(ram_box.get())
    ram_type = str(ram_type_box.get())
    bus = str(bus_box.get())
    gpu_manufacturer = str(gpu_manufacturer_box.get())
    storage = str(storage_box.get())
    screen_size = str(float(screen_size_box.get()))
    screen_resolution = str(screen_resolution_box.get())
    weight = str(weight_box.get(1.0, END))
    battery = str(battery_box.get(1.0, END))
    screen_ratio = str(screen_ratio_box.get())

    cpu = cpu_manufacturer + ' Gen ' + cpu_generation.replace('\n', '') + '.0th'
    # ram_type = 'RAM Type_' + ram_type
    # gpu_manufacturer = 'GPU Manufacturer_' + gpu_manufacturer
    # manufacturer = 'Manufacturer_' + manufacturer
    # screen_resolution = 'Screen Resolution_' + screen_resolution
    cpu_brand_modifier = cpu_brand_modifier.replace('\n', '')
    weight = weight.replace('\n', '')
    battery = battery.replace('\n', '')
    # screen_ratio = 'Screen Ratio_' + screen_ratio

    price = predict(manufacturer, cpu, cpu_brand_modifier, cpu_speed, gpu_manufacturer, ram_type, ram, bus, storage,
                    screen_resolution, screen_ratio, screen_size, battery, weight)

    result_win = ctk.CTkToplevel(root)
    result_win.title("Result Window")
    result_win.geometry('800x800')
    result_win.iconbitmap(ICON_PATH)

    method_label = ctk.CTkLabel(result_win, text=choose_box.get(), font = show_result_font)
    method_label.pack(pady= 10)

    showPredictResult(result_win, manufacturer, cpu, cpu_brand_modifier, cpu_speed, ram, ram_type, bus, gpu_manufacturer, 
                      storage, screen_size, screen_resolution, weight, battery)
    
    result_font = ctk.CTkFont(family="Urbani", size = 25, weight="bold")
    result_label = ctk.CTkLabel(result_win, text='Predict: ' + str(price) + '   triệu VNĐ', font = result_font)
    result_label.pack(pady= 10)

    def back():
        result_win.destroy()
        result_win.update()
        reset()

    #close window
    close_button = ctk.CTkButton(result_win, text="Turn back!", font = ("Urbani", 12), command= back)
    close_button.pack(pady=20)

# Predict button
show_result_font = ctk.CTkFont(family="Urbani", size = 14, weight="bold")
show_result_button = ctk.CTkButton(main_frame,text="Predict!", font= show_result_font, width=80, height=50, corner_radius=50, command = result)
show_result_button.pack(pady = 15)

#Reset button
def reset():
    cpu_generation_box.delete(0.0, 'end')
    cpu_brand_modifier_box.delete(0.0, 'end')
    weight_box.delete(0.0, 'end')
    battery_box.delete(0.0, 'end')

# Show predict result
def showPredictResult(result_win, manufacturer, cpu, cpu_brand_modifier, cpu_speed, ram, ram_type, bus, gpu_manufacturer, 
                      storage, screen_size, screen_resolution, weight, battery):
    manufacturer_result = ctk.CTkLabel(result_win, text="Manufacture: " + manufacturer, font = ("Urbani", 12))
    manufacturer_result.pack(pady= 5)

    cpu_manifacturer_result = ctk.CTkLabel(result_win, text="CPU: " + cpu , font = ("Urbani", 12))
    cpu_manifacturer_result.pack(pady= 5)

    cpu_brand_modifier_result = ctk.CTkLabel(result_win, text="CPU brand modifier: " + cpu_brand_modifier, font = ("Urbani", 12))
    cpu_brand_modifier_result.pack(pady= 5)

    # cpu_generation_result = ctk.CTkLabel(result_win, text="CPU generation: " + cpu_generation, font = ("Urbani", 12))
    # cpu_generation_result.pack(pady= 5)

    cpu_speed_result = ctk.CTkLabel(result_win, text="CPU speed(GHz): " + cpu_speed, font = ("Urbani", 12))
    cpu_speed_result.pack(pady= 5)

    ram_result = ctk.CTkLabel(result_win, text="RAM(GB): " + ram, font = ("Urbani", 12))
    ram_result.pack(pady= 5)

    ram_type_result = ctk.CTkLabel(result_win, text="RAM Type: " + ram_type, font = ("Urbani", 12))
    ram_type_result.pack(pady= 5)

    bus_result = ctk.CTkLabel(result_win, text="Bus(MHz): " + bus, font = ("Urbani", 12))
    bus_result.pack(pady= 5)

    gpu_manufacturer_result = ctk.CTkLabel(result_win, text="GPU Manufacturer: " + gpu_manufacturer, font = ("Urbani", 12))
    gpu_manufacturer_result.pack(pady= 5)

    storage_result = ctk.CTkLabel(result_win, text="Storage Size(GB): " + storage, font = ("Urbani", 12))
    storage_result.pack(pady= 5)  

    screen_size_result = ctk.CTkLabel(result_win, text="Screen Size(inch): " + screen_size, font = ("Urbani", 12))
    screen_size_result.pack(pady= 5)

    screen_resolution_result = ctk.CTkLabel(result_win, text="Screen Resolution: " + screen_resolution, font = ("Urbani", 12))
    screen_resolution_result.pack(pady= 5)

    weight_result = ctk.CTkLabel(result_win, text="Weight(kg): " + weight, font = ("Urbani", 12))
    weight_result.pack(pady= 5)

    battery_result = ctk.CTkLabel(result_win, text="Battery(WHrs): " + battery, font = ("Urbani", 12))
    battery_result.pack(pady= 5)

    price_result = ()



root.mainloop()