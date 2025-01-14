
# Final Program for Coffee Gui
# EL_Potato was used  


import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import pineworkslabs.RPi as GPIO
import time

archpump = 5  #Archmedies Pump 
dont_touch = 6 #Froather to mix
pump = 23 #Creamer pump
servo = 25 #Servo to start brewing process
GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

GPIO.output(archpump,GPIO.LOW)
GPIO.output(pump,GPIO.LOW)
GPIO.output(dont_touch,GPIO.HIGH)

class CoffeeMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Machine")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        #Restoring presesets that were saved
        self.preset_file = "coffee_presets.json" 
        self.presets = self.load_presets()

        # Set up a main frame with padding for a cleaner look
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Header Label
        header_label = ttk.Label(main_frame, text="Coffee Machine", font=("Arial", 18, "bold"))
        header_label.pack(pady=(0, 20))

        # Coffee amount selection
        coffee_label = ttk.Label(main_frame, text="Select Sugar Amount", font=("Arial", 12))
        coffee_label.pack(anchor="w")
        self.coffee_var = tk.StringVar(value="Medium")
        coffee_options = ["None", "Low", "Medium", "High"]
        coffee_frame = ttk.Frame(main_frame)
        coffee_frame.pack(anchor="w", pady=5)

        # Larger radio buttons for coffee option
        for option in coffee_options:
            radio_button = tk.Radiobutton(coffee_frame, text=option, variable=self.coffee_var, value=option, 
                                          font=("Arial", 12), indicatoron=False, width=10, height=2)
            radio_button.pack(side="left", padx=5)

        # Sugar amount selection
        sugar_label = ttk.Label(main_frame, text="Select Creamer Amount:", font=("Arial", 12))
        sugar_label.pack(anchor="w", pady=(10, 0))
        self.sugar_var = tk.IntVar(value=1)
        sugar_scale = ttk.Scale(main_frame, from_=0, to=5, variable=self.sugar_var, orient="horizontal", length=200)
        sugar_scale.pack(pady=10)

        # Naming preset 
        name_label = ttk.Label(main_frame, text="Enter Name for Preset:", font=("Arial", 12))
        name_label.pack(anchor="w", pady=(10, 0))
        self.name_entry = ttk.Entry(main_frame, font=("Arial", 10))
        self.name_entry.pack(fill="x", padx=10, pady=5)
        self.name_entry.bind("<FocusIn>", self.show_keyboard)

        # Selecting Presets 
        preset_label = ttk.Label(main_frame, text="Select Preset:", font=("Arial", 12))
        preset_label.pack(anchor="w", pady=(10, 0))
        self.preset_var = tk.StringVar(value="Select a preset")
        self.preset_dropdown = ttk.OptionMenu(main_frame, self.preset_var, "Select a preset")
        self.preset_dropdown.pack(fill="x", padx=10, pady=5)
        self.update_preset_dropdown()

        # Buttons for saving preset, loading preset, and brewing coffee
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        save_preset_btn = ttk.Button(button_frame, text="Save Preset", command=self.save_preset)
        save_preset_btn.pack(side="left", padx=10)
        load_preset_btn = ttk.Button(button_frame, text="Load Preset", command=self.load_preset)
        load_preset_btn.pack(side="left", padx=10)
        
        # Brew Button
        brew_button = ttk.Button(main_frame, text="Brew", command=self.brew_coffee)
        brew_button.pack(pady=10)

    def save_preset(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name for the preset.")
            return

        # Save the preset
        self.presets[name] = {
            "coffee": self.coffee_var.get(),
            "sugar": self.sugar_var.get()
        }
        self.save_presets_to_file()
        messagebox.showinfo("Success", f"Preset saved for {name}.")
        
        # Update the dropdown with the new preset
        self.update_preset_dropdown()

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
    
    # Load Preset choices
    def load_preset(self):
        name = self.preset_var.get()
        if name in self.presets:
            preset = self.presets[name]
            self.coffee_var.set(preset["coffee"])
            self.sugar_var.set(preset["sugar"])
            messagebox.showinfo("Loaded", f"Preset loaded for {name}.")
        else:
            messagebox.showerror("Error", f"No preset found for {name}.")

    # Coffee Brewing order
    def brew_coffee(self):

        # Servo makes 1 full rotation to turn on coffee machine
        GPIO.output(servo, GPIO.HIGH) 
        time.sleep(1.5)
        GPIO.output(servo, GPIO.LOW)
        #time.sleep(60) leave 
        self.sugar()
        self.creamer()
        coffee_amount = self.coffee_var.get()
        sugar_amount = self.sugar_var.get()
        print(f"Brewing coffee with {coffee_amount} coffee and {sugar_amount} sugar.")

    def update_preset_dropdown(self):
        # Clear and update dropdown options
        menu = self.preset_dropdown["menu"]
        menu.delete(0, "end")
        
        # Add new options
        for name in self.presets.keys():
            menu.add_command(label=name, command=lambda value=name: self.preset_var.set(value))

    def save_presets_to_file(self):
        # Save presets to a JSON file
        with open(self.preset_file, "w") as file:
            json.dump(self.presets, file)

    def load_presets(self):
        # Load presets from a JSON file, if it exists
        if os.path.exists(self.preset_file):
            with open(self.preset_file, "r") as file:
                return json.load(file)
        return {}

    
    def sugar(self):
        # Different variants for sugar amount
        sugarA = self.coffee_var.get()
        if sugarA == ("Low"):
            GPIO.output(archpump, GPIO.HIGH)
            time.sleep(15)
            GPIO.output(archpump, GPIO.LOW)
        elif sugarA == ("Medium"):
            GPIO.output(archpump, GPIO.HIGH)
            time.sleep(25)
            GPIO.output(archpump, GPIO.LOW)
        elif sugarA == ("High"):
            GPIO.output(archpump, GPIO.HIGH)
            time.sleep(35)
            GPIO.output(archpump, GPIO.LOW)

    def creamer(self):
        # Different variants for creamer amount
        cream = self.sugar_var.get()
        if cream == 1:
            GPIO.output(pump, GPIO.HIGH)
            time.sleep(15)
            GPIO.output(pump, GPIO.LOW)
        elif cream == 2:
            GPIO.output(pump, GPIO.HIGH)
            time.sleep(25)
            GPIO.output(pump, GPIO.LOW)
        elif cream == 3:
            GPIO.output(pump, GPIO.HIGH)
            time.sleep(35)
            GPIO.output(pump, GPIO.LOW)
        elif cream == 4:
            GPIO.output(pump, GPIO.HIGH)
            time.sleep(40)
            GPIO.output(pump, GPIO.LOW)
        elif cream == 5:
            GPIO.output(pump, GPIO.HIGH)
            time.sleep(50)
            GPIO.output(pump, GPIO.LOW)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeMachineGUI(root)
    
    root.mainloop()
