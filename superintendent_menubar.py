import customtkinter as ctk
from collections.abc import Callable

from app_configs import ConfigureWindow, init_app
from common_menubar import MenuBar


def superintendent_menu(window):

    tabs_names: list[ctk.StringVar] = [
        ctk.StringVar(value="Home"), # SuperintendentHome
        ctk.StringVar(value="Constables"), # ConstableList, EoDReport
        ctk.StringVar(value="Messages"), # SuperintendentMessages
        ctk.StringVar(value="Complaint Form"), # ComplaintForm
        ctk.StringVar(value="Unresolved Cases"), # UnresolvedCasesTab
        ctk.StringVar(value="Achievements"), # ResolvedCasesTab
        ctk.StringVar(value="Logout"), # LoginPage
    ]

    from login_page import LoginPage
    from complaint_handling import ComplaintForm, UnresolvedCases, Achievements
    from superintendent_home import SuperintendentHome
    from constable_list import ConstableList
    from superintendent_messages import SuperintendentMessages

    functions_list: list[Callable] = [
        SuperintendentHome,
        ConstableList,
        SuperintendentMessages,
        ComplaintForm,
        UnresolvedCases,
        Achievements,
        LoginPage,
    ]
    
    MenuBar(
        window,
        len(tabs_names),
        tabs_names,
        functions_list,
    )

if __name__ == "__main__":
    root_window = init_app()
    window = ConfigureWindow("MenuBar Test")
    ctk.CTkButton(window, text="test1").grid(row=1, column=0)
    superintendent_menu(window)
    window.configure_all_rows(weight=1)
    window.configure_all_columns(weight=1)

    root_window.mainloop()