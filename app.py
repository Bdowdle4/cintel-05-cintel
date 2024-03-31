
# These are all of the inputs you need to make your outputs work
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shinyswatch import theme

# This package provides the Palmer Penguins dataset but you have to load it before you can use it
from palmerpenguins import (
    load_penguins,
)
from shiny import reactive, render, req
import seaborn as sns
import pandas as pd

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = load_penguins()

# This creates a title for your visual pane
ui.page_opts(title="Brittany's Data About Spectacular Penguins", fillable=False)

#This will change the look of your UI, there are so many to try!
theme.yeti()

# This adds a Shiny UI sidebar for user interaction. We will be adding a dropdown, numeric, and slider option
with ui.sidebar(open="open"):
    # This will add a 2nd level header to the sidebar
    ui.h2("Sidebar")
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

    ui.input_selectize(
        "selected_attribute",
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    ui.input_slider(
        "seaborn_bin_count",
        "Seaborn Bin Count",
        1,
        100,
        40,
    )
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 40)
    ui.input_checkbox_group(
        "selected_island_list",
        "Select Island",
        penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=True,
    )

    # This will create a line to visually separate the widgets above and below it in the sidebar
    ui.hr()
    # This will add in a hyperlink to another website
    ui.a(
        "Brittany's GitHub Link to P3",
        href="https://github.com/Bdowdle4/cintel-03-reactive",
        target="_blank",
    )

# This will organize the Data Table and Data Grid into a Tabset with pill navigation to be more visually organized
with ui.navset_pill(id="tab"):
    with ui.nav_panel("Data Table"):

        @render.data_frame
        def penguin_datatable():
            return render.DataTable(filtered_data())

    with ui.nav_panel("Data Grid"):

        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid(filtered_data())


# This will organize the Plotly Histogram, Seaborn Histogram, and the Plotly scatterplot into a card to separate from the above "Data's" amd be easier to see
with ui.navset_card_pill(id="tab1"):
    # These will connect the dropdown in the sidebar to the histogram to be interactive
    with ui.nav_panel("Plotly Histogram"):

        @render_plotly
        def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            ).update_layout(
                title="Plotly Penguins Data",
                xaxis_title="Selected Attribute",
                yaxis_title="Count",
            )
            return plotly_hist

    # These will connect the numeric in the sidebar to the histogram to be interactive
    with ui.nav_panel("Seaborn Histogram"):

        @render.plot
        def seaborn_histogram():
            seaborn_hist = sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            seaborn_hist.set_title("Seaborn Penguin Data")
            seaborn_hist.set_xlabel("Selected Attribute")
            seaborn_hist.set_ylabel("Count")

    # These will connect the checkboxes in the sidebar to the scatterplot to be interactive
    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        # Add facet_col parameter to separate scatterplots by island
        @render_plotly
        def plotly_scatterplot():
            plotly_scatter = px.scatter(
                filtered_data(),
                x="bill_depth_mm",
                y="bill_length_mm",
                color="species",
                facet_col="island",
                size_max=8,
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "bill_length_mm": "Bill Length(mm)",
                },
            )
            return plotly_scatter


# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.


@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list()))
        & (penguins_df["island"].isin(input.selected_island_list()))
    ]
