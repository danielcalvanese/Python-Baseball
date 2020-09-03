import os;
import glob;
import pandas as pd;

# Assemble the path to the game files.
#gameFilesPath = os.path.join(os.getcwd(), 'games', '*.EVE');

# Retrieve the game files in the game files path.  
#gameFiles = glob.glob(gameFilesPath);

# Fix because pluralsight tests have to be exact.
game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'));

# Sort the game files.
game_files.sort();

# Prep game frames.
game_frames = [];

# Build game frames.
for game_file in game_files:
  # Retrieve the game frame of the game file.
  gameFrame = pd.read_csv(game_file, names=['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event']);
  
  # Build game frame.
  game_frames.append(gameFrame);

# Build games by concatenating game frames.
games = pd.concat(game_frames);

# Filter the column 'multi5' by replacing '??' with '' (using hint dataframe.loc[row condition, [columns]] = new value).  
games.loc[games['multi5'] == '??', ['multi5']] = '';

# Extract the multi2 column from games as identifiers.
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})');

# Fill NaN values in the identifiers.  
identifiers = identifiers.fillna(method='ffill');

# Rename identifier columns to game_id and year.
identifiers.columns = ['game_id', 'year'];

# Add the identifier column to games.  
games = pd.concat([identifiers, games], axis=1, sort=False);

# Fill NaN values in games.
games = games.fillna(' ');

# Optomize the type column in games by changing it to be categorical.
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type']);

# Print the first five games.
print(games.head(5));