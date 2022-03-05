from dash import Dash, dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from collections import OrderedDict, defaultdict
import pandas as pd
import datetime as dt

class MovieDataBase():
    def __init__(self) -> None:
        super().__init__()
        self.movie_df = pd.read_csv('movie_df.csv')
        self.show_cols = ['Title', 'Watched?', 'Time Watched', 'H', 'M']

    def add_movie(self, title):
        if not title:
            return 'Please enter a title first', 'warning'
        if title not in list(self.movie_df['Title']):
            new_row = pd.DataFrame([[title, dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'No', None, None, None]], columns=list(self.movie_df.columns))
            self.movie_df = pd.concat([self.movie_df.copy(), new_row])
            self.movie_df.reset_index(drop=True, inplace=True)
            return f'Added {title} to list', 'success'
        else:
            return 'Ooops, this movie is already in the list', 'warning'

    def submit_rating(self, title, h_score, m_score):
        idx = self.movie_df.index[self.movie_df['Title'] == title].tolist()[0]
        if h_score and m_score:
            self.movie_df.iloc[idx,2:6] = ['Yes', dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), h_score, m_score]
            return f'Submitted rating for {title}', 'success'
        else:
            return f'Please submit both scores (between 0 and 10)', 'danger'

    def remove_movie(self, title):
        idx = self.movie_df.index[self.movie_df['Title'] == title].tolist()[0]
        self.movie_df = self.movie_df.drop(idx).reset_index(drop=True)
    
    def prepare_table(self, option):
        if option == 1: #Watched
            df = self.movie_df[self.movie_df.iloc[:,2] == 'Yes']
        elif option == 2: #Unwatched
            df = self.movie_df[self.movie_df.iloc[:,2] == 'No']
        elif option == 3: #All
            df = self.movie_df
        total = self.movie_df.shape[0]
        watched = self.movie_df[self.movie_df.iloc[:,2] == 'Yes'].shape[0]
        title = f"{watched} Watched - {total} Total"
        return dbc.Table.from_dataframe(df.reset_index()[self.show_cols], striped=False, bordered=True, hover=True), title

    def main(self):
        print("launching dash")
        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])#, prevent_initial_callbacks=True)
        app.layout = html.Div([
            html.H1(children="XXX", style={"textAlign": "center", "padding": "40px"}, id='title'),
            html.Div(
                    dbc.InputGroup(
                        [
                            dbc.Select(
                                options=[{"label": f"{i}-way Mulligan", "value": i} for i in range(1,6)],
                                value=4,
                                style={"font-size":"30px"}
                            ),
                            dbc.Button("GO!", id="mulligan_button", color="success", n_clicks=0, style={"font-size":"30px"}),
                        ]
                    ),
                    style={
                            "width": "500px",
                            'margin': 'auto',
                            "vertical-align": "top",
                            "padding": "10px",
                            "font-size": "150px"
                        }
                ),
            html.Div(id='ph1', children = []),
            html.Div(id='ph2', children = []),
            html.Div(id='ph3', children = []),
            html.Div(id='ph4', children = []),
            html.Div(id='ph5', children = []),
            html.Div(
                    html.Hr(
                        style={
                            "border-top":"1px dashed #fff"
                        }
                    ),
                    style={
                            "width": "800px",
                            'margin': 'auto',
                        }
                ),
            html.Div([
                html.Div(
                    dbc.InputGroup(
                        [
                            dbc.Input(id='new_movie_input', type='text', placeholder="Movie Name"),
                            dbc.Button('Submit', id='new_movie_button', n_clicks=0),
                        ]),
                    style={
                            "width": "500px",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "10px",
                        }
                ),
                html.Div(id='new_movie_response',
                    children='Enter a value and press submit', style={"textAlign": "center", "padding": "10px"}),
                html.Div(
                    dbc.Alert(
                        "",
                        id="alert",
                        is_open=False,
                        duration=2000,
                    ),
                    style={
                            "width": "500px",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "10px",
                        }
                ),
                dbc.RadioItems(
                    options=[
                        {"label": "Watched", "value": 1},
                        {"label": "Unwatched", "value": 2},
                        {"label": "All", "value": 3},
                    ],
                    value=3,
                    id="options",
                    inline=True,
                ),
                html.Div(id='movie_table_div2',
                    children=dbc.Table.from_dataframe(self.movie_df.reset_index(), striped=True, bordered=True, hover=True), style={"textAlign": "center", "padding": "10px", "width": "800px",'margin': 'auto'}
                ),
                html.Div(id='movie_dropdown_div',
                    children=dcc.Dropdown([], False, id='movie_dropdown', style={
                            'color': 'black'
                        }
                    ), style={"textAlign": "center", "padding": "10px", "width": "400px",'margin': 'auto'}
                ),
                html.Div(
                    dbc.Alert(
                        "",
                        id="alert_2",
                        is_open=False,
                        duration=2000,
                    ),
                    style={
                            "width": "500px",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "10px",
                        }
                ),
                html.Div(id='rating_ui',
                    children = [
                        html.Div(
                            children=[
                                html.Div(id='h_score_div',
                                    children=dbc.Input(type="number", placeholder = "Hugo's Rating", min=0, max=10, step=0.5, id='h_score'),
                                    style={"textAlign": "center", "display": "inline-block", "padding": "10px", "width": "200px",'margin': 'auto'}
                                ),
                                html.Div(id='m_score_div',
                                    children=dbc.Input(type="number", placeholder = "Max's Rating", min=0, max=10, step=0.5, id='m_score'),
                                    style={"textAlign": "center", "display": "inline-block", "padding": "10px", "width": "200px",'margin': 'auto'}
                                )
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(id='submit_button',
                                    children=dbc.Button("Submit Review", color="primary", className="me-1"),
                                    style={"textAlign": "center", "padding": "10px", "display": "inline-block",'margin': 'auto'}
                                ),
                                html.Div(id='remove_button',
                                    children=dbc.Button("Remove from list", color="danger", className="me-1"),
                                    style={"textAlign": "center", "padding": "10px", "display": "inline-block",'margin': 'auto'}
                                )
                            ],
                            style={"textAlign": "center", "display": "inline-block", "padding": "10px", "width": "400px",'margin': 'auto'}
                        )
                    ],
                    style={"textAlign": "center", 'visibility':'hidden','margin': 'auto'}
                )
            ], style={"textAlign": "center"}),
        ])
        @app.callback(
            Output("alert", "is_open"),
            Output("alert", "children"),
            Output("alert", "color"),
            Input("new_movie_button", "n_clicks"),
            State('new_movie_input', "value")
        )
        def on_button_click(n_clicks, name):
            if n_clicks:
                response, code = self.add_movie(name)
                return True, response, code
            else:
                return False, "", ""

        @app.callback(
            [Output("movie_table_div2", "children"), Output("title", "children")],
            [Input("options", "value"), Input("alert", "children"), Input("ph3", "children")]
        )
        def updateTable(option, t, t2):
            return self.prepare_table(option)
        
        @app.callback(
            Output("movie_dropdown", "options"),
            [Input("alert", "children"), Input("ph3", "children")]
        )
        def updateDropdown(children, children2):
            unwatched = list(self.movie_df[self.movie_df.iloc[:,2] == 'No']['Title'])
            return unwatched

        @app.callback(
            Output("rating_ui", "style"),
            State("rating_ui", "style"),
            State('movie_dropdown', 'value'),
            Input('movie_dropdown', 'value'),
            Input("movie_dropdown", "options"),
            Input("ph3", "children")
        )
        def show_rating_ui(style, title, trigger, trigger2, trigger3):
            print(f'triggered {title}')
            if title:
                style.update({'visibility':'visible'})
            else:
                style.update({'visibility':'hidden'})
            return style
        
        @app.callback(
            Output("ph3", "children"),
            Input('ph1', 'children'),
            Input('ph2', 'children')
        )
        def trigger(t1,t2):
            return []
        
        @app.callback(
            Output("alert_2", "is_open"),
            Output("alert_2", "children"),
            Output("alert_2", "color"),
            Output('ph1', 'children'),
            Output('ph4', "children"),
            Input("submit_button", "n_clicks"),
            State('movie_dropdown', "value"),
            State('h_score', "value"),
            State('m_score', "value")
        )
        def submit(n_clicks, title, h_score, m_score):
            if n_clicks:
                response, code = self.submit_rating(title, h_score, m_score)
                return True, response, code, [], []
            else:
                return False, "", "", [], []

        @app.callback(
            Output('ph2', 'children'),
            Output('ph5', "children"),
            Input("remove_button", "n_clicks"),
            State('movie_dropdown', "value")
        )
        def submit(n_clicks, title):
            if n_clicks:
                self.remove_movie(title)
            return [], []
        
        @app.callback(
            Output('movie_dropdown', "value"),
            Input('ph4', "children"),
            Input('ph5', "children"),
        )
        def submit(t,t2):
            return False

        app.run_server(debug=True)

if __name__ == '__main__':
    mdb = MovieDataBase()
    mdb.main()