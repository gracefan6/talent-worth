import utils
import dash_core_components as dcc
import dash_html_components as html
from html_utils import generate_section_banner


def build_job_trend_tab():
    return html.Div(
        className="status-container",
        children=[
            build_job_trend_control_panel(),
            html.Div(id="graphs-container", children=[
                build_job_trend_top_panel(),
                build_job_trend_chart_panel()
            ])
        ]
    )


def build_job_trend_control_panel():
    return html.Div(
        id="quick-stats-job-trend",
        className="row",
        children=[
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Job Proportion"),
                    html.Br(),
                    dcc.Dropdown(
                        id="single-country-dropdown",
                        options=[{"label": country, "value": country}
                                 for country in utils.get_countries()],
                        value="China",
                        clearable=False,
                        searchable=True,
                    ),
                ]
            ),
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Job Proportion in Different Countries"),
                    html.Br(),
                    dcc.Dropdown(
                        id="multi-country-dropdown",
                        options=[{"label": country, "value": country}
                                 for country in utils.get_countries()],
                        value=["China"],
                        multi=True,
                        clearable=False,
                        searchable=True,
                        placeholder="Choose country"
                    ),
                ]
            ),
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Company Size Vs. Salary"),
                    html.Br(),
                    dcc.Checklist(
                        id="job-titles-multi-select",
                        options=[{"label": job, "value": job}
                                 for job in utils.get_job_titles()],
                        value=["Data Scientist"]
                    ),
                ]
            ),

        ],
    )


def build_job_trend_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner(
                        "Job Proportion in Different Countries"),
                    html.Div(
                        id="metric-div",
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id="job-proportion-differnet-countries-polar",
                                        figure=utils.get_job_proportion_polar_plot(
                                            ["China"]).get_figure()
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Job Proportion"),
                    dcc.Graph(
                        id="job-proportion-pie",
                        figure=utils.get_job_propotion_pie_chart("China")
                    )
                ],
            ),
        ],
    )


def build_job_trend_chart_panel():
    return html.Div(
        className="panel",
        children=[
            generate_section_banner("Salary"),
            dcc.Graph(id="salary-line-plot",
                      figure=utils.get_salary_line_plot().get_figure())
        ]
    )
