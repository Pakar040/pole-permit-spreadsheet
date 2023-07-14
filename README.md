# pole-permit-spreadsheet
 Tool used for filling out appendix on pole permit jobs

**Example (CableComApp xlsx to PSE template):**

    `# Create spreadsheet from downloaded data
    excel_manager = em.select_template('PSE')
    fulcrum_excel = ff.CableComAppManager('user_input/cablecom_poles.xlsx')
    fulcrum_excel.set_excel_manager(excel_manager)
    fulcrum_excel.read_excel()
    
    # Get make ready violations from poles
    poles = PoleManager()
    poles.extract_poles(fulcrum_excel.make_ready_df)
    poles.get_all_violations()
    
    # Add violations to excel and format template
    fulcrum_excel.update_make_ready(poles.pole_list)
    fulcrum_excel.format_to_template()

    # Once formatted for template
    excel_manager.read_data_frame(fulcrum_excel.df)
    excel_manager.create_output(file_path)`

**Example (PSE template alone):**

    # Read excel data and format for PoleManager
    excel_manager = em.select_template('PSE')
    excel_manager.set_file_path('user_input/pse_ground_mold.xlsx')
    excel_manager.read_excel()
    excel_manager.format()
    excel_manager.parse_column('additional_measurements')

    # Extract poles and create make ready
    poles = PoleManager()
    poles.extract_poles(excel_manager.df)
    poles.get_all_violations()

    # Update make ready in spreadsheet and create output
    excel_manager.update_make_ready(poles.pole_list)
    excel_manager.parse_column('additional_measurements')
    excel_manager.format()
    excel_manager.create_output(file_path)

**Example for using proposed values for make ready:**
    
    # Make sure to parse make ready column aswell
    excel_manager.parse_column('make_ready')

    # Extract poles and create make ready
    poles = PoleManager()
    poles.extract_poles(excel_manager.df)
    poles.set_to_proposed()  # <-- This line is added
    poles.get_all_violations()

    # Make sure to reverse parse make ready column aswell
    excel_manager.reverse_parse_column('make_ready')

* Note that finding violations from proposed  is only possible from the template
* Remember to parse the make ready column for the PoleManager class
