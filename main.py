import excel_manager as em
import format_fulcrum as ff
from pole_manager import PoleManager


def main():
    # Create spreadsheet from downloaded data
    fulcrum_excel = ff.CableComAppManager('user_input/cablecom_poles.xlsx')
    fulcrum_excel.read_excel()
    fulcrum_excel.select_jurisdiction('PSE')
    fulcrum_excel.transfer_to_spreadsheet()
    fulcrum_excel.create_output()

    # Do make ready calculations
    fulcrum_excel.excel_manager.set_file_path('output/output.xlsx')
    fulcrum_excel.excel_manager.read_excel()
    fulcrum_excel.excel_manager.parse_notes()
    fulcrum_excel.excel_manager.format()
    poles = PoleManager()
    poles.extract_poles(fulcrum_excel.excel_manager.df)
    poles.get_all_violations()
    fulcrum_excel.excel_manager.update_make_ready(poles.pole_list)
    fulcrum_excel.excel_manager.format()
    fulcrum_excel.excel_manager.reverse_parse_notes()
    fulcrum_excel.excel_manager.create_output()


if __name__ == "__main__":
    main()
