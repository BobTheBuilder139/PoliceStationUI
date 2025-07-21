import customtkinter as ctk
from functools import partial
import csv
from csv import DictReader, DictWriter
from PIL import Image

from app_configs import (
    ConfigureFrame,
    ConfigureWindow,
    default_heading_font,
    default_widget_font,
    font_color,
    entry_options,
    button_options,
    init_app,
    textbox_options,
    menu_options,
    padding,
    screenX,
    screenY,
)

from superintendent_menubar import superintendent_menu

class ComplaintForm:
    def __init__(self) -> None:

        self.window = ConfigureWindow("Superintendent -> Complaint Form")
        self.frame = ConfigureFrame(self.window)

        # Default Values
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)

        self.police_station_menu_choice = ctk.StringVar(value="Select Station")
        self.warning_msg = ctk.StringVar(value="")

        # Widgets
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

        superintendent_menu(self.window)

        # Window Configuration
        self.frame.configure_all_rows(weight=1)
        self.frame.configure_all_columns(weight=1)

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

class UnresolvedCases:
    def __init__(self):

        self.window = ConfigureWindow("Superintendent -> Unresolved Cases")

        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)
        self.bold_widget_font = ctk.CTkFont(**default_widget_font, weight="bold")

        self.complaint_icon = ctk.CTkImage(dark_image=Image.open("./database/Image Files/complaint_icon.png"), size=(padding*2, padding*2))
        self.resolved_icon = ctk.CTkImage(dark_image=Image.open("./database/Image Files/done_icon.png"), size=(padding*2, padding*2))

        self.title_label = ctk.CTkLabel(
            self.window,
            text="Unresolved Cases",
            font=self.heading_font,
            text_color=font_color,
        )
        self.title_label.grid(row=1, column=0, padx=padding, pady=(padding,0))

        self.main_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent",
            width=screenX,
            height=2*screenY/3,
        )
        self.main_frame.grid(row=2, column=0, padx=padding, pady=padding)

        self.all_case_frames: list[ConfigureFrame] = []
        self.all_case_frames_widgets = []

        with open("./database/complaints.csv", "r") as file:

            data = list(DictReader(file))
            i = 0
            case_row = 0
            case_column = 0
            for row in data:

                if row["is_resolved"] != "False": 
                    continue
                
                i+=1
                self.case_frame = ConfigureFrame(self.main_frame)
                self.case_frame.grid(row=case_row, column=case_column, padx=padding, pady=padding)
                
                if case_column == 2:
                    case_column = 0
                    case_row += 1
                else: 
                    case_column += 1

                # Case Widgets
                self.complaint_icon_label = ctk.CTkLabel(
                    self.case_frame,
                    image=self.complaint_icon,
                    text="",
                )

                self.case_label = ctk.CTkLabel(
                    self.case_frame,
                    text=f"Case {i}",
                    font=self.heading_font,
                    text_color=font_color,
                )

                self.issue_label_p1 = ctk.CTkLabel(
                    self.case_frame,
                    text="Issue: ",
                    font=self.widget_font,
                    text_color=font_color,
                )

                self.issue_label_p2 = ctk.CTkLabel(
                    self.case_frame,
                    text=f"{row["complaint"]}",
                    font=self.bold_widget_font,
                    text_color=font_color,
                )

                self.assigned_label = ctk.CTkLabel(
                    self.case_frame,
                    text=f"Assigned to: {row["assigned_to"]}",
                    font=self.widget_font,
                    text_color=font_color,
                )

                self.mark_as_resolved_button = ctk.CTkButton(
                    self.case_frame,
                    text="Mark as Resolved",
                    **button_options,
                )
                self.mark_as_resolved_button.configure(command=partial(self.mark_as_resolved_button_clicked, self.mark_as_resolved_button))

                self.assign_button = ctk.CTkButton(
                    self.case_frame,
                    text="Assign",
                    **button_options,
                )
                self.assign_button.configure(command=partial(self.assign_button_clicked, row, self.assigned_label, self.assign_button))
                
                if row["assigned_to"] != "None": # if case already assigned
                    self.assign_button.configure(text="Already Assigned", state="disabled")

                # Widget Placements
                self.complaint_icon_label.grid(row=0, column=2, padx=padding/2, pady=padding/2)
                self.case_label.grid(row=0, column=0, padx=padding, pady=padding, columnspan=2, sticky="w")
                self.issue_label_p1.grid(row=1, column=0, padx=(padding,0), pady=(0,padding), sticky="w")
                self.issue_label_p2.grid(row=1, column=1, padx=(0,padding), pady=(0,padding), sticky="w", columnspan=2)
                self.assigned_label.grid(row=2,column=0, padx=padding, pady=(0,padding), columnspan=3, sticky="w")
                self.assign_button.grid(row=3, column=0, padx=padding, pady=(0,padding), columnspan=3)
                self.mark_as_resolved_button.grid(row=4, column=0, padx=padding, pady=(0,padding), columnspan=3)

                self.all_case_frames.append(self.case_frame)
                self.all_case_frames_widgets.append(
                    [self.case_label, self.issue_label_p2, row["assigned_to"], self.mark_as_resolved_button, self.assign_button, self.complaint_icon_label, row]
                )

        superintendent_menu(self.window)

        rows = self.main_frame.grid_size()[1]
        for i in range(rows):
            self.main_frame.grid_rowconfigure(i, weight=1)

        columns = self.main_frame.grid_size()[0]
        for i in range(columns):
            self.main_frame.grid_columnconfigure(i, weight=1)

        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

    def mark_as_resolved_button_clicked(self, clicked_button):

        for i in self.all_case_frames_widgets:
            if clicked_button is i[3]:
                i[3].configure(state="disabled")
                i[4].configure(state="disabled")
                i[5].configure(image=self.resolved_icon)

                new_data = []
                with open("./database/complaints.csv", "r") as file:
                    data = list(DictReader(file))
                    for row in data:
                        if row["complaint"] == i[6]["complaint"]:
                            self.respective_constable = row["assigned_to"]
                            row["is_resolved"] = "True"
                        new_data.append(row)
                    break
        # print(new_data)
        # print(self.respective_constable)
                
        try:
            # Changing is_resolved status in complaints.csv
            self.headers = ["name","contact","email","address","city","station","complaint","is_resolved","assigned_to"]
            # name,contact,email,address,city,station,complaint,is_resolved,assigned_to

            with open("./database/complaints.csv", "w", newline="") as file:
                writer = DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(new_data)

            # Changing no_of_cases_currently in constable_details.csv
            new_constable_data = []
            with open("./database/constable_details.csv", "r") as file:
                constable_data = DictReader(file)
                
                for row in constable_data:
                    if row["name"] == self.respective_constable:
                        no_of_cases_currently = row["no_of_cases_currently"]
                        row["no_of_cases_currently"] = str(int(no_of_cases_currently) - 1)
                    new_constable_data.append(row)

            self.constable_headers = ["name","station","joining_year","no_of_cases_currently","total_no_of_cases"]
            # name,station,joining_year,no_of_cases_currently,total_no_of_cases

            with open("./database/constable_details.csv", "w", newline="") as file:
                writer = DictWriter(file, fieldnames=self.constable_headers)
                writer.writeheader()
                writer.writerows(new_constable_data)
            # print(new_constable_data)

        except Exception as e:
            print(f"Error occured: {e}")

    def assign_button_clicked(self, data_row, assigned_label_to_update, assign_button_to_update):
        self.window.withdraw()
        self.assigning_window = ConfigureWindow("Assigning Case")

        self.complaint_details_frame_left = ConfigureFrame(self.assigning_window)
        self.relevant_constables_frame_right = ConfigureFrame(self.assigning_window)

        with open("./database/complaints.csv", "r") as file:
            self.all_complaints_data = list(DictReader(file))

            for row in self.all_complaints_data:
                if row == data_row:
                    self.complaint_assign_frame_data = row
                    break

            # Widgets for -> complaint_details_frame_left

            self.return_button = ctk.CTkButton(
                self.complaint_details_frame_left,
                text="<- Return",
                command=self.return_clicked,
                **button_options,
            )
            self.return_button.grid(row=0, column=0, padx=padding, pady=padding, sticky="nw")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text="Complaint Details: ",
                font=self.heading_font,
                text_color=font_color,
            ).grid(row=1, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Issue: {self.complaint_assign_frame_data["complaint"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=2, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Assigned to: {self.complaint_assign_frame_data["assigned_to"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=3, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Police Station Of The Area: {self.complaint_assign_frame_data["station"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=4, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text="Complainant Details: ",
                font=self.heading_font,
                text_color=font_color,
            ).grid(row=5, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Name: {self.complaint_assign_frame_data["name"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=6, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Contact No.: {self.complaint_assign_frame_data["contact"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=7, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Email ID: {self.complaint_assign_frame_data["email"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=8, column=0, padx=padding, pady=(0, padding), sticky="w")

            ctk.CTkLabel(
                self.complaint_details_frame_left,
                text=f"Address: {self.complaint_assign_frame_data["address"]}, {self.complaint_assign_frame_data["city"]}",
                font=self.bold_widget_font,
                text_color=font_color,
            ).grid(row=9, column=0, padx=padding, pady=(0, padding), sticky="w")

            # Widgets for -> relevant_constables_frame_right
            ctk.CTkLabel(
                self.relevant_constables_frame_right,
                text="Eligible Constables: ",
                font=self.heading_font,
                text_color=font_color,
            ).grid(row=0, column=0, padx=padding, pady=padding, sticky="nw")

        sub_frame_row = 1
        self.scrollable_constable_frame_right = ctk.CTkScrollableFrame(
            self.relevant_constables_frame_right,
            fg_color="transparent",
            width=screenX/3,
            height=2*screenY/3,
        )
        self.scrollable_constable_frame_right.grid(row=1, column=0, padx=(0, padding), pady=(0, padding))

        with open ("./database/constable_details.csv", "r") as file:
            self.constable_list_data = DictReader(file)

            for row in self.constable_list_data:
                if row["station"] == self.complaint_assign_frame_data["station"]:

                    self.constable_details_sub_frame = ConfigureFrame(self.scrollable_constable_frame_right)
                    ctk.CTkLabel(
                        self.constable_details_sub_frame,
                        text=f"Name: {row["name"]}",
                        font=self.heading_font,
                        text_color=font_color,
                    ).grid(row=1, column=0, padx=padding, pady=(0, padding), sticky="w")

                    ctk.CTkLabel(
                        self.constable_details_sub_frame,
                        text=f"Joining Year: {row["joining_year"]}",
                        font=self.bold_widget_font,
                        text_color=font_color,
                    ).grid(row=2, column=0, padx=padding, pady=(0, padding), sticky="w")

                    ctk.CTkLabel(
                        self.constable_details_sub_frame,
                        text=f"No. Of Cases Currently: {row["no_of_cases_currently"]}",
                        font=self.bold_widget_font,
                        text_color=font_color,
                    ).grid(row=3, column=0, padx=padding, pady=(0, padding), sticky="w")

                    ctk.CTkLabel(
                        self.constable_details_sub_frame,
                        text=f"Total No. Of Cases Solved: {row["total_no_of_cases"]}",
                        font=self.bold_widget_font,
                        text_color=font_color,
                    ).grid(row=4, column=0, padx=padding, pady=(0, padding), sticky="w")

                    self.finally_assign_button = ctk.CTkButton(
                        self.constable_details_sub_frame,
                        text="Assign",
                        **button_options,
                    )
                    self.finally_assign_button.grid(row=5, column=0, padx=padding, pady=(0, padding))
                    self.finally_assign_button.configure(command=partial(self.finally_assigned, row, data_row, assigned_label_to_update, assign_button_to_update))

                    self.constable_details_sub_frame.grid(row=sub_frame_row, column=0, padx=padding, pady=padding)
                    sub_frame_row+=1

        # Frame Placements
        self.complaint_details_frame_left.grid(row=0, column=0, padx=(padding,padding/2), pady=padding)
        self.relevant_constables_frame_right.grid(row=0, column=1, padx=(padding/2, padding), pady=padding)

        # Configurations
        self.complaint_details_frame_left.configure_all_rows(weight=1)
        self.complaint_details_frame_left.configure_all_columns(weight=1)
        self.relevant_constables_frame_right.configure_all_rows(weight=1)
        self.relevant_constables_frame_right.configure_all_columns(weight=1)
        self.assigning_window.configure_all_rows(weight=1)
        self.assigning_window.configure_all_columns(weight=1)

    def return_clicked(self):
        self.window.deiconify()
        self.window.state("zoomed")
        self.assigning_window.destroy()

    def finally_assigned(self, required_constable_data, complaint_to_assign, assigned_label_to_update, assign_button_to_update):
        try:
            # Updating assigned_to in complaints.csv
            with open("./database/complaints.csv", "r") as file:
                data = DictReader(file)
                new_data=[]
                for row in data:
                    if row == complaint_to_assign:
                        row["assigned_to"] = required_constable_data["name"]
                    new_data.append(row)

            assign_button_to_update.configure(text="Already Assigned", state="disabled")

            self.headers = ["name","contact","email","address","city","station","complaint","is_resolved","assigned_to"]
            # name,contact,email,address,city,station,complaint,is_resolved,assigned_to

            with open("./database/complaints.csv", "w", newline="") as file:
                writer = DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(new_data)

            # Updating no_of_cases_currently, total_no_of_cases in constable_details.csv
            new_constable_data = []
            with open("./database/constable_details.csv", "r") as file:
                constable_data = DictReader(file)
                
                for row in constable_data:
                    if row == required_constable_data:
                        no_of_cases_currently = row["no_of_cases_currently"]
                        row["no_of_cases_currently"] = str(int(no_of_cases_currently) + 1)

                        total_no_of_cases = row["total_no_of_cases"]
                        row["total_no_of_cases"] = str(int(total_no_of_cases) + 1)
                    new_constable_data.append(row)

            self.constable_headers = ["name","station","joining_year","no_of_cases_currently","total_no_of_cases"]
            # name,station,joining_year,no_of_cases_currently,total_no_of_cases

            with open("./database/constable_details.csv", "w", newline="") as file:
                writer = DictWriter(file, fieldnames=self.constable_headers)
                writer.writeheader()
                writer.writerows(new_constable_data)
            # print(new_constable_data)

        except Exception as e:
            print(f"Error occured: {e}")

        # Updating assigned label for respective case in UnresolvedCases window
        assigned_label_to_update.configure(text=f"Assigned to: {required_constable_data["name"]}")

        # returning to UnresolvedCases Window
        self.return_clicked()

class Achievements:
    def __init__(self):
        self.window = ConfigureWindow("Superintendent -> Achievements")

        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)
        self.bold_widget_font = ctk.CTkFont(**default_widget_font, weight="bold")

        self.resolved_icon = ctk.CTkImage(dark_image=Image.open("./database/Image Files/done_icon.png"), size=(padding*2, padding*2))

        self.title_label = ctk.CTkLabel(
            self.window,
            text="Achievements",
            font=self.heading_font,
            text_color=font_color,
        )
        self.title_label.grid(row=1, column=0, padx=padding, pady=(padding,0))

        self.main_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent",
            width=screenX,
            height=2*screenY/3,
        )
        self.main_frame.grid(row=2, column=0, padx=padding, pady=padding)

        with open("./database/complaints.csv", "r") as file:

            self.data = list(DictReader(file))
            i = 0
            case_row = 0
            case_column = 0
            for row in self.data:

                if row["is_resolved"] == "False": 
                    continue
                
                i+=1
                self.case_frame = ConfigureFrame(self.main_frame)
                self.case_frame.grid(row=case_row, column=case_column, padx=padding, pady=padding)
                
                if case_column == 2:
                    case_column = 0
                    case_row += 1
                else: 
                    case_column += 1

                # Case Widgets
                self.icon_label = ctk.CTkLabel(
                    self.case_frame,
                    image=self.resolved_icon,
                    text="",
                )

                self.case_label = ctk.CTkLabel(
                    self.case_frame,
                    text=f"Case {i}",
                    font=self.heading_font,
                    text_color=font_color,
                )

                self.issue_label_p1 = ctk.CTkLabel(
                    self.case_frame,
                    text="Issue: ",
                    font=self.widget_font,
                    text_color=font_color,
                )

                self.issue_label_p2 = ctk.CTkLabel(
                    self.case_frame,
                    text=f"{row["complaint"]}",
                    font=self.bold_widget_font,
                    text_color=font_color,
                )

                self.assigned_label = ctk.CTkLabel(
                    self.case_frame,
                    text=f"Resolved by: {row["assigned_to"]}",
                    font=self.widget_font,
                    text_color=font_color,
                )

                # Widget Placements
                self.icon_label.grid(row=0, column=2, padx=padding/2, pady=padding/2)
                self.case_label.grid(row=0, column=0, padx=padding, pady=padding, columnspan=2, sticky="w")
                self.issue_label_p1.grid(row=1, column=0, padx=(padding,0), pady=(0,padding), sticky="w")
                self.issue_label_p2.grid(row=1, column=1, padx=(0,padding), pady=(0,padding), sticky="w", columnspan=2)
                self.assigned_label.grid(row=2,column=0, padx=padding, pady=(0,padding), columnspan=3, sticky="w")

        superintendent_menu(self.window)

        rows = self.main_frame.grid_size()[1]
        for i in range(rows):
            self.main_frame.grid_rowconfigure(i, weight=1)

        columns = self.main_frame.grid_size()[0]
        for i in range(columns):
            self.main_frame.grid_columnconfigure(i, weight=1)

        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

if __name__ == "__main__":
    root_window = init_app()
    ComplaintForm()
    # UnresolvedCases()
    root_window.mainloop()