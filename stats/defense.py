import pandas as pd
import matplotlib.pyplot as plt
from frames import games, info, events;

# Select all rows of games that have a play type without an NP event.
plays = games.query("type == 'play' & event != 'NP'");

# Rename the columns of plays.
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year'];

# Select all groups of plays that represent the same plate appearance.
pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team', 'player']];

# Group plate appearances by year, game identifier, and team, add a count column, and rename that column PA.
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA');

# Set the indices of events to the four columns year, game identifier, team, and event type.
events = events.set_index(['year', 'game_id', 'team', 'event_type']);

# Unstack events using the new indices (seems to do a new group by).
events = events.unstack().fillna(0).reset_index();

# Remove a level of column labels from events.
events.columns = events.columns.droplevel();

# Rename columns of events.
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO'];

# Remove the label of the index on the columns axis.
events = events.rename_axis(None, axis='columns');

# Merge events with plate appearances on year, game identifier, and team.
events_plus_pa = pd.merge(events, pa, how='outer', left_on=['year', 'game_id', 'team'], right_on=['year', 'game_id', 'team']);

# Merge events with plate appearances and info as defense.
defense = pd.merge(events_plus_pa, info);

# Calculate DER into defense using the calculation 1 - ((H + ROE) / (PA - BB - SO - HBP - HR)).
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) / (defense['PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']));

# Transform the year column of defense to numeric.
defense.loc[:, 'year'] = pd.to_numeric(defense['year']);

# Select the DER of defense for all years >= 1978.
der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']];

# Reshape DER with a pivot on year to defense DER.
der = der.pivot(index='year', columns='defense', values='DER');

# Add plot metadata.
der.plot(x_compat=True, xticks=range(1978, 2018, 4), rot=45);

# Show the plot.
plt.show();