import excel_manager as em
from pole_manager import PoleManager


def main():
    excel = em.PSEManager('user_input/JB0001175447-1_Appendix A Field Survey.xlsx')
    excel.read_excel()
    excel.parse_notes()
    excel.format()
    print(excel)
    poles = PoleManager()
    poles.extract_poles(excel.df)
    poles.get_all_violations()
    print(poles)
    excel.update_make_ready(poles.pole_list)
    excel.reverse_parse_notes()
    excel.format()
    print(excel)
    excel.create_output()


if __name__ == "__main__":
    main()
