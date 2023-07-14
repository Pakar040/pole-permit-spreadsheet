import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import os
from view.excel_spreadsheet import ExcelFile
import model.model as m


class View(ctk.CTk):
    def __init__(self):
        # Create window with settings
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title('')
        self.geometry(f"{800}x{500}")
        self.minsize(800, 500)

        # Menu and main page
        self.main = Main(master=self)
        self.menu = Menu(master=self, main=self.main)

        # Keep window open
        self.mainloop()


class Menu(ctk.CTkFrame):
    def __init__(self, master, main):
        # Create and place frame
        super().__init__(master)
        self.place(x=0, y=0, relwidth=0.1875, relheight=1.0)

        # Menu title
        self.title_label = ctk.CTkLabel(
            master=self,
            text='Make Ready Calculator',
            font=('Arial', 18, 'bold'),
        )
        self.title_label.pack(fill='x', padx=10, pady=10)

        # Update wrap length when window size changes
        self.bind('<Configure>', self.update_wraplength)

        # Create and place buttons
        button_font = ('Arial', 16)
        self.page_buttons = [
            ctk.CTkButton(master=self, text='Settings', font=button_font, command=main.settings_page),
            ctk.CTkButton(master=self, text='Format', font=button_font, command=main.format_page),
            ctk.CTkButton(master=self, text='Make Ready', font=button_font, command=main.make_ready_page)
        ]
        for button in self.page_buttons:
            button.pack(padx=10, pady=5, fill='x')

    def update_wraplength(self, _event):
        """Updates wraplength when window is resized"""
        new_wraplength = self.winfo_width() * 0.9
        self.title_label.configure(wraplength=new_wraplength)


class Main(ctk.CTkFrame):
    def __init__(self, master):
        # Create and place frame
        super().__init__(master, fg_color='transparent')
        self.place(relx=0.1875, y=0, relwidth=0.8125, relheight=1.0)

    def settings_page(self):
        """Loads the setting page into the main frame"""
        # Clear widgets
        self._clear_main()

    def format_page(self):
        """Loads the format page into the main frame"""
        # Clear widgets
        self._clear_main()

        # Create page
        FormatPage(master=self)

    def make_ready_page(self):
        """Loads the make ready page into the main frame"""
        # Clear widgets
        self._clear_main()

        # Create page
        MakeReadyPage(master=self)

    def _clear_main(self):
        """Clears main frame of any widgets"""
        for widget in self.winfo_children():
            widget.destroy()


class FormatPage(ctk.CTkFrame):
    def __init__(self, master):
        # Page variables
        self.input_file_path = None
        self.output_folder_directory = None

        # Create page
        super().__init__(master=master)
        self.pack(padx=10, pady=10, expand=True, fill='both')
        self.grid_columnconfigure(index=0, pad=10, weight=1)
        self.grid_columnconfigure(index=1, pad=10, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        # Create labels and frames
        label_font = ('Arial', 18, 'bold')
        self.input_label = ctk.CTkLabel(master=self, text='Input', font=label_font)
        self.output_label = ctk.CTkLabel(master=self, text='Output', font=label_font)
        self.input_frame = ctk.CTkFrame(master=self)
        self.output_frame = ctk.CTkFrame(master=self)
        self.format_button = ctk.CTkButton(
            master=self,
            text='Format to Template',
            font=label_font,
            command=self.format_to_template,
        )

        # Place labels and frames
        self.input_label.grid(row=0, column=0, sticky='nsew', pady=(10, 5))
        self.output_label.grid(row=0, column=1, sticky='nsew', pady=(10, 5))
        self.input_frame.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=5)
        self.output_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 10), pady=5)
        self.format_button.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=(5, 10))

        # Create widgets
        button_font = ('Arial', 14)
        button_label_font = ('Arial', 14, 'italic')

        # Input frame widgets
        self.input_template_option_menu = ctk.CTkOptionMenu(
            master=self.input_frame,
            values=['Cable Comm App'],
            font=button_font,
        )
        self.input_template_label = ctk.CTkLabel(
            master=self.input_frame,
            text='Select template',
            font=button_label_font,
            text_color='grey',
        )
        self.input_file_button = ctk.CTkButton(
            master=self.input_frame,
            text='Select Excel File',
            font=button_font,
            command=self.open_file_dialog,
        )
        self.input_file_label = ctk.CTkLabel(
            master=self.input_frame,
            text='No file selected',
            font=button_label_font,
            text_color='grey',
        )

        # Output frame widgets
        self.output_template_option_menu = ctk.CTkOptionMenu(
            master=self.output_frame,
            values=['PSE'],
            font=button_font,
        )
        self.output_template_label = ctk.CTkLabel(
            master=self.output_frame,
            text='Select template',
            font=button_label_font,
            text_color='grey',
        )
        self.output_folder_button = ctk.CTkButton(
            master=self.output_frame,
            text='Select Folder',
            font=button_font,
            command=self.open_folder_dialog,
        )
        self.output_folder_label = ctk.CTkLabel(
            master=self.output_frame,
            text='No folder selected',
            font=button_label_font,
            text_color='grey',
        )
        self.output_file_name_entry = ctk.CTkEntry(
            master=self.output_frame,
            placeholder_text='Enter a file name',
        )

        # Place input frame widgets
        self.input_frame.grid_columnconfigure(index=0, weight=1)
        self.input_template_option_menu.grid(row=0, column=0, sticky='nsew', padx=5, pady=(5, 2.5))
        self.input_template_label.grid(row=0, column=1, sticky='w', padx=5, pady=(5, 2.5))
        self.input_file_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=(2.5, 5))
        self.input_file_label.grid(row=1, column=1, sticky='w', padx=5, pady=(2.5, 5))

        # Place output frame widgets
        self.output_frame.grid_columnconfigure(index=0, weight=1)
        self.output_template_option_menu.grid(row=0, column=0, sticky='nsew', padx=5, pady=(5, 2.5))
        self.output_template_label.grid(row=0, column=1, sticky='w', padx=5, pady=(5, 2.5))
        self.output_folder_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=2.5)
        self.output_folder_label.grid(row=1, column=1, sticky='w', padx=5, pady=2.5)
        self.output_file_name_entry.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=2.5)

    def open_file_dialog(self):
        """Allows button to select file from file explorer"""
        filepath = filedialog.askopenfilename()
        file_is_selected = filepath != ""
        if file_is_selected:
            filename = os.path.basename(filepath)
            self.input_file_path = filepath  # <- Page variable
            self.input_file_label.configure(text=filename)

    def open_folder_dialog(self):
        """Allows button to select folder from file explorer"""
        folder_path = filedialog.askdirectory()
        file_is_selected = folder_path != ""
        if file_is_selected:
            folder_name = os.path.basename(folder_path)
            self.output_folder_directory = folder_path  # <- Page variable
            self.output_folder_label.configure(text=folder_name)

    def format_to_template(self):
        """Creates formatted excel file"""
        # Input object
        input_excel = ExcelFile()
        # Set file path
        input_excel.path = self.input_file_path
        # Set template
        input_excel.template = self.input_template_option_menu.get()

        # Output object
        output_excel = ExcelFile()
        # Set name
        output_file_name_is_blank = self.output_file_name_entry.get() == ""
        if output_file_name_is_blank:
            output_excel.name = 'output.xlsx'
        else:
            output_excel.name = self.output_file_name_entry.get() + '.xlsx'
        # Set directory
        output_excel.directory = self.output_folder_directory
        # Set template
        output_excel.template = self.output_template_option_menu.get()

        # Execute
        m.format_to_template(input_excel, output_excel)

        # Pop up message
        CTkMessagebox(title='', message="Spreadsheet successfully formatted", icon="check", option_1="Ok")


class MakeReadyPage(ctk.CTkFrame):
    def __init__(self, master):
        # Page variables
        self.input_file_path = None

        # Create page
        super().__init__(master=master)
        self.pack(padx=10, pady=10, expand=True, fill='both')
        self.grid_columnconfigure(index=0, pad=10, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        # Create frames
        self.input_frame = ctk.CTkFrame(master=self)
        self.display_frame = ctk.CTkFrame(master=self)

        # Place labels and frames
        self.input_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10, 5))
        self.display_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(5, 10))

        # Create widgets
        button_font = ('Arial', 14)
        button_label_font = ('Arial', 14, 'italic')

        # Input frame widgets
        self.input_template_option_menu = ctk.CTkOptionMenu(
            master=self.input_frame,
            values=['PSE'],
            font=button_font,
        )
        self.input_template_label = ctk.CTkLabel(
            master=self.input_frame,
            text='Select template',
            font=button_label_font,
            text_color='grey',
        )
        self.input_file_button = ctk.CTkButton(
            master=self.input_frame,
            text='Select Excel File',
            font=button_font,
            command=self.open_file_dialog,
        )
        self.input_file_label = ctk.CTkLabel(
            master=self.input_frame,
            text='No file selected',
            font=button_label_font,
            text_color='grey',
        )
        self.include_make_ready_check_box = ctk.CTkCheckBox(
            master=self.input_frame,
            text='Include Make Ready',
            font=button_font,
        )
        self.find_violations_button = ctk.CTkButton(
            master=self.input_frame,
            text='Find Violations',
            font=('Arial', 18, 'bold'),
            command=self.find_violations,
        )

        # Place input frame widgets
        self.input_frame.grid_columnconfigure(index=2, weight=1)
        self.input_template_option_menu.grid(row=0, column=0, sticky='nsew', padx=5, pady=(5, 2.5))
        self.input_template_label.grid(row=0, column=1, sticky='w', padx=5, pady=(5, 2.5))
        self.input_file_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=(2.5, 5))
        self.input_file_label.grid(row=1, column=1, sticky='w', padx=5, pady=(2.5, 5))
        self.include_make_ready_check_box.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=(2.5, 5))
        self.find_violations_button.grid(row=0, column=2, rowspan=3, sticky='nsew', padx=5, pady=5)

    def open_file_dialog(self):
        """Allows button to select file from file explorer"""
        filepath = filedialog.askopenfilename()
        file_is_selected = filepath != ""
        if file_is_selected:
            filename = os.path.basename(filepath)
            self.input_file_path = filepath  # <- Page variable
            self.input_file_label.configure(text=filename)

    def find_violations(self):
        """Gets violations and displays them"""
        # Get user inputs
        input_excel_file = ExcelFile()
        input_excel_file.template = self.input_template_option_menu.get()
        input_excel_file.path = self.input_file_path
        make_ready_is_included = self.include_make_ready_check_box.get() == 1

        # Get list
        pole_list = m.get_pole_list_with_violations(input_excel_file, make_ready_is_included)

        # Clear Display
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Display violations
        violations_frame = ctk.CTkScrollableFrame(master=self.display_frame, fg_color='transparent')
        violations_frame.pack(expand=True, fill='both')
        violations_frame.grid_columnconfigure(index=1, weight=1)

        for index, pole in enumerate(pole_list):
            # Create frames
            sequence_number_frame = ctk.CTkFrame(master=violations_frame)
            make_ready_frame = ctk.CTkFrame(master=violations_frame)
            sequence_number_frame.grid(row=index, column=0, sticky='nsew', padx=2.5, pady=2.5)
            make_ready_frame.grid(row=index, column=1, sticky='nsew', padx=2.5, pady=2.5)

            # Add sequence numbers to frames
            data_font = ('Arial', 14)
            sequence_number = ctk.CTkLabel(master=sequence_number_frame, text=pole.sequence_number, font=data_font)
            make_ready = ctk.CTkLabel(master=make_ready_frame, text=pole.make_ready, font=data_font)
            sequence_number.pack(padx=10, pady=10, expand=True, fill='both')
            make_ready.pack(padx=10, pady=10, expand=True, fill='both')


# Test code
if __name__ == '__main__':
    View()
