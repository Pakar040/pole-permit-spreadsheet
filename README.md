# pole-permit-spreadsheet
 Tool used for filling out appedix on pole permit jobs

**Example (CableComApp xlsx to PSE template):**

    `# Create spreadsheet from downloaded data
    excel_manager = em.select_jurisdiction('PSE')
    fulcrum_excel = ff.CableComAppManager('user_input/cablecom_poles.xlsx')
    fulcrum_excel.set_excel_manager(excel_manager)
    fulcrum_excel.read_excel()
    
    # Get make ready violations from poles
    poles = PoleManager()
    poles.extract_poles(fulcrum_excel.make_ready_df)
    poles.get_all_violations()
    
    # Add violations to excel and formate template
    fulcrum_excel.update_make_ready(poles.pole_list)
    fulcrum_excel.format_to_template()

    # Once formatted for template
    excel_manager.read_data_frame(fulcrum_excel.df)
    excel_manager.create_output()`

**Example (PSE template alone):**

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
