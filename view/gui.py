import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import excel_spreadsheet as es


class App:

    def __init__(self):

        # Variables for computation
        self.input_file_path = ''
        self.input_file_template = ''
        self.output_file_directory = ''
        self.output_file_template = ''

        # Window settings
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # Open window
        self.app = ctk.CTk()
        self.width = 850
        self.height = 550
        self.spacing = 10
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.title("")

        # Navigation bar
        self.nav_width = 170 - (self.spacing * 2)
        self.nav_height = self.height - (self.spacing * 2)
        nav_frame = ctk.CTkFrame(master=self.app, width=self.nav_width, height=self.nav_height)
        nav_frame.pack_propagate(False)
        nav_frame.pack(padx=(self.spacing, self.spacing / 2), pady=self.spacing, side='left')

        # Title
        title_label = ctk.CTkLabel(
            master=nav_frame,
            text='Make Ready Calculator',
            font=('Arial', 18, 'bold'),
            wraplength=self.nav_width - (self.spacing * 2)
        )
        title_label.pack(padx=self.spacing, pady=self.spacing)

        # Settings button
        settings_button = ctk.CTkButton(
            master=nav_frame,
            text='Settings',
            font=('Arial', 16),
            command=self.settings_frame
        )
        settings_button.pack(padx=self.spacing, pady=self.spacing / 2)

        # Make Ready
        pole_data_button = ctk.CTkButton(
            master=nav_frame,
            text='Pole Data',
            font=('Arial', 16),
            command=self.pole_data_frame
        )
        pole_data_button.pack(padx=self.spacing, pady=self.spacing / 2)

        # Load blank page
        self.page_width = self.width - self.nav_width - (self.spacing * 3)
        self.page_height = self.height - (self.spacing * 2)
        self.page_frame = ctk.CTkFrame(
            master=self.app,
            width=self.page_width,
            height=self.page_height,
            fg_color='transparent'
        )
        self.page_frame.pack_propagate(False)
        self.page_frame.pack(padx=(self.spacing / 2, self.spacing), pady=self.spacing, side='left')

        self.app.mainloop()

    def clear_page_frame(self):
        # Loop over all children of the frame and destroy them
        for widget in self.page_frame.winfo_children():
            widget.destroy()

    def pole_data_frame(self):

        # Clears page
        self.clear_page_frame()

        def format_section():
            # Format section
            format_width = self.page_width
            format_height = (self.page_height - (self.spacing * 1)) / 2
            format_frame = ctk.CTkFrame(master=self.page_frame, width=format_width, height=format_height)
            format_frame.pack_propagate(False)
            format_frame.pack(padx=0, pady=(self.spacing * 0, self.spacing / 2), side='top')

            # Format label
            format_label = ctk.CTkLabel(
                master=format_frame,
                text='Format to Template',
                font=('Arial', 18, 'bold'),
                wraplength=format_width - (self.spacing * 2)
            )
            format_label.pack(padx=self.spacing, pady=(self.spacing, self.spacing / 2), side='top')

            def input_section():

                # Input section
                input_width = (format_width - (self.spacing * 3)) / 2
                input_height = format_height - (self.spacing * 2)
                input_frame = ctk.CTkFrame(master=format_frame, width=input_width, height=input_height)
                input_frame.pack_propagate(False)
                input_frame.pack(
                    padx=(self.spacing, self.spacing / 2),
                    pady=(self.spacing / 2, self.spacing),
                    side='left'
                )

                # Input label
                input_label = ctk.CTkLabel(
                    master=input_frame,
                    text='Input:',
                    font=('Arial', 16, 'bold')
                )
                input_label.pack(padx=self.spacing, pady=self.spacing)

                def input_data_entry():

                    def open_file_dialog():
                        filepath = filedialog.askopenfilename()
                        file_is_selected = filepath != ""
                        if file_is_selected:
                            input_file_path.set(filepath)
                            filename = os.path.basename(filepath)
                            file_entry_label.configure(text=filename)

                    # Data entry frame
                    data_entry_width = input_width - (self.spacing * 2)
                    data_entry_frame = ctk.CTkFrame(master=input_frame, width=data_entry_width, )
                    data_entry_frame.pack(padx=self.spacing, pady=(0, self.spacing))
                    data_entry_frame.grid_columnconfigure(index=0, pad=self.spacing, minsize=145)
                    data_entry_frame.grid_columnconfigure(index=1, pad=self.spacing, minsize=145)
                    data_entry_frame.grid_rowconfigure(index=0, pad=self.spacing)
                    data_entry_frame.grid_propagate(False)

                    # File entry
                    input_file_path = ctk.StringVar(master=data_entry_frame)
                    input_file_path.set('')

                    file_entry_button = ctk.CTkButton(
                        master=data_entry_frame,
                        text="Select Excel File",
                        width=150,
                        font=('Arial', 14),
                        command=open_file_dialog
                    )
                    file_entry_button.grid(row=0, column=0)

                    file_entry_label = ctk.CTkLabel(
                        master=data_entry_frame,
                        text='No File Selected',
                        font=('Arial', 14, 'italic'),
                        text_color='grey',
                    )
                    file_entry_label.grid(row=0, column=1, sticky='W')

                    # Select excel format
                    input_selected_template = ctk.StringVar(master=data_entry_frame)
                    input_selected_template.set('Cable Comm App')

                    excel_option_menu = ctk.CTkOptionMenu(
                        master=data_entry_frame,
                        variable=input_selected_template,
                        values=['Cable Comm App'],
                        width=150,
                        font=('Arial', 14),
                        anchor='center',
                    )
                    excel_option_menu.grid(row=1, column=0)

                    excel_option_label = ctk.CTkLabel(
                        master=data_entry_frame,
                        text='Select Format',
                        font=('Arial', 14, 'italic'),
                        text_color='grey',
                    )
                    excel_option_label.grid(row=1, column=1, sticky='W')

                input_data_entry()

            input_section()

            def output_section():

                def open_folder_dialog():
                    folder_path = filedialog.askdirectory()
                    file_is_selected = folder_path != ""
                    if file_is_selected:
                        folder_name = os.path.basename(folder_path)
                        file_entry_label.configure(text=folder_name)

                # Input section
                output_width = (format_width - (self.spacing * 3)) / 2
                output_height = format_height - (self.spacing * 2)
                output_frame = ctk.CTkFrame(master=format_frame, width=output_width, height=output_height)
                output_frame.pack_propagate(False)
                output_frame.pack(
                    padx=(self.spacing / 2, self.spacing),
                    pady=(self.spacing / 2, self.spacing),
                    side='left'
                )

                output_label = ctk.CTkLabel(
                    master=output_frame,
                    text='Output:',
                    font=('Arial', 16, 'bold')
                )
                output_label.pack(padx=self.spacing, pady=self.spacing)

                # Data entry frame
                data_entry_width = output_width - (self.spacing * 2)
                data_entry_frame = ctk.CTkFrame(master=output_frame, width=data_entry_width, )
                data_entry_frame.pack(padx=self.spacing, pady=(0, self.spacing))
                data_entry_frame.grid_columnconfigure(index=0, minsize=145)
                data_entry_frame.grid_columnconfigure(index=1, minsize=140)
                data_entry_frame.grid_rowconfigure(index=0)
                data_entry_frame.grid_rowconfigure(index=1)
                data_entry_frame.grid_propagate(False)
                entry_spacing = self.spacing / 2

                # Select template
                excel_template_option_menu = ctk.CTkOptionMenu(
                    master=data_entry_frame,
                    values=['PSE'],
                    width=150,
                    font=('Arial', 14),
                    anchor='center',
                )
                excel_template_option_menu.grid(row=0, column=0, padx=entry_spacing, pady=(entry_spacing, entry_spacing / 2))

                excel_option_label = ctk.CTkLabel(
                    master=data_entry_frame,
                    text='Select Template',
                    font=('Arial', 14, 'italic'),
                    text_color='grey',
                )
                excel_option_label.grid(row=0, column=1, sticky='W', padx=entry_spacing, pady=(entry_spacing, entry_spacing / 2))

                # Folder entry
                folder_entry_button = ctk.CTkButton(
                    master=data_entry_frame,
                    text="Select Folder",
                    width=150,
                    font=('Arial', 14),
                    command=open_folder_dialog
                )
                folder_entry_button.grid(row=1, column=0, padx=entry_spacing, pady=entry_spacing / 2)

                file_entry_label = ctk.CTkLabel(
                    master=data_entry_frame,
                    text='No Folder Selected',
                    font=('Arial', 14, 'italic'),
                    text_color='grey',
                )
                file_entry_label.grid(row=1, column=1, sticky='W', padx=entry_spacing, pady=entry_spacing / 2)

                # Create output button
                create_output_button = ctk.CTkButton(
                    master=data_entry_frame,
                    text="Create Spreadsheet",
                    font=('Arial', 14),
                    width=290
                )
                create_output_button.grid(row=2, column=0, columnspan=2, padx=entry_spacing, pady=entry_spacing / 2)

            output_section()

        def violation_section():
            # Violation section
            violation_width = self.page_width
            violation_height = (self.page_height - (self.spacing * 1)) / 2
            violation_frame = ctk.CTkFrame(master=self.page_frame, width=violation_width, height=violation_height)
            violation_frame.pack_propagate(False)
            violation_frame.pack(padx=0, pady=(self.spacing / 2, self.spacing * 0), side='top')

            # Violation label
            violation_label = ctk.CTkLabel(
                master=violation_frame,
                text='Find Violations',
                font=('Arial', 18, 'bold'),
                wraplength=violation_width - (self.spacing * 2)
            )
            violation_label.pack(padx=self.spacing, pady=(self.spacing, self.spacing / 2))

            def input_section():
                # Input section
                input_width = (violation_width - (self.spacing * 3)) / 2
                input_height = violation_height - (self.spacing * 2)
                input_frame = ctk.CTkFrame(master=violation_frame, width=input_width, height=input_height)
                input_frame.pack_propagate(False)
                input_frame.pack(
                    padx=(self.spacing, self.spacing / 2),
                    pady=(self.spacing / 2, self.spacing),
                    side='left'
                )

                input_label = ctk.CTkLabel(
                    master=input_frame,
                    text='Input:',
                    font=('Arial', 16, 'bold')
                )
                input_label.pack(padx=self.spacing, pady=self.spacing)

            input_section()

            def output_section():
                # Input section
                output_width = (violation_width - (self.spacing * 3)) / 2
                output_height = violation_height - (self.spacing * 2)
                output_frame = ctk.CTkFrame(master=violation_frame, width=output_width, height=output_height)
                output_frame.pack_propagate(False)
                output_frame.pack(
                    padx=(self.spacing / 2, self.spacing),
                    pady=(self.spacing / 2, self.spacing),
                    side='left'
                )

                output_label = ctk.CTkLabel(
                    master=output_frame,
                    text='Output:',
                    font=('Arial', 16, 'bold')
                )
                output_label.pack(padx=self.spacing, pady=self.spacing)

            output_section()

        # Create pole data page
        format_section()
        violation_section()

    def settings_frame(self):

        # Clears page
        self.clear_page_frame()

    def format_to_template(self):
        pass
        # input_spreadsheet = es.ExcelFile()
        # input_spreadsheet.template = input_selected


if __name__ == '__main__':
    App()
