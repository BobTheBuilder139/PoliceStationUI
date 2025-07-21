import customtkinter as ctk
from csv import DictWriter

from app_configs import (
    ConfigureFrame,
    ConfigureWindow,
    default_heading_font,
    default_widget_font,
    font_color,
    entry_options,
    button_options,
    textbox_options,
    menu_options,
    padding,
)

from constable_menubar import constable_menu

class Report:
    def __init__(self) -> None:
        from app_configs import constable_name

        self.window = ConfigureWindow(f"{constable_name} -> End of Day Report")
        self.frame = ConfigureFrame(self.window)

        # Default Values
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)

        self.police_station_menu_choice = ctk.StringVar(value="Select Station")
        self.warning_msg = ctk.StringVar(value="")
        self.constable_name = constable_name

        # Widgets
        self.title_label = ctk.CTkLabel(
            self.frame,
            text="Final report",
            font=self.heading_font,
            text_color=font_color,
        )

        self.heading_label = ctk.CTkLabel(
            self.frame,
            text="End Of Day Report",
            font=self.heading_font,
            text_color=font_color,
        )

        self.name_label = ctk.CTkLabel(
            self.frame,
            text="Constable Name*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.date_label = ctk.CTkLabel(
            self.frame,
            text="Date*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        
        
        self.police_station_label = ctk.CTkLabel(
            self.frame,
            text="Police Station*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.work_label = ctk.CTkLabel(
            self.frame,
            text="Work Done",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.name_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Name", 
            **entry_options,
        )

        self.date_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="DD/MM/YYYY", 
            **entry_options,
        )

        self.police_station_menu = ctk.CTkOptionMenu(
            self.frame,
            values=["Station 01", "Station 02", "Station 03"],
            variable=self.police_station_menu_choice,
            font=self.widget_font,
            dropdown_font=self.widget_font,
            **menu_options,
        )

        self.work_textbox = ctk.CTkTextbox(
            self.frame,
            height=padding*4,
            **textbox_options,
        )

        self.warning_label = ctk.CTkLabel(
            self.frame,
            textvariable=self.warning_msg,
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.submit_button = ctk.CTkButton(
            self.frame,
            text="Submit",
            command=self.complaint_submit_clicked,
            **button_options,
        ) 

        # Widget Placements
        self.frame.grid(row=1, column=0)

        self.heading_label.grid(row=0, column=0, columnspan=3, padx=padding, pady=padding)

        self.name_label.grid(row=1, column=0, padx=padding, sticky="sw")
        self.name_entry.grid(row=2, column=0, padx=padding, pady=(0,padding), sticky="nw", ipadx=10)
        self.date_label.grid(row=1, column=1, padx=(0,padding), sticky="sw")
        self.date_entry.grid(row=2, column=1, padx=(0,padding), pady=(0,padding), sticky="nw", ipadx=10)


        self.police_station_label.grid(row=5, column=0, padx=padding, sticky="sw")
        self.police_station_menu.grid(row=6, column=0, padx=padding, pady=(0,padding), sticky="nw", ipadx=10)

        self.work_label.grid(row=7, column=0, columnspan=3, padx=padding, sticky="sw")
        self.work_textbox.grid(row=8, column=0, columnspan=3, padx=padding, pady=(0,padding), sticky="nwe")

        self.warning_label.grid(row=9, column=0, columnspan=3, padx=padding, pady=(0,padding/2))

        self.submit_button.grid(row=10, column=0, columnspan=3, padx=padding, pady=(0,padding))

        # Window Configuration
        self.frame.configure_all_rows(weight=1)
        self.frame.configure_all_columns(weight=1)

        constable_menu(self.window)

        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

    def complaint_submit_clicked(self):
        # Reading Values
        self.name = self.name_entry.get()
        self.date = self.date_entry.get()
        self.station = self.police_station_menu.get()
        self.work = self.work_textbox.get("0.0", "end").strip()

        if not self.name or not self.date or self.station == "Select Station" or not self.work:
            self.warning_msg.set("Please Fill All Required Fields")
            return
        
        self.warning_msg.set("Report submitted")
        self.submit_button.configure(state="disabled") # ensures report is not submitted twice

        new_complaint: dict = {
            "Name" : self.name,
            "Date" : self.date,
            "Station" : self.station,
            "Work Done" : self.work,
        }
        #checking which constable

        match(self.constable_name):
            case 'Constable1':
                try:
                    with open("./database/Constable1.csv", 'a', newline='') as file:
                        writer = DictWriter(file,fieldnames=new_complaint.keys())
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(new_complaint)
                        file.close()
                except Exception as e:
                    print(f"Error appending data to CSV: {e}")
            case 'Constable2':
                try:
                    with open("./database/Constable2.csv", 'a', newline='') as file:
                        writer = DictWriter(file,fieldnames=new_complaint.keys())
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(new_complaint)
                        file.close()
                except Exception as e:
                    print(f"Error appending data to CSV: {e}")
            case 'Constable3':
                try:
                    with open("./database/Constable3.csv", 'a', newline='') as file:
                        writer = DictWriter(file,fieldnames=new_complaint.keys())
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(new_complaint)
                        file.close()
                except Exception as e:
                    print(f"Error appending data to CSV: {e}")
            case 'Constable4':
                try:
                    with open("./database/Constable4.csv", 'a', newline='') as file:
                        writer = DictWriter(file,fieldnames=new_complaint.keys())
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(new_complaint)
                        file.close()
                except Exception as e:
                    print(f"Error appending data to CSV: {e}")
            case 'Constable5':
                try:
                    with open("./database/Constable5.csv", 'a', newline='') as file:
                        writer = DictWriter(file,fieldnames=new_complaint.keys())
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(new_complaint)
                        file.close()
                except Exception as e:
                    print(f"Error appending data to CSV: {e}")
            case 'Constable6':
                try:
                    with open("./database/Constable6.csv", 'a', newline='') as file:
                        writer = DictWriter(file,fieldnames=new_complaint.keys())
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(new_complaint)
                        file.close()
                except Exception as e:
                    print(f"Error appending data to CSV: {e}")


# if __name__ == "__main__":
#     root_window = init_app()
#     Report()
#     root_window.mainloop()