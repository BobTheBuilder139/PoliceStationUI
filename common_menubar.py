from functools import partial
import customtkinter as ctk
from collections.abc import Callable

from app_configs import (
    ConfigureFrame,
    ConfigureWindow,
    button_options,
    padding,
    default_corner_radius,
    nested_window_color,
    font_color,
    default_widget_font,
)

class MenuBar:
    def __init__(self, window: ConfigureWindow, tabs_count: int, tabs_names: list[ctk.StringVar], functions_list: list[Callable]) -> None:
        # Default Values
        self.window: ConfigureWindow = window
        self.tab_count = tabs_count
        self.tab_names = tabs_names
        self.functions_list = functions_list
        self.progress_values: list[ctk.DoubleVar] = [ctk.DoubleVar(value=0.0) for _ in range(self.tab_count)]
        self.is_mouse_hovering: list[bool] = [False] * self.tab_count
        self.widget_font = ctk.CTkFont(**default_widget_font)
        
        # Main Frame and Subordinate Frames
        self.frame = ConfigureFrame(window)
        self.subordinate_frames: list[ConfigureFrame] = [ConfigureFrame(self.frame) for _ in range(self.tab_count)]

        # Widget Placements and Configurations
        for i in range(self.tab_count):
            self.subordinate_frames[i].grid(row=0, column=i, padx=padding/2, pady=padding/2)
            self.subordinate_frames[i].configure_all_rows(weight=1)
            self.subordinate_frames[i].configure_all_columns(weight=1)

        self.frame.grid(row=0, column=0, columnspan=window.grid_size()[0], sticky="we")

        self.frame.configure_all_rows(weight=1)
        self.frame.configure_all_columns(weight=1)

        # Widgets
        self.create_widgets()
        self.update_progress_bars()

    def create_widgets(self):
        self.buttons = []
        self.progressbars = []

        for i in range(self.tab_count):
            # Creating Button
            button = ctk.CTkButton(
                self.subordinate_frames[i],
                textvariable=self.tab_names[i],
                font=self.widget_font,
#               width=10,
                **button_options,
            )

            button.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="wes")

            # Mouse Hover Event Binding
            button.bind("<Enter>", lambda event, button_number=i: self.start_progress(event, button_number))
            button.bind("<Leave>", lambda event, button_number=i: self.stop_progress(event, button_number))

            button.configure(command=partial(self.destroy_and_open, self.functions_list[i]))

            self.buttons.append(button)

            # Creating Progress Bars
            progress_bar = ctk.CTkProgressBar(
                self.subordinate_frames[i],
                orientation="horizontal",
                variable=self.progress_values[i],
                height=5,
                border_width=0,
#               width=10,
                corner_radius=default_corner_radius,
                fg_color=nested_window_color,
                progress_color=nested_window_color,
            )

            progress_bar.grid(row=1, column=0, padx=10, pady=5, sticky="wen")

            self.progressbars.append(progress_bar)

    def start_progress(self, event, button_number):
        self.is_mouse_hovering[button_number] = True

    def stop_progress(self, event, button_number):
        self.is_mouse_hovering[button_number] = False

    def update_progress_bars(self):
        for i in range(self.tab_count):
            current_value = self.progress_values[i].get()

            # Checks if mouse is hovering over any button
            if self.is_mouse_hovering[i]:
                self.progressbars[i].configure(progress_color=font_color)
                new_value = current_value + 0.08 # Increases Progress Value
                if new_value > 1.0:
                    new_value = 1.0 # Progress does not reset
            else:
                new_value = current_value - 0.1 # Decreases Progress Value
                if new_value < 0.0:
                    new_value = 0.0 
                    self.progressbars[i].configure(progress_color=nested_window_color)

            self.progress_values[i].set(new_value)

        self.frame.after(25, self.update_progress_bars)

    def destroy_and_open(self, new_window_init: Callable):
        self.window.destroy()
        new_window_init()