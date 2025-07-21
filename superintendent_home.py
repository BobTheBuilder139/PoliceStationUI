import customtkinter as ctk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

from app_configs import (
    ConfigureWindow,
    default_heading_font,
    default_widget_font,
    nested_window_color,
    font_color,
    init_app,
    padding,
) 

from superintendent_menubar import superintendent_menu

class SuperintendentHome:
    def __init__(self):
        super().__init__()
        self.window = ConfigureWindow("Superintendent -> Home")
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)

        self.load_constable_data()
        self.display_constables()
        self.display_police_stations()
        self.display_blockade_graph()

        superintendent_menu(self.window)

        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)
        
    def load_constable_data(self):
        self.file_path = "./database/constable_details.csv"
        self.df = pd.read_csv(self.file_path)
    
    def display_constables(self):
        constable_frame = ctk.CTkFrame(self.window, fg_color=nested_window_color, corner_radius=10)
        constable_frame.grid(row=1, column=2, padx=padding/5, pady=padding/5, sticky="ns")

        for index, row in self.df.iterrows():
            self.create_constable_frame(constable_frame, index, row)
    
    def create_constable_frame(self, constable_frame, row_num, data):
        frame = ctk.CTkFrame(constable_frame, fg_color=nested_window_color, corner_radius=10)
        frame.grid(row=row_num, column=0, padx=padding/5, pady=padding/5, sticky="ew")
        
        image_path = os.path.join("images", f"{data['name']}.jpeg")
        try:
            image = Image.open(image_path).resize((50, 50))
            img = ImageTk.PhotoImage(image)
            img_label = ctk.CTkLabel(frame, image=img, text="")
            img_label.grid(row=0, column=0, padx=padding/5)
        except FileNotFoundError:
            pass
        
        info_text = f"{data['name']}\nStation: {data['station']}\nCases: {data['no_of_cases_currently']}/{data['total_no_of_cases']}"
        label = ctk.CTkLabel(frame, text=info_text, font=self.widget_font, text_color=font_color)
        label.grid(row=0, column=1, padx=padding/5, pady=padding/5, sticky="w")
    
    def display_police_stations(self):
        station_frame = ctk.CTkFrame(self.window, fg_color=nested_window_color, corner_radius=10)
        station_frame.grid(row=1, column=0, padx=padding/5, pady=padding/5, sticky="ns")
        
        station_data = self.df.groupby('station').agg({'no_of_cases_currently': 'sum', 'total_no_of_cases': 'sum'})
        for index, (station, data) in enumerate(station_data.iterrows()):
            self.create_station_frame(station_frame, index, station, data)
    
    def create_station_frame(self, parent, row_num, station, data):
        frame = ctk.CTkFrame(parent, fg_color=nested_window_color, corner_radius=10)
        frame.grid(row=row_num, column=0, padx=padding/5, pady=padding/5, sticky="ew")
        
        label = ctk.CTkLabel(frame, text=station, font=self.widget_font, text_color=font_color)
        label.grid(row=0, column=0, padx=padding/5, pady=padding/5)
        
        fig, ax = plt.subplots(figsize=(3, 2))
        sns.barplot(x=["Pending", "Solved"], y=[data['no_of_cases_currently'], data['total_no_of_cases'] - data['no_of_cases_currently']], ax=ax, palette=["#FF6F61", "#6B8E23"])
        ax.set_title("Case Status", fontsize=8)
        ax.set_ylabel("Cases", fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().grid(row=1, column=0, pady=padding/5)
        canvas.draw()
        
        frame.grid_columnconfigure(0, weight=1)
    def display_blockade_graph(self):
      graph_frame = ctk.CTkFrame(self.window, fg_color=nested_window_color, corner_radius=10)
      graph_frame.grid(row=1, column=1, padx=padding, pady=padding)

      self.window.grid_rowconfigure(1, weight=1)
      self.window.grid_columnconfigure(1, weight=1)
      file_path = "./database/blockade_details.csv"
      try:
         df = pd.read_csv(file_path)
      except FileNotFoundError:
        print("CSV not found!")
        return
      fig, ax = plt.subplots(figsize=(4, 3))
      ax.plot(df['day'], df['blockades'], marker='o', label='Blockades', color='red')
      ax.plot(df['day'], df['resources'], marker='o', label='Resources', color='green')

      ax.set_title("Blockades & Resources Over Time", fontsize=10)
      ax.set_xlabel("Day", fontsize=8)
      ax.set_ylabel("Count", fontsize=8)
      ax.legend()
      ax.grid(True)
      ax.tick_params(axis='both', labelsize=8)
      canvas = FigureCanvasTkAgg(fig, master=graph_frame)
      canvas.draw()
      canvas.get_tk_widget().grid(row=0, column=0, padx=padding/5, pady=padding/5)
      
      graph_frame.grid_rowconfigure(0, weight=1)
      graph_frame.grid_columnconfigure(0, weight=1)


def main():
    root_window = init_app()
    SuperintendentHome()
    root_window.mainloop()

if __name__ == "__main__":
    main()