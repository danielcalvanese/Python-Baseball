import pandas as pd
import matplotlib.pyplot as plt
from data import games;

# Resolve all plays in games.
plays = games[games['type'] == 'play'];

# Resolve all strike outs in plays.
strike_outs = plays[plays['event'].str.contains('K')];

# Group strike outs by year and game identifier and return the row count (these lines should be split in a real project).
strike_outs = strike_outs.groupby(['year', 'game_id']).size();

# Rename the size column that was created to 'strike_outs'.
strike_outs = strike_outs.reset_index(name='strike_outs');

# Transform the strike outs column into a numeric type.
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric);

# Plot strike outs.
strike_outs.plot(x='year', y='strike_outs', kind='scatter').legend('Strike Outs');

# Add plot metadata.
plt.xlabel('Year');
plt.ylabel('Strike Outs');

# Show the plot.
plt.show();
