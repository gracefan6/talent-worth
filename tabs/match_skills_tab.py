import utils
import dash_core_components as dcc
import dash_html_components as html
from html_utils import generate_section_banner


def build_match_skills_tab():
    return html.Div(
        className="status-container",
        children=[
            build_match_skills_control_panel(),
            html.Div(
                id="graphs-container",
                children=[
                    build_match_skills_top_panel(),
                    build_match_skills_chart_panel()
                ])
        ]
    )


def build_match_skills_control_panel():
    return html.Div(
        id="quick-stats-match-skills",
        className="row",
        children=[
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Skills in Job Descriptions"),
                    html.Br(),
                    dcc.Checklist(
                        id="prog-language-multi-select",
                        options=[{"label": job, "value": job}
                                 for job in utils.get_programming_language()],
                        value=["Python"]
                    ),
                ]
            ),
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Coding Experience"),
                    html.Br(),
                    dcc.Checklist(
                        id="time-writing-code-multi-select",
                        options=[{"label": job, "value": job}
                                 for job in utils.get_time_writing_code()],
                        value=["1-2 years"],
                    ),
                ]
            ),

        ],
    )


def build_match_skills_top_panel():
    return html.Div(
        id="top-section-container-match-skills",
        className="row",
        children=[
            html.Div(
                className="panel",
                children=[
                    generate_section_banner(
                        "Skills in Job Descriptions"),
                    dcc.Graph(
                        id="job-skills-desc-polar-chart",
                        figure=utils.get_job_skills_polar_plot().get_figure()
                    )
                ]
            )
        ],
    )


def build_match_skills_chart_panel():
    return html.Div(
        # id="control-chart-container",
        className="panel",
        children=[
            generate_section_banner("Quantity of Programming Languages"),
            dcc.Graph(id="time-writing-code-line-chart",
                      figure=utils.get_prog_language_line_plot().get_figure())
        ]
    )
