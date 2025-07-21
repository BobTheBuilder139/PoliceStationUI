import customtkinter as ctk
import csv

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

class ConstableComplaintForm:
    def __init__(self) -> None:
        from app_configs import constable_name

        self.window = ConfigureWindow(f"{constable_name} -> Complaint Form")
        self.frame = ConfigureFrame(self.window)

        # Default Values
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)

        self.police_station_menu_choice = ctk.StringVar(value="Select Station")
        self.warning_msg = ctk.StringVar(value="")

        # Widgets
        self.title_label = ctk.CTkLabel(
            self.frame,
            text="File a Complaint",
            font=self.heading_font,
            text_color=font_color,
        )

        self.heading_label = ctk.CTkLabel(
            self.frame,
            text="File a Complaint",
            font=self.heading_font,
            text_color=font_color,
        )

        self.name_label = ctk.CTkLabel(
            self.frame,
            text="Full Name*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.contact_number_label = ctk.CTkLabel(
            self.frame,
            text="Contact Number*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.email_label = ctk.CTkLabel(
            self.frame,
            text="E-Mail ID*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.address_label = ctk.CTkLabel(
            self.frame,
            text="Address",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.city_label = ctk.CTkLabel(
            self.frame,
            text="City",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.police_station_label = ctk.CTkLabel(
            self.frame,
            text="Police Station*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.complaint_label = ctk.CTkLabel(
            self.frame,
            text="Complaint*",
            font=self.widget_font,
            text_color=font_color,
            )
        
        self.name_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Dhruv Vira", 
            **entry_options,
        )

        self.contact_number_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="1234567890", 
            **entry_options,
        )

        self.email_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="example@domain.com", 
            **entry_options,
        )

        self.address_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Sector, Vile Parle, Mumbai", 
            **entry_options,
        )

        self.city_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Mumbai", 
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

        self.complaint_textbox = ctk.CTkTextbox(
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

        self.contact_number_label.grid(row=1, column=1, padx=(0,padding), sticky="sw")
        self.contact_number_entry.grid(row=2, column=1, padx=(0,padding), pady=(0,padding), sticky="nw", ipadx=10)

        self.email_label.grid(row=1, column=2, padx=(0,padding), sticky="sw")
        self.email_entry.grid(row=2, column=2, padx=(0,padding), pady=(0,padding), sticky="nw", ipadx=10)

        self.address_label.grid(row=3, column=0, columnspan=2, padx=padding, sticky="sw")
        self.address_entry.grid(row=4, column=0, columnspan=2, padx=padding, pady=(0,padding), sticky="nwe")

        self.city_label.grid(row=3, column=2, padx=(0,padding), sticky="sw")
        self.city_entry.grid(row=4, column=2, padx=(0,padding), pady=(0,padding), sticky="nw", ipadx=10)

        self.police_station_label.grid(row=5, column=0, padx=padding, sticky="sw")
        self.police_station_menu.grid(row=6, column=0, padx=padding, pady=(0,padding), sticky="nw", ipadx=10)

        self.complaint_label.grid(row=7, column=0, columnspan=3, padx=padding, sticky="sw")
        self.complaint_textbox.grid(row=8, column=0, columnspan=3, padx=padding, pady=(0,padding), sticky="nwe")

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
        self.contact = self.contact_number_entry.get()
        self.email = self.email_entry.get()
        self.address = self.address_entry.get()
        self.city = self.city_entry.get()
        self.station = self.police_station_menu.get()
        self.complaint = self.complaint_textbox.get("0.0", "end").strip()

        if not self.name or not self.contact or not self.email or self.station == "Select Station" or not self.complaint:
            self.warning_msg.set("Please Fill All Required Fields")
            return
        
        self.warning_msg.set("Complaint Registered")
        self.submit_button.configure(state="disabled") # ensures same complaint is not filed twice

        new_complaint: list = [
            self.name,
            self.contact,
            self.email,
            self.address,
            self.city,
            self.station,
            self.complaint,
            "False",
            "None",
        ]

        try:
            with open("./database/complaints.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(new_complaint)
        except Exception as e:
            print(f"Error appending data to CSV: {e}")

# if __name__ == "__main__":
#     root_window = init_app()
#     ConstableComplaintForm()
#     root_window.mainloop()