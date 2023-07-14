import model.excel_manager as em
from model.pole_manager import PoleManager
import logging
import os
from view.gui_2 import View


def main():
    # Remove log file if it is there
    log_file = 'model/logging/log.log'
    if os.path.exists(log_file):
        os.remove(log_file)

    # Log settings
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(levelname)s - %(message)s',
    )

    View()

    # # Read excel data and format for PoleManager
    # excel_manager = em.select_template('PSE')
    # excel_manager.set_file_path('model/user_input/pole_data_make_ready.xlsx')
    # excel_manager.read_excel()
    # excel_manager.format()
    # excel_manager.parse_column('additional_measurements')
    # excel_manager.parse_column('make_ready')
    #
    # # Extract poles and create make ready
    # poles = PoleManager()
    # poles.extract_poles(excel_manager.df)
    # poles.set_to_proposed()
    # poles.get_all_violations()
    #
    # # Update make ready in spreadsheet and create output
    # excel_manager.reverse_parse_column('additional_measurements')
    # excel_manager.reverse_parse_column('make_ready')
    # excel_manager.update_make_ready(poles.pole_list)
    # excel_manager.format()
    # excel_manager.create_output()


if __name__ == "__main__":
    main()
