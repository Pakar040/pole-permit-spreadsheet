import excel_manager as em
from pole_manager import PoleManager


def main():
    excel = em.PSEManager('user_input/JB0001175447-1_Appendix A Field Survey.xlsx')
    excel.read_excel()
    excel.parse_notes()
    excel.format_to_standard()
    print(excel)
    poles = PoleManager()
    poles.get_poles(excel.df)


if __name__ == "__main__":
    main()
