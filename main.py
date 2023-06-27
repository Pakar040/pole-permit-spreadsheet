import excel_manager as em
import format_fulcrum as ff
from pole_manager import PoleManager


def main():
    # Read excel data and format for PoleManager
    excel_manager = em.select_jurisdiction('PSE')
    excel_manager.set_file_path('user_input/pse_ground_mold.xlsx')
    excel_manager.read_excel()
    excel_manager.format()
    excel_manager.parse_notes()

    # Extract poles and create make ready
    poles = PoleManager()
    poles.extract_poles(excel_manager.df)
    poles.get_all_violations()

    # Update make ready in spreadsheet and create output
    excel_manager.update_make_ready(poles.pole_list)
    excel_manager.reverse_parse_notes()
    excel_manager.format()
    excel_manager.create_output()


if __name__ == "__main__":
    main()
