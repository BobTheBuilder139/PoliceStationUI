import customtkinter as ctk
from collections.abc import Callable

def constable_menu(window):

    tabs_names: list[ctk.StringVar] = [
        ctk.StringVar(value="Home"),
        ctk.StringVar(value="Messages"),
        ctk.StringVar(value="Complaint Form"),
        ctk.StringVar(value="Report"),
        ctk.StringVar(value="Logout"),
    ]

    from constable_complaint_form import ConstableComplaintForm
    from common_menubar import MenuBar
    from constable_home_page import ConstableHome
    from login_page import LoginPage
    from end_of_day_report import Report
    from constable_messages import ConstableMessages

    functions_list: list[Callable] = [
        ConstableHome,
        ConstableMessages,
        ConstableComplaintForm,
        Report,
        LoginPage,
    ]
    
    MenuBar(
        window,
        len(tabs_names),
        tabs_names,
        functions_list,
    )