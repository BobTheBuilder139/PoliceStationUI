import customtkinter as ctk
from functools import partial
from PIL import Image
import csv

from app_configs import (
    ConfigureFrame,
    ConfigureWindow,
    default_widget_font,
    font_color,
    entry_options,
    button_options,
    init_app,
    padding,
    screenY,
)

from superintendent_menubar import superintendent_menu

class SuperintendentMessages:
    def __init__(self):

        # Declaring all frames and window
        self.window = ConfigureWindow("Superintendent -> Messages")
        self.constable_frame = ConfigureFrame(self.window)
        self.message_frame = ConfigureFrame(self.window)

        # Default Values
        self.message_sender = "Superintendent"
        self.widget_font = ctk.CTkFont(**default_widget_font)
        self.constable_icon = ctk.CTkImage(dark_image=Image.open("./images/Constable1.jpeg"), size=(padding*2, padding*2))
        self.message_send_icon = ctk.CTkImage(dark_image=Image.open("./database/Messages Files/message_send_icon.png"), size=(padding/2.5, padding/2.5))

        # self.constable_frame Widgets
        self.constable_buttons_list: list[ctk.CTkButton] = []
        for i in range(1,7):
            self.constable_button = ctk.CTkButton(
                self.constable_frame,
                text=f"Constable {i}",
                command=partial(self.show_messages, i),
                **button_options,
            )
            self.constable_button.grid(row=i-1, column=0, padx=padding, pady=padding/2)
            self.constable_buttons_list.append(self.constable_button)

        # self.message_frame Widgets
        ctk.CTkLabel(
            self.message_frame,
            image=self.constable_icon,
            text="",
            font=self.widget_font,
            text_color=font_color,
        ).grid(row=0, column=0, padx=padding, sticky="s")
        ctk.CTkLabel(
            self.message_frame,
            text="Please select a constable to view its messages",
            font=self.widget_font,
            text_color=font_color,
        ).grid(row=1, column=0, padx=padding, sticky="n")

        # Frame Placements
        self.constable_frame.grid(row=1, column=0, padx=padding, pady=padding, sticky="nsew")
        self.message_frame.grid(row=1, column=1, padx=padding, pady=padding, sticky="nsew", columnspan=2)

        superintendent_menu(self.window)

        # Configuring all frames and window
        self.constable_frame.configure_all_rows(weight=1)
        self.constable_frame.configure_all_columns(weight=1)
        self.message_frame.configure_all_rows(weight=1)
        self.message_frame.configure_all_columns(weight=1)
        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

    def clear_message_frame(self):
        for widget in self.message_frame.winfo_children():
            widget.grid_forget()

    def update_message_file(self, required_constable):
        message = self.message_entry.get()
        new_data_row = {"Sender":self.message_sender,
                        "Message":message}

        with open(f"./database/Messages Files/Constable{required_constable}_messages.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Sender", "Message"])
            writer.writerow(new_data_row)

        self.clear_message_frame()
        self.show_messages(required_constable)

    def show_messages(self, required_constable):
        self.clear_message_frame()

        for i in range(0, 6):
            if i == required_constable-1:
                self.constable_buttons_list[i].configure(state="disabled")
            else:
                self.constable_buttons_list[i].configure(state="normal")

        # Nested Frames of self.message_frame
        new_message_frame = ConfigureFrame(self.message_frame)
        prior_messages_display = ctk.CTkScrollableFrame(
            self.message_frame,
            fg_color="transparent",
            height=screenY/2.5,
        )

        # new_message_frame Widgets
        self.message_entry = ctk.CTkEntry(
            new_message_frame, 
            placeholder_text="Enter Message", 
            **entry_options,
        )
        self.message_entry.grid(row=0, column=0, columnspan=5, padx=padding/2, pady=padding/2, sticky="ew")

        send_button = ctk.CTkButton(
            new_message_frame,
            text="Send",
            image=self.message_send_icon,
            compound="right",
            command=lambda: self.update_message_file(required_constable),
            **button_options,
        )
        send_button.grid(row=0, column=5, padx=padding/2, pady=padding/2)

        # prior_messages_display Widgets
        sender_color = "#232323"
        receiver_color = "#2d2d2d"
        with open(f"./database/Messages Files/Constable{required_constable}_messages.csv", "r") as file:
            conversation_data = list(csv.DictReader(file))
            for i in range(len(conversation_data)-1, -1, -1):
                current_row = len(conversation_data)-1 - i
                message_label_frame = ConfigureFrame(prior_messages_display)
                
                if conversation_data[i]["Sender"] == self.message_sender:
                    message_label_frame.configure(fg_color=sender_color)
                    message_label_frame.grid(row=current_row, column=2, columnspan=4, padx=padding/2, pady=padding/4, sticky="e")
                else:
                    message_label_frame.configure(fg_color=receiver_color)
                    message_label_frame.grid(row=current_row, column=0, columnspan=4, padx=padding/2, pady=padding/4, sticky="w")
                
                ctk.CTkLabel(
                    message_label_frame,
                    text=conversation_data[i]["Message"],
                    wraplength=500,
                    justify="left",
                    font=self.widget_font,
                    text_color=font_color,
                ).grid(row=0, column=0, padx=padding/2, pady=padding/3, sticky="ew")

        # Frame Placements and Configuration
        new_message_frame.grid(row=0, column=0, padx=padding/2, pady=(padding/2, 0), sticky="nsew")
        prior_messages_display.grid(row=1, column=0, padx=(0,padding/2), pady=padding/2, sticky="nsew")
        new_message_frame.configure_all_columns(weight=1)
        new_message_frame.configure_all_columns(weight=1)

        rows = prior_messages_display.grid_size()[1]
        for i in range(rows):
            prior_messages_display.grid_rowconfigure(i, weight=1)
        columns = prior_messages_display.grid_size()[0]
        for i in range(columns):
            prior_messages_display.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root_window = init_app()
    SuperintendentMessages()
    root_window.mainloop()