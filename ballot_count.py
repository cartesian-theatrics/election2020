import os
import pickle

import plotly.graph_objects as go
import requests
from dateutil import parser
from plotly.subplots import make_subplots


def plot_state(state_data):
    trump, biden, other, dates = [], [], [], []
    for data_point in state_data['timeseries']:
        vote_shares = data_point['vote_shares']
        date = parser.parse(data_point['timestamp'])
        trump.append(vote_shares['trumpd'])
        biden.append(vote_shares['bidenj'])
        other.append(1 - (vote_shares['trumpd'] + vote_shares['bidenj']))
        dates.append(date)
    return [go.Scatter(x=dates, y=trump, mode='markers', name="Trump", marker_color='red'),
            go.Scatter(x=dates, y=biden, mode='markers', name="Biden", marker_color='blue'),
            go.Scatter(x=dates, y=other, mode='markers', name="Other", marker_color='gold')]


def plot_all_states(election_data):
    fig = make_subplots(rows=len(election_data),
                        cols=1,
                        subplot_titles=list(election_data.keys()))

    for i, (state, state_results) in enumerate(all_results.items()):
        assert len(state_results['data']['races']) == 1
        race = state_results['data']['races'][0]
        for fig_data in plot_state(race):
            fig.add_trace(fig_data, row=i+1, col=1)

    fig.update_layout(showlegend=False,
                      title_text="Election Plot",
                      height=30000)
    return fig


states = [
    'Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia',
    'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky',
    'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
    'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina',
    'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico',
    'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
    'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin',
    'West Virginia', 'Wyoming',
]

if os.path.exists("election-assets.pkl"):
    all_results = pickle.load(open("election-assets.pkl", 'rb'))
else:
    all_results = {}
    for state in states:
        print('Downloading {}'.format(state))
        formatted_state = state.lower().replace(' ', '-')
        state_results = requests.get(f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{formatted_state}/president.json').json()
        all_results[formatted_state] = state_results

    pickle.dump(all_results, open("election-assets.pkl", 'wb'))

fig = plot_all_states(all_results)
fig.show()
