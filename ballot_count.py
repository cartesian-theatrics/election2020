import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import os
import pprint
from dateutil import parser
import requests
import pickle


def collapse_results_by_party(results_by_candidate, candidates):
    results_by_party = {}
    for candidate, count in results_by_candidate.items():
        party = candidates[candidate]['party']
        results_by_party[party] = results_by_party.get(party, 0) + count

    return results_by_party


def plot_state(state_data):
    xs, ys, colors, text = [], [], [], []
    idx = 0
    for data_point in state_data['timeseries']:
        vote_shares = data_point['vote_shares']
        date = parser.parse(data_point['timestamp'])
        xs.extend([date, date, date])
        idx += 3
        ys.extend([vote_shares['trumpd'], vote_shares['bidenj'],
                   1 - (vote_shares['trumpd'] + vote_shares['bidenj'])])
        colors.extend([1, 2, 3])
        text.extend(["Trump", "Biden", "Other"])
    return go.Scatter(x=xs,
                      y=ys,
                      mode='markers',
                      text=text,
                      marker=dict(
                          color=colors,
                          colorscale='Viridis',
                          line_width=1))


def plot_all_states(state_data):
    xs, ys, colors, text = [], [], [], []
    for data_point in state_data['counties']:
        vote_shares = data_point['vote_shares']
        date = parser.parse(data_point['timestamp'])

        xs.extend([date, date, date])
        ys.extend([vote_shares['trumpd'], vote_shares['bidenj'],
                   1 - (vote_shares['trumpd'] + vote_shares['bidenj'])])
        colors.extend([1, 3, 5])
        text.extend(["Trump", "Biden", "Other"])
    return go.Scatter(x=xs,
                      y=ys,
                      mode='markers',
                      text=text,
                      marker=dict(
                          color=colors,
                          colorscale='Viridis',
                          line_width=1))


def country_plots(election_data):
    """
    :param election_data:
    """
    fig = make_subplots(rows=len(election_data),
                        cols=1,
                        subplot_titles=list(election_data.keys()))

    for i, (state, state_results) in enumerate(all_results.items()):
        assert len(state_results['data']['races']) == 1
        race = state_results['data']['races'][0]
        fig_data = plot_state(race)
        fig.add_trace(fig_data, row=i+1, col=1)

    fig.update_layout(showlegend=False,
                      title_text="Election Plot",
                      height=30000)
    return fig


states = ['Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado',
          'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Iowa', 'Idaho',
          'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts',
          'Maryland', 'Maine', 'Michigan', 'Minnesota', 'Missouri', 'Mississippi',
          'Montana', 'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire',
          'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma',
          'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
          'Tennessee', 'Texas', 'Utah', 'Virginia', 'Vermont', 'Washington',
          'Wisconsin', 'West Virginia', 'Wyoming']

if os.path.exists("election-assets.pkl"):
    all_results = pickle.load(open("election-assets.pkl", 'rb'))
else:
    all_results = {}
    for state in states:
        print('Downloading {}'.format(state))
        formatted_state = state.lower().replace(' ', '-')
        state_results = requests.get('https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{}/president.json'.format(formatted_state)).json()
        all_results[formatted_state] = state_results

    pickle.dump(all_results, open("election-assets.pkl", 'wb'))

fig = plot_all_states(all_results)
fig.show()

# records = []
# for state, state_results in all_results.items():
#     race = state_results['data']['races'][0]
# 
#     for candidate in race['candidates']:
#         if candidate['party_id'] == 'republican':
#             candidate['party'] = 'rep'
#         elif candidate['party_id'] == 'democrat':
#             candidate['party'] = 'dem'
#         else:
#             candidate['party'] = 'trd'
#     candidates = { candidate['candidate_key']: candidate for candidate in race['candidates'] }
# 
#     for data_point in race['timeseries']:
#         data_point['state']             = state
#         data_point['expected_votes']    = race['tot_exp_vote']
#         data_point['trump2016']         = race['trump2016']
#         data_point['votes2012']         = race['votes2012']
#         data_point['votes2016']         = race['votes2016']
# 
#         vote_shares = collapse_results_by_party(data_point['vote_shares'], candidates)
#         for party in ['rep', 'dem', 'trd']:
#             data_point['vote_share_{}'.format(party)] = vote_shares.get(party, 0)
# 
#         data_point.pop('vote_shares')
#         records.append(data_point)
# 
# time_series_df = pd.DataFrame.from_records(records)
# time_series_df.to_csv('nyt_ts.csv', encoding='utf-8')
