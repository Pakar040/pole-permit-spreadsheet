from typing import List
from view.excel_spreadsheet import ExcelFile
from model.pole_manager import PoleManager
from model.pole import Pole
import model.excel_manager as em
import model.format_fulcrum as ff


def format_to_template(input_excel: ExcelFile, output_excel: ExcelFile) -> None:
    """Creates a formatted Excel output using input Excel"""
    # Create spreadsheet from downloaded data
    excel_manager = em.select_template(template=output_excel.template)
    fulcrum_excel = ff.CableComAppManager(file_path=input_excel.path)
    fulcrum_excel.set_excel_manager(excel_manager)
    fulcrum_excel.read_excel()
    fulcrum_excel.format_to_template()

    # Once formatted to template
    excel_manager.read_data_frame(fulcrum_excel.df)
    excel_manager.create_output(file_path=output_excel.path)


def get_pole_list_with_violations(input_excel: ExcelFile, make_ready_is_included: bool) -> List[Pole]:
    """Returns a list of pole objects with make ready and sequence numbers"""
    # Read excel data and format for PoleManager
    excel_manager = em.select_template(input_excel.template)
    excel_manager.set_file_path(input_excel.path)
    excel_manager.read_excel()
    excel_manager.format()
    excel_manager.parse_column('additional_measurements')
    excel_manager.parse_column('make_ready')

    # Extract poles and create make ready
    poles = PoleManager()
    poles.extract_poles(excel_manager.df)
    if make_ready_is_included:
        poles.set_to_proposed()
    poles.get_all_violations()

    # Return pole list
    return poles.pole_list
