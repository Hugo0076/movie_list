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

    def add_movie(self, title):
        new_row = pd.DataFrame([[title, dt.datetime.now(), 'No', None, None]], columns=list(self.movie_df.columns))
        self.movie_df = pd.concat([self.movie_df.copy(), new_row])
        self.movie_df.reset_index(drop=True, inplace=True)
        print(self.movie_df)

    def submit_rating(self, title, h_score, m_score):
        print(self.movie_df.index)
        print(self.movie_df[self.movie_df['Title'] == title])
        idx = self.movie_df.index[self.movie_df['Title'] == title].tolist()[0]
        print(idx)
        print(self.movie_df.iloc[idx,:])
        self.movie_df.iloc[idx,2:5] = ['Yes', h_score, m_score]
        print('df changed')
        print(self.movie_df.iloc[idx,:])

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
        return dbc.Table.from_dataframe(df.reset_index(), striped=False, bordered=True, hover=True)

    def main(self):
        print("launching dash")
        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], prevent_initial_callbacks=True)
        app.layout = html.Div([
            html.H1(children="Movie Thingo", style={"textAlign": "center", "padding": "40px"}, id='title'),
            html.Div(id='ph1', children = []),
            html.Div(id='ph2', children = []),
            html.Div(id='ph3', children = []),
            html.Div(id='ph4', children = []),
            html.Div(id='ph5', children = []),
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

                
                
                #dbc.Table.from_dataframe(self.movie_df, striped=True, bordered=True, hover=True), style={"textAlign": "center", "padding": "10px"})
            
            ], style={"textAlign": "center"}),
        ])
        
        #@app.callback(
        #    Output('container-button-basic', 'children'),
        #    Input('submit-val', 'n_clicks'),
        #    State('input-on-submit', 'value')
        #)
        #def update_output(n_clicks, value):
        #    return 'The input value was "{}" and the button has been clicked {} times'.format(
        #        value,
        #        n_clicks
        #    )
        @app.callback(
            Output("new_movie_response", "children"),
            Input("new_movie_button", "n_clicks"),
            State('new_movie_input', "value")
        )
        def on_button_click(n_clicks, name):
            if n_clicks:
                if name:
                    self.add_movie(name)
                    print(f'Added {name} to list')
                    return f'Added {name} to list'
                else:
                    return 'Please enter a movie'
            else:
                return ''

        @app.callback(
            Output("movie_table_div2", "children"),
            [Input("options", "value"), Input("new_movie_response", "children"), Input("ph3", "children")]
        )
        def updateTable(option, t, t2):
            return self.prepare_table(option) #dbc.Table.from_dataframe(self.movie_df.reset_index(), striped=False, bordered=True, hover=True)
        
        @app.callback(
            Output("movie_dropdown", "options"),
            [Input("new_movie_response", "children"), Input("ph3", "children")]
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
            Output('ph1', 'children'),
            Output('ph4', "children"),
            Input("submit_button", "n_clicks"),
            State('movie_dropdown', "value"),
            State('h_score', "value"),
            State('m_score', "value")
        )
        def submit(n_clicks, title, h_score, m_score):
            self.submit_rating(title, h_score, m_score)
            return [], []

        @app.callback(
            Output('ph2', 'children'),
            Output('ph5', "children"),
            Input("remove_button", "n_clicks"),
            State('movie_dropdown', "value")
        )
        def submit(n_clicks, title):
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