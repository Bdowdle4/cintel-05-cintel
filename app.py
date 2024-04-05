# Imports at the top - PyShiny EXPRESS VERSION
from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats

# Import icons as you like
# https://fontawesome.com/v4/cheatsheet/
from faicons import icon_svg

# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)

UPDATE_INTERVAL_SECS: int = 30

# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings

DEQUE_SIZE: int = 6
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# Initialize a REACTIVE CALC that all display components can call to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS to trigger updates.
# It returns a tuple with everything needed to display the data.


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(-10, 60), 1)
    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    new_dictionary_entry = {"temp": temp, "timestamp": timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry


# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI
ui.page_opts(
    title="Constantly Varied Midwest Weather", window_title="Dowdle P5", fillable=True
)

# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently
with ui.sidebar(open="open"):
    ui.h2(
        "Which seasons will we see today?",
        style="font-weight:bold",
        class_="text-center",
    )
    ui.p(
        "Winter frost in the morning, Summer sun before lunch, Spring showers in the afternoon, and crispy Fall breeze into the evening.",
        class_="text-center", style="background-color: lightblue; color: black",
    )
    ui.hr()
    ui.h6("Important Links:",
         style="text-decoration:underline")
    ui.a(
        "GitHub Repo",
        href="https://github.com/Bdowdle4/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "PyShiny Playground",
        href="https://shinylive.io/py/app/#code=NobwRAdghgtgpmAXGKAHVA6VBPMAaMAYwHsIAXOcpMAYgAIBJGVYgJzIGc6oy6yALOH2Ko6AWjoAFbAGV+ASwjY6AUQAakgEoqZMugDUVmmQwDyAOQA6EAGatiMOhwVK685m16s4UQmXkAbnB4dN4QACZwrNZ2Dk4u2BhwAB6o3hxc7izsdACu8tZZnqFQEQ4x9o7hPHD+8G4eOdUUdXAVcSQANp1wfvKkmY28kQCOuW0QRTmopdVcUFyo4YVDdKidxGSdiSlpcBnci8ntjs6K2ADu8uEA5rWD2V6UkawA+uub2ydOhPI4DY8nGQeBxrNZ6ExAfISBB5lxsMRcnROvIANYTej8MhkVAcRAAenxNlIwIu+wccAwJBg+ICABZ8YRBCDBLV8d8bFBoQMAcVuRBXhwAjcwRB6AAxeSsDhkEIcWrcOgwmWlXgAVUkABEAIIAFRUjHM+s0+m1ABk6MTWNxusjAkJmlBwXQAMIDYHkebePIcXJQbrKSI2RRwcJuCB5dBRQgLIQ9bFRUFiuhq+WKsjYVBCFy8MjEOgwKDoty8Qg9KDWgQ8EsAcnmEcUFDu1oAFIhw2QAJSijU6-WvBhGoyms2vGQqF0yduNugAXjoAGYAAyiiGTfz++QALyEUDo2m1Lt1DEMBnNaoNVwEiupMFIdEdQNYuT8uW8zt1glCPj6QToAX9cY3C4XJ5TDPMgTYIQVQoOgW0UK1C38Uhu2TVNQzoAAjZR-U6Pgv3CeQOHWKBlGpFgIEoTh8OrZxiAufCiLtP9HQwD8FC4bxfH8P8AM6ICmL3C5WDQLNrQrREIkVTUVAARQvOhiBsb8oEIiAbiTawZPklQxwYAAtFRp3IOc6AARhXCAuN-OBXj48ZXmE0SolM6yeMpey4BbUZxhbQtkh6CBZ20i89MMztUOdBh13kTcd0VA8jxPA0XXNF0aN4XCHyIkiyIcCiqK4GMIxjW0ILuXMv06GoZQfHg91mbLiOq5R5DINjk0-IRSsIXJquQhtMggPjrhqMM4CCVhlF7PVdMHY0RzHCc9AgshWHkG5m0jZp9g6iEnjIN9YXTXJ1iEK9+DoCaomwARFBuOhKNDDCIMI5rSPwh16o66wAAE3PtKl-UIFtUKDFSbNeHqoYcTCQ3CUHEGsOgUboNcRp2xiiuBvqeH6CNrqmlMtVmgchxNc0lsnYQ+HWzaXNOnak1RiH3IwRQMZqV5+qiFsZv7ebh0p8dJ0iiNUfoTV6roO5KJEgbkWIG5oWR1GKGYVzJIRkSyhgDBckmRCWzEMyAA4QhNgA2TsQjM1CWdaFUNfnHbWgwCB6NBjAZVYGxWhbSwwAAUgATTEIOYHDsMg4ACUQIOAFl45kQP7dRyiLleQi+lICtsFeKiifnEBA-V1BA8QMuQlL9x9mBZgK8d+vUAAX1FFn6Aqz6HzgMZdyk5ypIEIQM6u8gptVlGAaCOzANspyo1YDAKq9weEYzrPoQGvOC-H7AxY7ugAHEFT3DhoFxfhNkU5Th6VN8wmGXugKtbhXBsN9h+tNJiEIfYOHupPHufdBQXzorwec09bKeUciJRey9aig3bhLOg4o2B0E1DlFq7Y3TDSiE-PuNMpbAnFCJeor83q5SAeEZS84lgYGIVAUhsAvI+VsufNA4CD4oLQdaTB71sDthPpVOMNVhhb3xnnMea1sBAJ5jKTeOdoBTV3jI0yG9s7bxUYXWREAgH0E0LUI6J0zp0AuldSat0XAPTJI9OAoZ9GqEsXwWuZjupZTulwD+EAlEhDJDWW0XcPGCDTJ5ZmqNvCHVYBGNhoDOFX1lA+GwIR5FkEUVo-OOjVyumCUIfIWAoB3FeCITgoNLQGyUc6GQCp-BbCEBBM+a17rhjoGMTY+wMpmPkLaZyFZuAiOEOXZM1TeDBm6FATCPQaa6mfPU-MoF6lfguFfKZMw7hdPCNeV+d81QMGsPktZtkSkcBbLUnos5A64JVOQbYBgKzyAwgna4ZJaoAHUfBf0DiEMZ1VJlwFnDM8YYt6DmHad3cxME4DwBMhBQgXFYJ3wAZETCfTiTdHohhbCN5iAbD0cmFQli7rqRaYi64cAUXWiYooSI5AMLKiIhQG5ujzH5KReSisLYRCUAuWALleiwCdiRnilm+T+AACYA5gFeQoJkTgfAcB5FcW0tj5RzOqNgAA-F8pU1UMivB5RQZIZAxB-1pdEAVQCDkB3FizFGgdXmNhcrEWqihu53mifdEIMhcgwHgNaX0EZMJwCtHGCp-AvVpGaXRMk0oSVfigH7KIHtSAhEanCnKyhxRZUwt4OA8VGz5jvtdSY6k2L4CASzMsCwOD6tLikY1pqKDmrwEAtOKNRWsCQTavI8gMD8EtpKs0ihUR4lTpa3tUBrW2tRoHI+bUY65EwvuOALAvkVtRvwbwNgeVYhxHiQkysBCLqpA4fEAAhcI9Fwg9AZL8WlnQxBLgAKwmsdZ0Nd3aHYVgqjy14kzSiog-SzNtPaMCTsDtIOQ5xtWbuDTu7EuICT4jOEoLAxAAHtRIPiHA7J8B8G-bUX9-6ICAYtd2-J4HP0zrAJBhIqhUjpFBOWqjKNYPbsDvwXdiHCQocSCwDDJ78STKVth9DnBkMJDELsRjuGW0sfw6wH9gc-3VRI0B1GwLGARig64FQDH-4hEJlY5pHteCutJcivpVKIx30LK6mYlF314pZb2lqiI0ldB9bCRGQCXMYBgZhYgyQp3TviPRGM8pZz8kFMKSVAbU5ydC59eAPLMI3DEDcEShEqJiEmeMMQqA3xnXUyjQVyDp2XIflROguooViR4G+NoYByu2v+s8KIGBDVkHXSjcGlCWqvDLj5+TLNA5jbAMI7uqSVJqQeo1SJxi9xlyiA170PtAHNc2z121sSOGX02CEGhKSxHpMkdoverkfzuShsDGGMA4aUQRiBpLC3omWkDiAVJp3c7nZkcAGsZcawAF0W6ujG8K0LgcLgVj9TRCMoE-TvuaxDlrfmYysARh-bogo4X2KCoCuAZX5P5PR+EV4zIXiSpdFVkyxD+5hl1LXMdEPp1tYiB1rr22+tYNIoN2uw2kuja2xNmpVUxEzeafNoxb2lu1ydqIdb6lxvg8F6jXbYCEmHeSciE7mizuZIu5Aq79obudEIHdh7oYu2q6ntLiMNgPtfb1z9g3f2Ady+bsDtuyPVxo4rJjvqnQce5vx7MkIMBFDk7gBtLEPK6RLiDqnIVfuMctix0HjguPuUE6JyK3tpOo+qV5oHBOYnl2NuXape6THuEozZy8DAjpXh2BYdQ4NTVcpZxsALyHwvJt32m1xWbb8wyvYjHuR0Lf6jmN6qwR+Ev1JMeV-J9X8SDtJOOxQBRzvlGu6LqzE30NqSW6e9t+h8o0klPxi2Gs-XSIYCuJs-gNYQigsop2JL9B0IFigMkdwPqNkBBtsx9vx2cl5GEj51oEYN9H8BAeULIE9mdrAU8nshU88gYMdC9KdLl+AKxeBzFqc59qsZlngkDu168oh3gNgthdEWZucBEqDNge9p0JRahZVYhHA74oElRgZykfEBoudn52ENd18jsdct80kd8d4dFLtuJD9btj94Yu1tt6AVBYRGtu5GFmF6gmJTMrpmAMwsJg0oI1hqD-Ald5N5BlI9CaEkgDDBFttD5cFJoBl3d4B5cawlQcUvMaZXZXFX4g0Exv4zDAERs1cbBgAa53Dm5A4gdTJ6E8ws4ah-YaFIiwAm5YBy4wAgda9Bd6AXR4VoIYwgjTDr5X4h9q9HCUEZgDhzMCJtc75oB6glJu5kgvD+IYAIAQhGiWEb5u48oOiuiR8CwoJtsqiUZgwHo6FkhvZiim1vJklxi6BkgDUPdMiStBdsADU6sNikszl-lA5atmAVsokhBDEq9F8ulrxDFMt-58Y6Ah1KJdjQtfk4BOgOBZwS50idikA6BDi6sTiNCWwAAGl0bsPDKIuudY34w4pnMAFuRLG3LoNgTeTPSJdhIQnxf5NIvLJrOI57SHMIlGegR4nwa0bwW4jIe4iQWxJ6cCfMIJO0WqFo4eJYtcSILMdnEyACdaCZKZNosJOCVoD-RqVkoktGDBFddrbk+5PkoQZQQU05OrAklgz6IYtqOsNYSJQw+VZQUCKNX4HAb2YETgDAFEKyOASkk5XIz-VBdBNo+MTU2WE43cOVPuLEvox1ZsLxSoOgJcGmQKBYlU21eUd0v+VyUoO4FsQMmhCKJY5IWed40yFEGUFsUM8YLE4MlmfOPiLgF2CIutBubIlrJLDgDYLMEIR1VgP+VARJN4TyEIVARM8YOUMgMnKIa0ecGCDgM0xQCkxjFsBM3MkIHM-0DgLM8I-7INBRYMNJc0uAYHUyYAMsrlOgAAKmWLoAAGoOxowV1Rl7SWkhyxygcSzQt6BtRwhwIvx+y7j7x5yaY75JjGsljJiwMrycceB5iVjUjIT5dYiRzZxUiaxpy0lZzuYQxgdw9iBIhZwAkQwOAX9HoWE4KbjGN7jSSawbTzyUwlgagdcERchMouA6SXp8xeoZQHBtwhAP52BBBohxS3zGYuY3MiLBzf8iI+c6keVGd4AvlsAOKa19ieKAT5YgTQTwTsLbcol7cNptt4S8BwAmiEBkBvAxgpQoVCpOsjV8AiASQqJqAHM5hrAPgaDrB4SgcgA",
        target="_blank",
    )
    ui.a(
        "The Weather Channel",
        href="https://weather.com/weather/today/l/d0a574438dc01abf00c019355ae81203b3ec557999155ad59a0af07157d97a798c267e721a50ad96c6d10ebdbefed30f",
        target="_blank",
    )

# In Shiny Express, everything not in the sidebar is in the main panel
with ui.layout_columns(row_heights=["auto"], fill=True):
    with ui.value_box(
        showcase=icon_svg("tornado"),
        theme="bg-gradient-red-purple",
        style="color: black;",
    ):
        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} F"

        "Is this normal?"

    with ui.card(full_screen=True, style="background-color: lightcyan"):
        ui.card_header(
            "Current Date and Time 📅",
            style="background-color: green; color: white;",
        )

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']} CST"


# with ui.card(full_screen=True, min_height="60%"):
with ui.navset_card_tab(id="tab1"):
    with ui.nav_panel("Table"):
        with ui.card(
            full_screen=True, style="background-color: lightcyan;", height="300px"
        ):
            ui.card_header(
                "Most Recent Readings ⏰", style="background-color: green; color: white;"
            )

            @render.data_frame
            def display_df():
                """Get the latest reading and return a dataframe with current readings"""
                deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
                pd.set_option("display.width", None)  # Use maximum width
                return render.DataGrid(df, width="100%")

    with ui.nav_panel("Graph"):
        with ui.card(
            full_screen=True, style="background-color: lightcyan;", height="600px"
        ):
            ui.card_header(
                "Current Trend 🌡️", style="background-color: green; color: white;"
            )

            @render_plotly
            def display_plot():
                # Fetch from the reactive calc function
                deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

                # Ensure the DataFrame is not empty before plotting
                if not df.empty:
                    # Convert the 'timestamp' column to datetime for better plotting
                    df["timestamp"] = pd.to_datetime(df["timestamp"])

                    # Create scatter plot for readings
                    # pass in the df, the name of the x column, the name of the y column, and more

                    fig = px.scatter(
                        df,
                        x="timestamp",
                        y="temp",
                        title="Temperature Readings with Regression Line",
                        labels={"temp": "Temperature (°F)", "timestamp": "Time"},
                        color_discrete_sequence=["blue"],
                    )

                    # Linear regression - we need to get a list of the
                    # Independent variable x values (time) and the
                    # Dependent variable y values (temp)
                    # then, it's pretty easy using scipy.stats.linregress()

                    # For x let's generate a sequence of integers from 0 to len(df)
                    sequence = range(len(df))
                    x_vals = list(sequence)
                    y_vals = df["temp"]

                    slope, intercept, r_value, p_value, std_err = stats.linregress(
                        x_vals, y_vals
                    )
                    df["best_fit_line"] = [slope * x + intercept for x in x_vals]

                    # Add the regression line to the figure
                    fig.add_scatter(
                        x=df["timestamp"],
                        y=df["best_fit_line"],
                        mode="lines",
                        name="Regression Line",
                    )

                    # Update layout as needed to customize further
                    fig.update_layout(
                        xaxis_title="Time", yaxis_title="Temperature (°F)"
                    )

                    return fig
