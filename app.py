import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import utils
from tabs.job_trend_tab import build_job_trend_tab
from tabs.match_skills_tab import build_match_skills_tab


app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server


def init_value_setter_store():
    # Initialize store data
    state_dict = {"a": 1}
    return state_dict


####################################### Layout elements ###########################################################

# top banner
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H4("TalentWorth"),
                    html.H6("Make your skills with future trend"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Div(
                        [
                            html.A(
                                html.Button("View on Github",
                                            id="view-on-github"),
                                href="https://github.com/EckoTan0804/talent-worth",

                            )
                        ]

                    ),
                ],
            ),
        ],
    )

# tabs


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="job-trend",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        label="Job Trend",
                        value="job-trend",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Match Skills",
                        value="match-skills",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="About Us",
                        value="about-us",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def build_about_us_tab():
    GROUP_MEMBERS = [
        "Grace Fan",
        "Katharina Koenig",
        "Linh Nguyen",
        "Vinuzan Ratnasingam",
        "Haobin Tan"
    ]
    return html.Div(
        # className="status-container",
        children=[
            html.Img(
                src=app.get_asset_url("talent-worth-logo.png"),
                style={'height': '30%', 'width': '30%'}
            ),
            html.Br(),
            html.Br(),
            html.H3("Group Members", style={"font-weight": "bold"}),
            html.Div(children=[html.H6(member) for member in GROUP_MEMBERS]),
            html.Br(),
            html.H3("Mentor/Tutor", style={"font-weight": "bold"}),
            html.H6("Lisa Zaeuner"),
            html.Br(),
            html.H3("Special Thanks", style={"font-weight": "bold"}),
            html.Div(
                children=[
                    html.Img(
                        src=app.get_asset_url("AiTalents.png"),
                        style={
                            'height': '15%',
                            'width': '15%',
                            "marginRight": 10,
                        }
                    ),
                    html.Img(
                        src=app.get_asset_url("TechQuartier.jpg"),
                        style={
                            'height': '10%',
                            'width': '10%',
                            "marginRight": 20,
                        }
                    ),
                ],
                style={
                    "justifyContent": "center",
                    'verticalAlign': 'middle',
                }),
            html.Br(),
            html.Br(),
        ],
        style={
            "justifyContent": "center",
            "textAlign": "center",
        }
    )


job_trend_tab = build_job_trend_tab()
match_skills_tab = build_match_skills_tab()
about_us_tab = build_about_us_tab()


@ app.callback(Output("app-content", "children"), [Input("app-tabs", "value")])
def render_tab_content(tab_switch):
    """Tabs switching"""
    if tab_switch == "job-trend":
        return job_trend_tab
    elif tab_switch == "match-skills":
        return match_skills_tab
    return about_us_tab


####################################### Job trend tab callbacks ###########################################################

@app.callback(
    Output("multi-country-dropdown", "value"),
    Output("job-proportion-pie", "figure"),
    Input("single-country-dropdown", "value"),
    State("multi-country-dropdown", "value"),
)
def update_job_proportion_pie_chart(selected_country, current_selected_countries):
    if selected_country not in current_selected_countries:
        current_selected_countries.append(selected_country)
    return current_selected_countries, utils.get_job_propotion_pie_chart(selected_country)


@app.callback(
    Output("job-proportion-differnet-countries-polar", "figure"),
    Input("multi-country-dropdown", "value"),
)
def update_job_proportion_polar_plot(selected_countries):
    return utils.get_job_proportion_polar_plot(selected_countries).get_figure()


@app.callback(
    Output("salary-line-plot", "figure"),
    Input("job-titles-multi-select", "value"),
)
def update_salary_line_plot(selected_job_titles):
    return utils.get_salary_line_plot(job_titles=selected_job_titles).get_figure()


####################################### Match skills tab callbacks ##########################################################

@app.callback(
    Output("job-skills-desc-polar-chart", "figure"),
    Input("prog-language-multi-select", "value")
)
def update_job_skills_polar_plot(selected_languages):
    return utils.get_job_skills_polar_plot(selected_languages).get_figure()


@app.callback(
    Output("time-writing-code-line-chart", "figure"),
    Input("time-writing-code-multi-select", "value")
)
def update_time_writing_code_line_chart(selected_time):
    return utils.get_prog_language_line_plot(selected_time).get_figure()


####################################### About us tab ##############################################################

def build_about_us_tab():
    pass


################################################################################################################
app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,
            n_intervals=50,
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
