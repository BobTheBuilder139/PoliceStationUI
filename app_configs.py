import customtkinter as ctk

def init_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    global root_window
    root_window = ctk.CTk()
    root_window.withdraw()
    return root_window

# Default Values
screen_size: str = "1920x1080"
screenX, screenY = [int(i) for i in screen_size.split("x")]
window_color: str = "#1e1e1e" # dark black
nested_window_color: str = "#333333" # dark gray
widget_foreground_color: str = "#444444" # less dark gray
widget_border_color: str = "#555555" # lesser dark gray
font_color: str = "cyan2"
widget_text_color: str = "light cyan"
button_hover_color: str = "light cyan" # light cyan
default_corner_radius: int = 15
padding: int = 50
default_heading_font: dict[str, str | int] = dict(family="Sans Serif", size=24, weight="bold")
default_widget_font: dict[str, str | int] = dict(family="Sans Serif", size=14)
entry_options: dict[str, str | int] = {"fg_color" : widget_foreground_color,
                                       "text_color" : widget_text_color,
                                       "border_color" : widget_border_color,
                                        }
button_options: dict[str, str | int] = {"fg_color" : font_color,
                                        "text_color" : window_color,
                                        "hover_color" : button_hover_color,
                                        "corner_radius" : default_corner_radius,
                                         }
segmented_button_options: dict[str, str | int] = {"corner_radius" : default_corner_radius,
                                                   "fg_color" : widget_foreground_color,
                                                   "text_color" : "black",
                                                   "selected_color" : font_color,
                                                   "unselected_color" : widget_border_color,
                                                   "selected_hover_color" : button_hover_color,
                                                   }
textbox_options: dict[str, str | int] = {"fg_color" : widget_foreground_color,
                                         "text_color" : widget_text_color,
                                         "border_color" : widget_border_color,
                                         "corner_radius" : default_corner_radius,
                                         }
menu_options: dict[str, str | int] = {"corner_radius" : default_corner_radius,
                                      "fg_color" : widget_foreground_color,
                                      "button_color" : font_color,
                                      "button_hover_color" : button_hover_color,
                                      "dropdown_fg_color" : widget_border_color,
                                      "dropdown_hover_color" : widget_foreground_color,
                                      "dropdown_text_color" : font_color,
                                      "text_color" : widget_text_color,
                                      }

class Configuration:
    def configure_all_rows(self, **kwargs) -> None:
        rows = self.grid_size()[1]  # type: ignore # grid_size -> tuple (columns, rows)
        for i in range(rows):
            self.grid_rowconfigure(i, **kwargs) # type: ignore

    def configure_all_columns(self, **kwargs) -> None:
        columns = self.grid_size()[0]  # type: ignore # grid_size -> tuple (columns, rows)
        for i in range(columns):
            self.grid_columnconfigure(i, **kwargs) # type: ignore

class ConfigureWindow(Configuration, ctk.CTkToplevel):
    def __init__(self, title_text: str, parent = None):
        super().__init__(root_window if parent is None else parent)
        self.geometry(screen_size)
        self.set_default_color()
        self.create_title(title_text)
        self.state('zoomed')

    def set_default_color(self) -> None:
        self.configure(fg_color=window_color)

    def create_title(self, title_text: str) -> None:
        self.title(title_text)

class ConfigureFrame(Configuration, ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(master=window)
        self.set_nested_window_color()
        self.set_corner_radius()

    def set_corner_radius(self) -> None:
        self.configure(corner_radius=default_corner_radius)

    def set_nested_window_color(self) -> None:
        self.configure(fg_color=nested_window_color)