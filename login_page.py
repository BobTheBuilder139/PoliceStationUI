import customtkinter as ctk
from csv import DictReader

import app_configs
from app_configs import (
    ConfigureFrame,
    ConfigureWindow,
    button_options,
    default_heading_font,
    default_widget_font,
    entry_options,
    font_color,
    padding,
    segmented_button_options,
)
from constable_home_page import ConstableHome
from superintendent_home import SuperintendentHome

class LoginPage:
    def __init__(self) -> None:
        # Primary Login Window and Frame Creation
        self.window = ConfigureWindow("CopTrack Login")
        self.frame = ConfigureFrame(self.window)

        # Default Values
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)

        # Tkinter Variables
        self.position_button_choice = ctk.StringVar(value="")
        self.warning_text = ctk.StringVar(value="")

        # Frame Widgets
        self.heading_label = ctk.CTkLabel(
            self.frame,
            text="CopTrack Login",
            font=self.heading_font,
            text_color=font_color,
        )

        self.username_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Username", 
            **entry_options,
        ) 

        self.password_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Password", 
            show="*", 
            **entry_options,
        ) 

        self.position_button = ctk.CTkSegmentedButton(
            self.frame,
            values=["Superintendent", "Constable"],
            font=self.widget_font,
            variable=self.position_button_choice,
            **segmented_button_options,
        ) 

        self.submit_button = ctk.CTkButton(
            self.frame,
            text="Submit",
            command=self.login_submit_clicked,
            **button_options,
        )

        self.warning_label = ctk.CTkLabel(
            self.frame,
            textvariable=self.warning_text,
            font=self.widget_font,
            text_color=font_color,
        )

        # Widget Placement
        self.frame.grid(row=0, column=0)
        self.heading_label.grid(row=0, column=0, padx=padding, pady=padding)
        self.username_entry.grid(row=1, column=0, padx=padding, pady=(0, padding))
        self.password_entry.grid(row=2, column=0, padx=padding, pady=(0, padding))
        self.position_button.grid(row=3, column=0, padx=padding, pady=(0, padding))
        self.submit_button.grid(row=4, column=0, padx=padding, pady=(0, padding/5))
        self.warning_label.grid(row=5, column=0, padx=padding, pady=(0, 3*padding/5))

        # Window Configuration
        self.frame.configure_all_rows(weight=1)
        self.frame.configure_all_columns(weight=1)
        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

    def valid_user(self) -> bool:
        with open("./database/police_credentials.csv", "r") as file:
            data = list(DictReader(file))
            for row in data:
                if row["Position"] == self.login_position and row["Username"] == self.login_username and row["Password"] == self.login_password:
                    return True
            return False

    def login_submit_clicked(self) -> None:
        self.login_username = self.username_entry.get()

        self.login_password = self.password_entry.get()

        self.login_position = self.position_button_choice.get()

        if not self.login_username or not self.login_password or not self.login_position:
            self.warning_text.set("Please Fill All Required Fields")
            return
        
        if not self.valid_user():
            self.warning_text.set("Invalid Credentials")
            return

        match self.login_position:
            case "Superintendent":
                self.window.destroy()
                SuperintendentHome()
            case "Constable":
                self.window.destroy()
                app_configs.constable_name = self.login_username
                ConstableHome()