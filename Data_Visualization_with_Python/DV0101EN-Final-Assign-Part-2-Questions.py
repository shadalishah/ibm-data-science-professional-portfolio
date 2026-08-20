#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


# ---------------------------------------------------------
# Load the dataset
# ---------------------------------------------------------

url = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)

data = pd.read_csv(url)


# ---------------------------------------------------------
# Initialize the Dash application
# ---------------------------------------------------------

app = dash.Dash(__name__)

app.title = "Automobile Sales Statistics Dashboard"


# ---------------------------------------------------------
# Dropdown options
# ---------------------------------------------------------

dropdown_options = [
    {
        "label": "Yearly Statistics",
        "value": "Yearly Statistics"
    },
    {
        "label": "Recession Period Statistics",
        "value": "Recession Period Statistics"
    }
]

year_list = [i for i in range(1980, 2024, 1)]


# ---------------------------------------------------------
# Application layout
# ---------------------------------------------------------

app.layout = html.Div(
    children=[

        # TASK 2.1: Dashboard title
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "fontSize": 24
            }
        ),

        # TASK 2.2: Report type dropdown
        html.Div(
            children=[
                html.Label(
                    "Select Statistics:",
                    style={
                        "fontWeight": "bold",
                        "display": "block",
                        "marginBottom": "5px"
                    }
                ),

                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    value="Select Statistics",
                    placeholder="Select a report type",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": "20px",
                        "textAlignLast": "center"
                    }
                )
            ],
            style={
                "width": "80%",
                "margin": "20px auto"
            }
        ),

        # TASK 2.2: Year dropdown
        html.Div(
            children=[
                html.Label(
                    "Select Year:",
                    style={
                        "fontWeight": "bold",
                        "display": "block",
                        "marginBottom": "5px"
                    }
                ),

                dcc.Dropdown(
                    id="select-year",
                    options=[
                        {
                            "label": year,
                            "value": year
                        }
                        for year in year_list
                    ],
                    value="Select-year",
                    placeholder="Select-year",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": "20px",
                        "textAlignLast": "center"
                    }
                )
            ],
            style={
                "width": "80%",
                "margin": "20px auto"
            }
        ),

        # TASK 2.3: Output division
        html.Div(
            children=[
                html.Div(
                    id="output-container",
                    className="chart-grid",
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "width": "100%"
                    }
                )
            ]
        )
    ]
)


# ---------------------------------------------------------
# TASK 2.4: Enable or disable the year dropdown
# ---------------------------------------------------------

@app.callback(
    Output(
        component_id="select-year",
        component_property="disabled"
    ),
    Input(
        component_id="dropdown-statistics",
        component_property="value"
    )
)
def update_input_container(selected_statistics):

    if selected_statistics == "Yearly Statistics":
        # False means year dropdown is enabled
        return False

    # True means year dropdown is disabled
    return True


# ---------------------------------------------------------
# Callback for displaying dashboard graphs
# ---------------------------------------------------------

@app.callback(
    Output(
        component_id="output-container",
        component_property="children"
    ),
    [
        Input(
            component_id="dropdown-statistics",
            component_property="value"
        ),
        Input(
            component_id="select-year",
            component_property="value"
        )
    ]
)
def update_output_container(selected_statistics, input_year):

    # -----------------------------------------------------
    # TASK 2.5: Recession Report Statistics
    # -----------------------------------------------------

    if selected_statistics == "Recession Period Statistics":

        recession_data = data[data["Recession"] == 1]

        # Plot 1:
        # Average automobile sales over recession years
        yearly_rec = (
            recession_data
            .groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                markers=True,
                title=(
                    "Average Automobile Sales Fluctuation "
                    "over Recession Periods"
                ),
                labels={
                    "Year": "Year",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 2:
        # Average automobile sales by vehicle type
        average_sales = (
            recession_data
            .groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                color="Vehicle_Type",
                title=(
                    "Average Automobile Sales by Vehicle Type "
                    "during Recession Periods"
                ),
                labels={
                    "Vehicle_Type": "Vehicle Type",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 3:
        # Total advertisement expenditure by vehicle type
        exp_rec = (
            recession_data
            .groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Advertisement Expenditure "
                    "by Vehicle Type during Recession Periods"
                )
            )
        )

        # Plot 4:
        # Effect of unemployment rate on sales
        unemp_data = (
            recession_data
            .groupby(
                ["unemployment_rate", "Vehicle_Type"]
            )["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                barmode="group",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                    "Vehicle_Type": "Vehicle Type"
                },
                title=(
                    "Effect of Unemployment Rate "
                    "on Vehicle Type and Sales"
                )
            )
        )

        # Display recession graphs in two rows and two columns
        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=R_chart1,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=R_chart2,
                        style={"width": "50%"}
                    )
                ],
                style={
                    "display": "flex",
                    "width": "100%"
                }
            ),

            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=R_chart3,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=R_chart4,
                        style={"width": "50%"}
                    )
                ],
                style={
                    "display": "flex",
                    "width": "100%"
                }
            )
        ]

    # -----------------------------------------------------
    # TASK 2.6: Yearly Report Statistics
    # -----------------------------------------------------

    elif (
        selected_statistics == "Yearly Statistics"
        and input_year not in [None, "Select-year"]
    ):

        input_year = int(input_year)

        yearly_data = data[data["Year"] == input_year]

        # Plot 1:
        # Yearly average automobile sales for full period
        yas = (
            data
            .groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                markers=True,
                title="Yearly Average Automobile Sales",
                labels={
                    "Year": "Year",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 2:
        # Total monthly automobile sales for selected year
        mas = (
            yearly_data
            .groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
            .sort_values("Month")
        )

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                markers=True,
                title=(
                    "Total Monthly Automobile Sales in "
                    f"{input_year}"
                ),
                labels={
                    "Month": "Month",
                    "Automobile_Sales": "Total Automobile Sales"
                }
            )
        )

        # Plot 3:
        # Average number of vehicles sold by vehicle type
        avr_vdata = (
            yearly_data
            .groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                color="Vehicle_Type",
                title=(
                    "Average Vehicles Sold by Vehicle Type "
                    f"in the Year {input_year}"
                ),
                labels={
                    "Vehicle_Type": "Vehicle Type",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 4:
        # Total advertisement expenditure by vehicle type
        exp_data = (
            yearly_data
            .groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Advertisement Expenditure "
                    f"for Each Vehicle in {input_year}"
                )
            )
        )

        # Display yearly graphs in two rows and two columns
        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=Y_chart1,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=Y_chart2,
                        style={"width": "50%"}
                    )
                ],
                style={
                    "display": "flex",
                    "width": "100%"
                }
            ),

            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=Y_chart3,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=Y_chart4,
                        style={"width": "50%"}
                    )
                ],
                style={
                    "display": "flex",
                    "width": "100%"
                }
            )
        ]

    else:
        return html.Div(
            "Please select a report type and year.",
            style={
                "textAlign": "center",
                "fontSize": "20px",
                "color": "#503D36",
                "marginTop": "30px"
            }
        )


# ---------------------------------------------------------
# Run the Dash application
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)