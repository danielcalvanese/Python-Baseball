import pandas as pd
import matplotlib.pyplot as plt
from data import games;

# Resolve plays as games with the 'play' type and set its columns.
plays = games[games['type'] == 'play'];
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year'];

# Resolve hits.
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning', 'event']];

# Transform the inning column into a numeric type.
#hits = hits.loc[:, ['inning']].apply(pd.to_numeric); # Not sure why this causes errors later.
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])

# Build a dictionary of replacements mapping regular expressions to strings.
replacements = {
    r'^S(.*)': 'single',
    r'^D(.*)': 'double',
    r'^T(.*)': 'triple',
    r'^HR(.*)': 'hr'
};

# Replace events in hits using the replacements dictionary and store it as hit_type.
hit_type = hits['event'].replace(replacements, regex=True);

# Add the hit_type column to hits.
hits = hits.assign(hit_type=hit_type);

# Group hits by inning and hit type, add a count column, and rename the size column to count.
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count');

# Optimize the hit_type column in hits by changing it to be categorical.
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr']);

# Sort hits by inning and hit type.
hits = hits.sort_values(['inning', 'hit_type']);

# Reshape hits with a pivot on inning to hit type count.
hits = hits.pivot(index='inning', columns='hit_type', values='count');

# Add plot metadata.
hits.plot.bar(stacked=True);

# Show the plot.
plt.show();
