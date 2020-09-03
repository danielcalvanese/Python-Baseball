import pandas as pd;
import matplotlib.pyplot as plt;
from data import games;

# Resolve attendance as the columns year and multi3 where the type is info and multi2 is attendance (who designed this system).
attendance = games.loc[(games['type'] == 'info') & (games['multi2'] == 'attendance'), ['year', 'multi3']];

# Rename attendance columns to year and attendance.
attendance.columns = ['year', 'attendance'];

# Filter the attendance column to become numeric.
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[:, 'attendance']);

# Plot attendance.
attendance.plot(x='year', y='attendance', figsize=(15,7), kind='bar');

# Add plot metadata.
plt.xlabel('Year');
plt.ylabel('Attendance');
plt.axhline(y=attendance['attendance'].mean(), label='Mean', linestyle='-', color='Green');

# Show the plot.
plt.show();

