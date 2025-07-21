import customtkinter as ctk
import tkintermapview
from app_configs import (
    ConfigureFrame,
    ConfigureWindow,
    default_heading_font,
    default_widget_font,
    window_color,
    widget_foreground_color,
    nested_window_color,
    font_color,
    button_options,
    padding,
)
from csv import DictReader

from constable_menubar import constable_menu

class ConstableHome:
    def create_view_card(self,frame,name,address):
        card = ConfigureFrame(frame)
        # card.configure(fg_color = widget_foreground_color)
        card.pack(padx = 10, pady = 10,fill = "x")
        title = ctk.CTkLabel(card, text = f"{name} - {address}", font =self.bold_widget_font,text_color=font_color)
        title.grid(row = 0,column = 1,sticky="w",padx = 10, pady = 10)

    def create_card(self,name):

        self.window.withdraw()
        self.case_window = ConfigureWindow(f"{name} -> All cases")
        self.another_frame = ConfigureFrame(self.case_window)
        self.some_frame = ctk.CTkScrollableFrame(self.another_frame)
        self.some_frame.configure(fg_color = nested_window_color,height=600,width = 500)
        self.labelkaframe = ConfigureFrame(self.case_window)

        self.another_frame.grid(row = 0, column = 0,sticky = "s")
        self.some_frame.grid(row = 1, column = 3, columnspan = 3,sticky = "s")
        self.labelkaframe.grid(row = 1, column = 0,sticky = "n",pady = 10)
        self.return_button = ctk.CTkButton(
                self.labelkaframe,
                text="<- Return",
                command=self.return_clicked,
                **button_options,
            )
        self.return_button.grid(row = 0, column = 0)
        with open("./database/complaints.csv","r") as case_database:
            csv_reader = list(DictReader(case_database))

            for row in csv_reader:
                if row["assigned_to"] == name:
                    card = ConfigureFrame(self.some_frame)
                    card.configure(fg_color = widget_foreground_color)
                    card.pack(padx = 10, pady = 10,fill = "x")

                    title = ctk.CTkLabel(card, text = f"{row['name']} - {row['address']}", font =self.bold_widget_font,text_color=font_color)
                    title.grid(row = 0,column = 1,sticky="w",padx = 10, pady = 10)

                    contact = ctk.CTkLabel(card,text=f"Contact: {row['contact']}", font =self.bold_widget_font,text_color=font_color)
                    contact.grid(row = 1, column = 1,sticky = "w",padx = 10, pady = 10)

                    email = ctk.CTkLabel(card, text=f"Email ID: {row['email']}",font =self.bold_widget_font,text_color=font_color)
                    email.grid(row = 2,column = 1,sticky = "w", padx = 10, pady = 10)

                    city = ctk.CTkLabel(card,text = f"City: {row['city']}",font =self.bold_widget_font,text_color=font_color)
                    city.grid(row = 3,column = 1, sticky = "w",padx = 10, pady = 10)

                    complaint_desc = ctk.CTkLabel(card,text = f"Issue: {row["complaint"]}",font=self.bold_widget_font,wraplength=300,justify="left",text_color=font_color)
                    complaint_desc.grid(row = 4,column = 1, sticky = "w",padx = 10, pady = 10)

        self.case_window.configure_all_rows(weight=1)
        self.case_window.configure_all_columns(weight=1)

    def return_clicked(self):
        self.window.deiconify()
        self.window.state("zoomed")
        self.case_window.destroy()

    def __init__(self):
        from app_configs import constable_name
        self.constable_name = constable_name
        #Initializing all the widgets
        self.window = ConfigureWindow(f"{self.constable_name} -> Home")
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)
        self.bold_widget_font = ctk.CTkFont(**default_widget_font, weight="bold")
        
        self.map_frame = ConfigureFrame(self.window)
        self.case_frame = ctk.CTkScrollableFrame(self.window)
        self.pending_cases_label = ctk.CTkLabel(
            self.window,
            text="Pending Cases",
            font=self.heading_font,
            text_color=font_color,
        )
        self.duty_sites = ctk.CTkScrollableFrame(self.window)
        self.view_more_cases = ctk.CTkButton(self.case_frame,text="View all cases",**button_options)
        # self.case_frame2 = ctk.CTkScrollableFrame(self.window)


        # Default Values
        self.heading_font = ctk.CTkFont(**default_heading_font)
        self.widget_font = ctk.CTkFont(**default_widget_font)

        #Configuration(if any)
        self.case_frame.configure(fg_color = window_color,height=600,width = 400)
        self.duty_sites.configure(fg_color = window_color,height=600,width = 400)
        # self.case_frame2.configure(fg_color = widget_foreground_color,height=600,width = 400)

        # duty_sites Widgets
        with open("./database/blockade_details.csv", "r") as file:
            blockade_data = list(DictReader(file))

            row_number=0
            for row in blockade_data:
                if row["constable"] == self.constable_name:
                    blockade_frame = ConfigureFrame(self.duty_sites)

                    ctk.CTkLabel(
                        blockade_frame,
                        text=f"{row["blockades"]}",
                        font=self.heading_font,
                        text_color=font_color,
                    ).grid(row=0, column=0, padx=padding/5, pady=padding/5, sticky="w")

                    ctk.CTkLabel(
                        blockade_frame,
                        text=f"Resources Used: {row["resources"]}",
                        font=self.bold_widget_font,
                        text_color=font_color,
                    ).grid(row=1, column=0, padx=padding/5, pady=(0,padding/5), sticky="w")

                    ctk.CTkLabel(
                        blockade_frame,
                        text=f"Timings: {row["time_slot"]}",
                        font=self.bold_widget_font,
                        text_color=font_color,
                    ).grid(row=2, column=0, padx=padding/5, pady=(0,padding/5), sticky="w")

                    blockade_frame.grid(row=row_number, column=0, padx=padding/5, pady=(padding/5,0), sticky="we")
                    row_number+=1

        #Map Widget
        with open("./database/constable_details.csv") as constable_station_database:
            read_police_station = list(DictReader(constable_station_database))
            map_widget = tkintermapview.TkinterMapView(
                self.map_frame, 
                width=800, 
                height=600, 
                corner_radius=0,
                )
        
            for row in read_police_station:
                if(self.constable_name == "Constable1"):
                    map_widget.set_position(19.09614480079679, 72.855176906498)
                    self.map_marker = map_widget.set_marker(19.09614480079679, 72.855176906498,text = "Your Station")
                elif(self.constable_name == "Constable2"):
                    map_widget.set_position(19.12046853431045, 72.84827378303014)
                    self.map_marker = map_widget.set_marker(19.12046853431045, 72.84827378303014,text = "Your Station")
                elif(self.constable_name == "Constable3"):
                    map_widget.set_position(19.10315098210704, 72.83272629652348)
                    self.map_marker = map_widget.set_marker(19.10315098210704, 72.83272629652348,text = "Your Station")
                elif(self.constable_name == "Constable4"):
                    map_widget.set_position(19.10315098210704, 72.83272629652348)
                    self.map_marker = map_widget.set_marker(19.10315098210704, 72.83272629652348,text = "Your Station")
                elif(self.constable_name == "Constable5"):
                    map_widget.set_position(19.12046853431045, 72.84827378303014)
                    self.map_marker = map_widget.set_marker(19.12046853431045, 72.84827378303014,text = "Your Station")
                elif(self.constable_name == "Constable6"):
                    map_widget.set_position(19.12046853431045, 72.84827378303014)
                    self.map_marker = map_widget.set_marker(19.12046853431045, 72.84827378303014,text = "Your Station")
        #Placement
        self.duty_sites.grid(row = 2, column = 0, padx= padding, pady=padding)
        map_widget.grid(row=0,column=0,padx=10,pady=10)
        self.pending_cases_label.grid(row = 1,column = 3, sticky = "sw")
        self.map_frame.grid(row=2, column=1,columnspan=2, padx=(0, padding), pady=padding)
        self.case_frame.grid(row = 2, column = 3, padx=(0,padding), pady=padding)
        
        #File Handling
        case_database = open("./database/complaints.csv","r")
        csv_reader = list(DictReader(case_database))

        for row in csv_reader:
            if row["assigned_to"] == self.constable_name and row["is_resolved"] == "False":
                self.create_view_card(self.case_frame,row['name'],row['address'])
        
        self.view_more_cases.pack(anchor = "s")
        self.view_more_cases.configure(command = lambda: self.create_card(self.constable_name))

        constable_menu(self.window)

        self.window.configure_all_rows(weight=1)
        self.window.configure_all_columns(weight=1)

# if __name__ == "__main__":
#     root_window = init_app()
#     ConstableHome()
#     root_window.mainloop()