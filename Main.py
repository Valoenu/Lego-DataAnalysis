# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML

# Display introductory image
display(HTML('<img src="https://i.imgur.com/49FNOHj.jpg">'))

# ===============================
# Load and Explore Colors Dataset
# ===============================

# Load the colors dataset which contains information about LEGO colors
colors = pd.read_csv('data/colors.csv')

# Display first few rows of the dataset
colors.head()

# Check how many unique color names exist in the dataset
colors['name'].nunique()

# Group by transparency status and count the number of each
colors.groupby('is_trans').count()

# Alternatively, use value_counts() for a quicker transparency distribution
colors['is_trans'].value_counts()

# ===============================
# Markdown Explanation of Themes & Sets
# ===============================
# This section describes the concept of LEGO themes vs sets
display(HTML("""
<h4>Understanding LEGO Themes vs. LEGO Sets</h4>
<p>Walk into a LEGO store and you’ll see their products organised by theme. These include Star Wars, Batman, Harry Potter, and many more.</p>
<img src="https://i.imgur.com/aKcwkSx.png">
<p>A LEGO <strong>set</strong> is a specific product box sold under a theme. A single theme often contains many sets.</p>
<img src="https://i.imgur.com/whB101g.png">
"""))

# ===============================
# Load and Explore Sets Dataset
# ===============================

# Load LEGO sets data which includes set name, year, number of parts, theme_id, etc.
sets = pd.read_csv('data/sets.csv')

# Check dimensions of the dataset
sets.shape

# Display first and last few records
sets.head()
sets.tail()

# Find top 5 LEGO sets with the most parts
sets.sort_values('num_parts', ascending=False).head(5)

# Explore which year LEGO started releasing sets
sets.sort_values('year').head()

# Find all products released in the first year (1949)
sets[sets['year'] == 1949]

# =======================================
# Visualize Number of LEGO Sets per Year
# =======================================

# Group data by release year and count how many sets released each year
sets_by_year = sets.groupby('year').count()

# Plot number of sets per year (excluding the last 2 years with incomplete data)
plt.plot(sets_by_year.index[:-2], sets_by_year.set_num[:-2])
plt.title("Number of LEGO Sets Released Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Sets")
plt.grid(True)
plt.show()

# ========================================
# Analyze Number of Unique Themes per Year
# ========================================

# Group by year and count number of unique themes
themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})

# Rename the column for clarity
themes_by_year.rename(columns={'theme_id': 'themes_number'}, inplace=True)

# Plot number of themes per year
plt.plot(themes_by_year.index[:-2], themes_by_year.themes_number[:-2])
plt.title("Number of Unique LEGO Themes by Year")
plt.xlabel("Year")
plt.ylabel("Number of Themes")
plt.grid(True)
plt.show()

# ===================================
# Dual Axis Plot: Sets vs. Themes
# ===================================

# Create a dual-axis chart comparing number of sets and themes over time
ax1 = plt.gca()                      # Get current axis
ax2 = ax1.twinx()                    # Create a twin axis sharing the same x-axis

# Plot sets on left axis (green)
ax1.plot(sets_by_year.index[:-2], sets_by_year.set_num[:-2], color='green', label='Number of Sets')
ax1.set_ylabel('Number of Sets', color='green')

# Plot themes on right axis (blue)
ax2.plot(themes_by_year.index[:-2], themes_by_year.themes_number[:-2], color='blue', label='Number of Themes')
ax2.set_ylabel('Number of Themes', color='blue')

# Labels and title
ax1.set_xlabel('Year')
plt.title("LEGO Sets and Themes Released Over Time")
plt.show()

# =======================================
# Average Number of Parts per Set by Year
# =======================================

# Calculate the average number of parts per set grouped by year
parts_per_set = sets.groupby('year').agg({'num_parts': pd.Series.mean})

# Scatter plot to visualize trends over time
plt.scatter(parts_per_set.index[:-2], parts_per_set.num_parts[:-2])
plt.title("Average Number of Parts per LEGO Set")
plt.xlabel("Year")
plt.ylabel("Average Number of Parts")
plt.grid(True)
plt.show()

# ==================================================
# Determine Which Theme Has the Most LEGO Sets
# ==================================================

# Count how many sets exist for each theme ID
theme_set_count = sets['theme_id'].value_counts()

# Display the top 5 themes with most sets
theme_set_count.head()

# Display schema explanation
display(HTML('<img src="https://i.imgur.com/Sg4lcjx.png">'))

# ===============================
# Load Themes Dataset
# ===============================

# Load theme names and IDs from the themes dataset
themes = pd.read_csv('data/themes.csv')
themes.head()

# Check how many different IDs exist for the 'Star Wars' name
themes[themes.name == 'Star Wars']

# View all sets that belong to theme ID 158 (Star Wars)
sets[sets.theme_id == 158]

# ==================================================
# Merge Theme Names with Set Counts for Visualization
# ==================================================

# Convert the theme count Series to a DataFrame for merging
theme_set_count_df = pd.DataFrame({
    'id': theme_set_count.index,
    'set_count': theme_set_count.values
})

# Merge theme names using 'id' as the key
merged_df = pd.merge(theme_set_count_df, themes, on='id')

# ==================================
# Bar Chart: Top 10 Most Common Themes
# ==================================

# Plot the top 10 themes with most sets
plt.figure(figsize=(15,7))
plt.bar(merged_df.name[:10], merged_df.set_count[:10])
plt.xlabel('Theme Name', fontsize=12)
plt.ylabel('Number of Sets', fontsize=12)
plt.title('Top 10 LEGO Themes by Number of Sets')
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()
