import excel_manager as em
import format_fulcrum as ff
from pole_manager import PoleManager


def main():
    # Create spreadsheet from downloaded data
    excel_manager = em.select_jurisdiction('PSE')
    fulcrum_excel = ff.CableComAppManager('user_input/cablecom_poles.xlsx')
    fulcrum_excel.set_excel_manager(excel_manager)
    fulcrum_excel.read_excel()
    fulcrum_excel.format_to_template()

    # Once formatted for template
    excel_manager.read_data_frame(fulcrum_excel.df)
    excel_manager.format()
    excel_manager.parse_notes()
    poles = PoleManager()
    poles.extract_poles(excel_manager.df)
    poles.get_all_violations()
    excel_manager.update_make_ready(poles.pole_list)
    excel_manager.reverse_parse_notes()
    excel_manager.format()
    excel_manager.create_output()


if __name__ == "__main__":
    main()
