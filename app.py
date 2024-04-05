with ui.layout_columns(col_widths={"sm": (8, 4)}, row_heights=2):
    with ui.value_box(
        showcase=icon_svg("tornado"),
        theme="bg-gradient-red-green",
        style="color: black;",
    ):
        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} F"

        "Is this normal?"

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time 📅",
        style="background-color: green; color: lightblue;",
    )

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

