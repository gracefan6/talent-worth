import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dataset_utils import get_datasets

GRID_COLOR = "#595959"
JOB_TITLES = [
    'Business Analyst',
    'Data Analyst',
    'Data Scientist',
    'Data Engineer/DBA',
    'Software Engineer',
    'Statistician/Research Scientist'
]
PROGRAMMING_LANGUAGE = ['Bash', 'C', 'C++', 'Java', 'Javascript', 'MATLAB',
                        'Other', 'Python', 'R', 'SQL', 'TypeScript']
TIME_WRITING_CODE = ['< 1 years', '1-2 years',
                     '3-5 years', '5-10 years', '10-20 years', '20+ years']
COMPANY_SIZE = [
    '0-49 employees',
    '50-249 employees',
    '250-999 employees',
    '1000-9,999 employees',
    '> 10,000 employees'
]


##################################### datasets #####################################################
kaggle, glassdoor = get_datasets()

##################################### polar chart plotting #########################################


class PolarPlot():

    def __init__(self):
        self.figure = go.Figure()
        self.range = (0, 0)
        self.theta = ['Business Analyst', 'Data Analyst', 'Data Scientist', 'Data Engineer/DBA',
                      'Software Engineer', 'Statistician/Research Scientist', 'Business Analyst']

    def update_common_layout(self):
        """
        Updates general layout characteristics
        """
        self.figure.update_layout(
            showlegend=True,
            legend_itemclick='toggleothers',
            legend_itemdoubleclick='toggle',
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            autosize=True,
            font_color="white",
            uirevision=True,
            height=400,
            margin=dict(t=10)
        )

    def update_commom_polar_layout(self):
        """
        Updates polar layout characteristics
        """
        self.figure.update_layout(
            polar_bgcolor='rgba(0, 0, 0, 0)',

            polar_radialaxis_visible=True,
            polar_radialaxis_showticklabels=True,
            polar_radialaxis_tickfont_color='darkgrey',
            polar_radialaxis_showline=False,
            polar_radialaxis_layer='below traces',
            polar_radialaxis_gridcolor=GRID_COLOR,
            polar_radialaxis_range=self.range,

            # polar_angularaxis_color='gray',
            polar_angularaxis_showline=True,
            polar_angularaxis_linecolor=GRID_COLOR,
            polar_angularaxis_gridcolor=GRID_COLOR,
        )

    def add_data(self, data, country, hover_template='%{r:0.0f}%'):
        """
        Adds a trace to the figure following the same standard for each trace
        """
        # add the first element to the end of the list to "close" the polar chart
        data.append(data[0])
        self.figure.add_trace(
            go.Scatterpolar(
                r=data,
                theta=self.theta,
                mode='lines',
                name=country,
                hoverinfo='name+r',
                hovertemplate=hover_template,
                showlegend=True,
                line_shape='spline',
                line_smoothing=0.8,
                line_width=3
            )
        )
        # update the max range
        self.update_range(data)

    def update_range(self, data):
        """
        Updates the range to be 110% of maximum value of all traces
        """
        max_range = max(data) * 1.1
        self.range = (
            0, max_range) if max_range > self.range[1] else self.range

    def get_figure(self):
        """
        Update layouts and shows the figure
        """
        self.update_common_layout()
        self.update_commom_polar_layout()
        return self.figure


def plot_polar(polar_plot, data, traces, x_names, agg_column, group_column, trace_column, hover_template):

    data_cp = data.copy()
    polar_plot.figure.data = tuple()

    for trace_name in traces:

        if agg_column in ('JobDescription', 'CloudPlatf'):
            data_cp['TempCol'] = data_cp[agg_column].apply(
                lambda x: trace_name.lower() in x)
        else:
            data_cp['TempCol'] = data_cp[agg_column].apply(
                lambda x: trace_name in x)

        plot_data = data_cp.groupby([group_column], as_index=False).agg({
            'TempCol': ['sum', 'count']})
        plot_data['TempColPct'] = plot_data['TempCol']['sum'] / \
            plot_data['TempCol']['count'] * 100
        plot_data = plot_data.TempColPct.tolist()
        polar_plot.add_data(plot_data, trace_name, hover_template)

##################################### Line chart plotting ############################################


class LinePlot():

    def __init__(self):
        self.figure = go.Figure()
        self.range = (0, 100)

    def update_axis_title(self, x, y):
        self.figure.update_layout(
            xaxis_title_text=x,
            yaxis_title_text=y,
        )

    def update_layout(self):
        """
        Creates a clean layout for ploting, adjusting multiple settings
        """
        self.figure.update_layout(
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            showlegend=True,
            legend_font_color='gray',
            legend_itemclick='toggleothers',
            legend_itemdoubleclick='toggle',
            xaxis={
                "visible": True,
                "showgrid": False,
                "gridwidth": 0.8,
                # "color": "white",
            },
            yaxis={
                "showgrid": True,
                "gridcolor": GRID_COLOR,
                "gridwidth": 0.5,
            },
            font_color='white'
        )

    def add_data(self, x_names, y_data, trace_name, hover_template):
        """
        Adds a trace to the figure following the same standard for each trace
        """
        self.figure.add_trace(
            go.Scatter(
                x=x_names,
                y=y_data,
                mode='lines',
                name=trace_name,
                hoverinfo='name+y',
                hovertemplate=hover_template,
                line_shape='spline',
                line_smoothing=0.8,
                line_width=3
            )
        )

    def get_figure(self):
        self.update_layout()
        return self.figure


def plot_lines(line_plot, data, traces, x_names, agg_column, group_column, trace_column, hover_template):
    """
    Creates aggregation to plot
    """
    line_plot.figure.data = tuple()
    for trace_name in traces:
        data_filtered = data[data[trace_column] == trace_name]
        plot_data = data_filtered.groupby([group_column], as_index=False).agg({
            agg_column: ['mean', 'count']})
        plot_data = plot_data[agg_column]['mean'].tolist()
        line_plot.add_data(x_names, plot_data, trace_name,
                           hover_template=hover_template)


########################################## getters ##################################################

job_proportion_polar_plot = PolarPlot()
time_of_coding_line_plot = LinePlot()
salary_line_plot = LinePlot()
job_skills_polar_plot = PolarPlot()
job_desc_polar_plot = PolarPlot()
prog_language_line_plot = LinePlot()


def get_salary_line_plot(job_titles=None):
    # salary_line_plot.figure.data = tuple()
    traces = job_titles if job_titles is not None else JOB_TITLES
    x_names = COMPANY_SIZE
    plot_lines(
        salary_line_plot,
        data=kaggle,
        traces=traces,
        x_names=x_names,
        agg_column='Salary',
        group_column='CompanySize',
        trace_column='JobTitle',
        hover_template='U$%{y:,.2r}'
    )

    xaxis_title = 'Company size'
    yaxis_title = 'Average Salary (USD per Year)'
    salary_line_plot.update_axis_title(xaxis_title, yaxis_title)
    return salary_line_plot


def get_job_skills_polar_plot(selected_languages=None):
    traces = selected_languages if selected_languages is not None else PROGRAMMING_LANGUAGE

    x_names = JOB_TITLES

    plot_polar(
        job_skills_polar_plot,
        data=kaggle,
        traces=traces,
        x_names=x_names,
        agg_column='ProgLang',
        group_column='JobTitle',
        trace_column='ProgLang',
        hover_template='%{r:0.0f}%'
    )

    job_skills_polar_plot.figure.update_layout(
        polar_radialaxis_tickvals=[25, 50, 75],
        polar_radialaxis_ticktext=['25%', '50%', '75%'],
        polar_radialaxis_tickmode='array',
    )

    return job_skills_polar_plot


def get_job_proportion_polar_plot(countries):
    job_proportion_polar_plot.figure.data = tuple()
    proportion_dict = dict()
    for country in countries:
        glassdoor_country = glassdoor[glassdoor.Country == f"{country}"].groupby(
            ["JobTitle"], as_index=False).Count.sum().Count.tolist()
        glassdoor_country = (np.array(glassdoor_country) /
                             sum(glassdoor_country) * 100).tolist()
        proportion_dict[f"{country}"] = glassdoor_country

    for country, proportion in proportion_dict.items():
        job_proportion_polar_plot.add_data(proportion, country)

    return job_proportion_polar_plot


def get_job_propotion_pie_chart(country):
    glassdoor_country = glassdoor[glassdoor.Country == f"{country}"].groupby(
        ["JobTitle"], as_index=False).Count.sum().Count.tolist()
    glassdoor_country = (np.array(glassdoor_country) /
                         sum(glassdoor_country) * 100).tolist()

    fig = go.Figure(data=go.Pie(labels=JOB_TITLES, values=glassdoor_country))
    fig.update_traces(
        hoverinfo="label+percent",
        textposition='inside',
        textinfo='label',
    )
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=False,
        margin=dict(t=10),
        title=dict(
            text=country,
            x=0.5,
            y=0.95,
            xanchor="center",
            yanchor="top"
        ),
        font_color="white"
        # height=400
    )
    return fig


def get_prog_language_line_plot(selected_time_writing_code=None):
    traces = selected_time_writing_code if selected_time_writing_code is not None else list(
        set(kaggle.TimeWritingCode.tolist()))

    x_names = ['{} languages'.format(x) for x in range(7)]

    plot_lines(
        prog_language_line_plot,
        data=kaggle,
        traces=traces,
        x_names=x_names,
        agg_column='Salary',
        group_column='QtyProgLang',
        trace_column='TimeWritingCode',
        hover_template='U$%{y:,.2r}'
    )

    # Adding Averarage
    # plot_data = kaggle.groupby(
    #     ['QtyProgLang'], as_index=False).agg({'Salary': 'mean'})
    # plot_data = plot_data.Salary.tolist()
    # prog_language_line_plot.add_data(
    #     x_names, plot_data, 'Average', hover_template='U$%{y:,.2r}')

    xaxis_title = 'Quantity of programming languages used on a regular basis'
    yaxis_title = 'Average Salary (USD per Year)'
    prog_language_line_plot.update_axis_title(xaxis_title, yaxis_title)

    return prog_language_line_plot


def get_countries():
    countries = list(set(glassdoor["Country"]))
    countries.sort()
    return countries


def get_job_titles():
    return JOB_TITLES


def get_programming_language():
    return PROGRAMMING_LANGUAGE


def get_time_writing_code():
    return TIME_WRITING_CODE
