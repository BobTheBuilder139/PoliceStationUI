import customtkinter as ctk
from PIL import Image, ImageTk
import os
import csv

from app_configs import (
    ConfigureWindow,
    ConfigureFrame,
    default_heading_font,
    default_widget_font,
    font_color,
    init_app,
) 

from superintendent_menubar import superintendent_menu

class ConstableList:
    def __init__(self):
        super().__init__()
        self.window = ConfigureWindow("Superintendent -> Constable List")
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)
        
        self.load_constable_data()
        self.display_constables()

        superintendent_menu(self.window)
        
        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

    def load_constable_data(self):
        self.file_path = "./database/constable_details.csv"
        self.df = []
        
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.df.append(row)
    
    def display_constables(self):
        for index, row in enumerate(self.df):
            self.create_constable_frame(index + 1, row)
    
    def create_constable_frame(self, row_num, data):
        frame = ConfigureFrame(self.window)
        frame.grid(row=row_num, column=0, padx=10, pady=5)
        frame.bind("<Button-1>", lambda e, d=data: self.open_assign_window(d))
        
        image_path = os.path.join("images", f"{data['name']}.jpeg")
        try:
            image = Image.open(image_path).resize((50, 50))
            img = ImageTk.PhotoImage(image)
            img_label = ctk.CTkLabel(frame, image=img, text="")
            img_label.grid(row=0, column=0, padx=5)
        except Exception:
            pass
        
        info_text = f"{data['name']}\nStation: {data['station']}\nCases: {data['no_of_cases_currently']}/{data['total_no_of_cases']}\n"
        label = ctk.CTkLabel(frame, text=info_text, font=self.widget_font, text_color=font_color)
        label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    
    def open_assign_window(self, data):
        self.window.withdraw()
        assign_window = ConfigureWindow(parent=self.window, title_text=f"Assign Task -> {data['name']}")
        
        left_frame = ConfigureFrame(assign_window)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ConfigureFrame(assign_window)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        info_text = f"Name: {data['name']}\nStation: {data['station']}\nCases: {data['no_of_cases_currently']}/{data['total_no_of_cases']}\nTime Slot: {data.get('time_slot', 'N/A')}\n"
        info_label = ctk.CTkLabel(left_frame, text=info_text, font=self.widget_font, text_color=font_color, anchor="w")
        info_label.pack(pady=10, padx=10, fill="both")
        
        assign_button = ctk.CTkButton(left_frame, text="Assign Task", command=lambda: self.assign_task(data, assign_window))
        assign_button.pack(pady=5)
        
        index = self.df.index(data)
        image_path = os.path.join("images", f"Constable{index + 1}.jpeg")
        try:

            image = Image.open(image_path).resize((150, 150))
            img = ImageTk.PhotoImage(image)
            img_label = ctk.CTkLabel(right_frame, image=img, text="")
            img_label.image = img
            img_label.pack(pady=10)

            with open(f"./database/{data["name"]}.csv", "r") as eod_report:
                report_data = list(csv.DictReader(eod_report))
                recent_report_data = report_data[-1]
                ctk.CTkLabel(
                    right_frame,
                    text=f"Name: {recent_report_data["Name"]}",
                    font=self.widget_font,
                    text_color=font_color,
                ).pack(pady=10)
                ctk.CTkLabel(
                    right_frame,
                    text=f"Date: {recent_report_data["Date"]}",
                    font=self.widget_font,
                    text_color=font_color,
                ).pack(pady=10)
                ctk.CTkLabel(
                    right_frame,
                    text=recent_report_data["Station"],
                    font=self.widget_font,
                    text_color=font_color,
                ).pack(pady=10)
                ctk.CTkLabel(
                    right_frame,
                    text=f"Work Done: \n{recent_report_data["Work Done"]}",
                    font=self.widget_font,
                    text_color=font_color,
                ).pack(pady=10)

        except Exception:
            pass
    
    def assign_task(self, data, window):
     assign_frame = ConfigureFrame(window)
     assign_frame.pack(pady=10, padx=10, fill="both")

     time_slots = []
     blockade_values = []

     try:
        with open("./database/blockade_details.csv", 'r') as file:
            blockade_data = list(csv.DictReader(file))
            for row in blockade_data:
                time_slots.append(row["time_slot"])
                blockade_values.append(row["blockades"])

     except Exception as e:
        print("Error loading blockade_details.csv:", e)

     time_label = ctk.CTkLabel(assign_frame, text="Select Time Slot:", font=self.widget_font, text_color=font_color)
     time_label.pack()

     time_slot_box = ctk.CTkComboBox(assign_frame, values=sorted(list(time_slots)))
     time_slot_box.pack()

     blockade_label = ctk.CTkLabel(assign_frame, text="Select Blockade:", font=self.widget_font, text_color=font_color)
     blockade_label.pack()

     blockade_slot = ctk.CTkComboBox(assign_frame, values=sorted(list(blockade_values)))
     blockade_slot.pack()

     confirm_button = ctk.CTkButton(
        assign_frame,
        text="Confirm",
        command=lambda: self.save_assignment(data, time_slot_box.get(), blockade_slot.get(), window)
     )
     confirm_button.pack(pady=10)

    
    def save_assignment(self, data, time, blockade, window):
    #   print(data)
      updated_rows = []
      assigned = False
      file_path = "./database/blockade_details.csv"

      try:
         with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["time_slot"] == time and row["blockades"] == blockade:
                    row["constable"] = data["name"]
                    assigned = True
                updated_rows.append(row)
      except FileNotFoundError:
        fieldnames = ["time_slot", "blockades", "constable"]
        updated_rows = []

      if not assigned:
        updated_rows.append({"time_slot": time, "blockades": blockade, "constable": data["name"]})

      with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

      window.destroy()
      self.window.deiconify()
      self.window.state("zoomed")


if __name__ == "__main__":
    root_window = init_app()
    ConstableList()
    root_window.mainloop()