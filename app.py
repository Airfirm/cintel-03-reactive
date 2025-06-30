import palmerpenguins
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from shiny.express import input, render, ui
from shiny import render
from shinywidgets import render_plotly
from shiny import reactive

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguin Exploratory Data Analysis - Femi", fillable=True)

# Sidebar
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )
    ui.input_numeric("plotly_bin_count", "Plotly Histogram Bin Count", 20)
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 5, 100, 20)
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter by Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True
    )
    ui.hr()
    ui.a("GitHub Repo URL", href="https://github.com/Airfirm/cintel-02-data", target="_blank")

# Reactive calculations and effects
    @reactive.calc
    def filtered_data():
        df = penguins_df.dropna()
        df = df[df["species"].isin(input.selected_species_list())]
        return df
        
# Main layout - Data Table and Data Grid
with ui.layout_columns():
    @render.data_frame
    def data_table():
        return render.DataTable(filtered_data())

    @render.data_frame
    def data_grid():
        return render.DataGrid(filtered_data())

# Main layout - Histograms and Scatterplot
with ui.layout_columns():
    @render_plotly
    def plot1():
        return px.histogram(
            filtered_data(),
            x=input.selected_attribute(),
            color="species",
            nbins=input.plotly_bin_count(),
            title=f"Histogram of {input.selected_attribute()} by Species",
            labels={input.selected_attribute(): input.selected_attribute().replace('_', ' ').title()}
    )

    @render.plot(alt="Seaborn Histogram")
    def seaborn_hist():
        data = filtered_data()
        bins = input.seaborn_bin_count()
        attr = input.selected_attribute()

        for species in data["species"].unique():
            species_data = data[data["species"] == species]
            plt.hist(
                species_data[attr],
                bins=bins,
                alpha=0.5,
                label=species,
                density=True
    )
        plt.title(f"Seaborn Histogram of {attr.replace('_', ' ').title()} by Species")
        plt.xlabel(attr.replace('_', ' ').title())
        plt.ylabel("Density")
        plt.legend()
        return plt.gcf()

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            filtered_data(),
            x="bill_length_mm",
            y=input.selected_attribute(),  # dynamic Y-axis
            color="species",
            title=f"Scatterplot of Bill Length vs {input.selected_attribute().replace('_', ' ').title()}",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                input.selected_attribute(): input.selected_attribute().replace('_', ' ').title()
        },
            size_max=10
        )
