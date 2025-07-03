# cintel-03-reactive
# Reactive Calculations and Effects



--------------------------------------------------------
Reactive calculations and effects
--------------------------------------------------------

Add a reactive calculation to filter the data
By decorating the function with @reactive, we can use the function to filter the data
The function will be called whenever an input functions used to generate that output changes.
Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    isSpeciesMatch = penguins_df["species"].isin(input.selected_species_list())
    return penguins_df[isSpeciesMatch]

Additional Python Notes
------------------------

Capitalization matters in Python. Python is case-sensitive: min and Min are different.
Spelling matters in Python. You must match the spelling of functions and variables exactly.
Indentation matters in Python. Indentation is used to define code blocks and must be consistent.

Functions
---------
Functions are used to group code together and make it more readable and reusable.
We define custom functions that can be called later in the code.
Functions are blocks of logic that can take inputs, perform work, and return outputs.

Defining Functions
------------------
Define a function using the def keyword, followed by the function name, parentheses, and a colon. 
The function name should describe what the function does.
In the parentheses, specify the inputs needed as arguments the function takes.

For example:
   The function filtered_data() takes no arguments.
   The function between(min, max) takes two arguments, a minimum and maximum value.
   Arguments can be positional or keyword arguments, labeled with a parameter name.

The function body is indented (consistently!) after the colon. 
Use the return keyword to return a value from a function.

Calling Functions
-----------------
Call a function by using its name followed by parentheses and any required arguments.
    
Decorators
----------
Use the @ symbol to decorate a function with a decorator.
Decorators a concise way of calling a function on a function.
We don't typically write decorators, but we often use them.


# Create an input for year selection
ui.input_slider(
    "selected_year",
    "Year of Observation",
    min=2000, max=2020,
    value=2010,  # Default value
    step=1
)

# Assuming penguins_df is a pandas DataFrame with a 'year' column
isYearMatch = penguins_df["year"].isin([2010])  # <-- What to change here? Replace isin([2010]) with == input.selected_year()

# Filter DataFrame based on the year
filtered_df_by_year = penguins_df[isYearMatch]


# Create an input for island selection
ui.input_checkbox_group(
    "selected_island_list",
    "Islands in Scatterplot",
    ["Torgersen", "Dream", "Biscoe"],
    selected=["Torgersen", "Dream"],
    inline=True,
)

# Assuming penguins_df is a pandas DataFrame 
isSpeciesMatch = penguins_df["species"].isin(['Adelie', 'Chinstrap'])
isIslandMatch = penguins_df["island"].isin(['Dream', 'Biscoe'])  # <-- What to change here? Change ['Dream', 'Biscoe'] to input.selected_island_list()

# Combining conditions with AND (&) to get a filtered DataFrame
filtered_df_and = penguins_df[isSpeciesMatch & isIslandMatch]


# Create an input 
  ui.input_checkbox_group(
        "selected_species_list",
        "Species in Scatterplot",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )


# Assuming penguins_df is a pandas DataFrame 
isSpeciesMatch = penguins_df["species"].isin(['Adelie', 'Chinstrap']) --input.selected_species_list()
isIslandMatch = penguins_df["island"].isin(['Dream', 'Biscoe'])

# Combining conditions with AND (&) to get a filtered df
filtered_df_and = penguins_df[isSpeciesMatch & isIslandMatch]

# Combining conditions with OR (|) to get a filtered df
filtered_df_or = penguins_df[isSpeciesMatch | isIslandMatch]
