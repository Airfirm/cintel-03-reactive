import palmerpenguins
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly

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
        return penguins_df
        
# Main layout - Data Table and Data Grid
with ui.layout_columns():
    @render.data_frame
    def data_table():
        return render.DataTable(penguins_df)

    @render.data_frame
    def data_grid():
        return render.DataGrid(penguins_df)

# Main layout - Histograms and Scatterplot
with ui.layout_columns():
    @render_plotly
    def plot1():
        return px.histogram(
            penguins_df.dropna(subset=["species", "body_mass_g"]),
            x="body_mass_g",
            color="species",  # different colors per species
            nbins=input.plotly_bin_count(),  # uses sidebar input
            title="Plotly Histogram of Penguin Body Mass by Species",
            labels={"body_mass_g": "Body Mass (g)"}
    )

    @render.plot(alt="Seaborn Histogram by Species")
    def seaborn_hist():
        data = penguins_df.dropna(subset=["body_mass_g", "species"])
        bins = input.seaborn_bin_count()
    
        # Plot histogram for each species
        for species_name in data["species"].unique():
            species_data = data[data["species"] == species_name]
            plt.hist(
                species_data["body_mass_g"],
                bins=bins,
                alpha=0.5,
                label=species_name,
                density=True
    )
    
        plt.title("Seaborn Histogram of Body Mass by Species")
        plt.xlabel("Body Mass (g)")
        plt.ylabel("Density")
        plt.legend(title="Species")
        return plt.gcf()


with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            penguins_df,
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot (Plotly Express)",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)"
            },
            size_max=8
    )
