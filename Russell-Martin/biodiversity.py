
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[1]:


import pandas as pd 
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[2]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[3]:


species.head(10)


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[4]:


len(species)


# What are the different values of `category` in `species`?

# In[5]:


species['category'].unique().tolist()


# What are the different values of `conservation_status`?

# In[6]:


species['conservation_status'].unique().tolist()


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currently neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[7]:


species.groupby('conservation_status').count()['scientific_name'].reset_index()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[8]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Intervention`.

# In[9]:


species.groupby('conservation_status').count()['scientific_name'].reset_index()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[10]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')
    
protection_counts


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[11]:


#  Get the data for the bar chart, and the labels too
x = range(len(protection_counts))
y = [protection_counts.values[i][1] for i in x]
labels = [protection_counts.values[i][0] for i in x]

#  Label plotting code adapted from https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart

fig = plt.figure(figsize=(10,4.6))
ax = plt.subplot()
plt.bar(x,y)
rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label. 
    space = 1.1
    # Vertical alignment for positive values
    va = 'bottom'

    # Use Y value as label and format number with one decimal place
    label = "{:.0f}".format(y_value)

    # Create annotation
    plt.annotate(
        label,                     # Use `label` as label
        (x_value, y_value),        # Place label at end of the bar
        xytext=(0, space),         # Vertically shift label by `space`
        textcoords="offset points",# Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        va=va)   
    
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set(title='Conservation Status by Species', ylabel='Number of Species')
plt.savefig('StatusBySpecies.pdf')
plt.show()


# In[12]:


protection_counts.values[:4,1].sum()  #  Species that are threated, endangered, "of concern", and in recovery


# In[13]:


#  Label plotting code adapted from https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart

fig = plt.figure(figsize=(10,4.6))
ax = plt.subplot()
plt.bar(x[:-1],y[:-1])
rects = ax.patches

for rect in rects:
    # Get X and Y placement of label from rect
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label. 
    space = 1
    # Vertical alignment for positive values
    va = 'bottom'

    # Use Y value as label and format number with one decimal place
    label = "{:.0f}".format(y_value)

    # Create annotation
    plt.annotate(
        label,                     # Use `label` as label
        (x_value, y_value),        # Place label at end of the bar
        xytext=(0, space),         # Vertically shift label by `space`
        textcoords="offset points",# Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        va=va)                     

ax.set_xticks(x)
ax.set_xticklabels(labels[:-1])
ax.set(title='Conservation Status by Species', ylabel='Number of Species')
plt.savefig('ProtectedStatusBySpecies.pdf')
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[14]:


species['is_protected'] = species['conservation_status']    .apply(lambda x: True if x != 'No Intervention' else False)


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[15]:


category_counts = species.groupby(['category','is_protected'])['scientific_name']    .count().reset_index()


# Examine `category_count` using `head()`.

# In[16]:


category_counts


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[17]:


category_pivot = category_counts.pivot(index='category', columns='is_protected',values='scientific_name').reset_index()


# Examine `category_pivot`.

# In[18]:


category_pivot


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[19]:


#  Set the index back to 'category' to simplify the look of the table.
category_pivot.set_index('category',inplace=True)

#  Rename the columns by assigning a new list to them
category_pivot.columns = ['not_protected', 'protected']

#  Swap the two columns, as I think it makes it more logical when viewing the table.
category_pivot=category_pivot[['protected','not_protected']]

category_pivot


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[20]:


category_pivot['percent_protected']=round(100*category_pivot['protected']              /(category_pivot['protected']+category_pivot['not_protected']),2)


# Examine `category_pivot`.

# In[21]:


category_pivot


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|total|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[22]:


contingency = category_pivot.loc[['Mammal','Bird']][['protected','not_protected']]
contingency


# In order to perform our chi squared test, we'll need to import the correct function from scipy.  Paste the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[23]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[24]:


chi2, pval, dof, expected = chi2_contingency(contingency)
pval


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[25]:


mammal_reptile = category_pivot.loc[['Mammal','Reptile']][['protected','not_protected']]
mammal_reptile


# In[26]:


chi2, pval, dof, expected = chi2_contingency(mammal_reptile)
pval


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# In[27]:


#  How about birds vs. reptiles?  

bird_reptile = category_pivot.loc[['Bird','Reptile']][['protected','not_protected']]

chi2, pval, dof, expected = chi2_contingency(bird_reptile)
pval


# Ok, "very close" to showing significant difference.  Hard to "split the difference" between Mammal and Reptile vs Bird and Reptile.

# In[28]:


bird_amphibian = category_pivot.loc[['Bird','Amphibian']][['protected','not_protected']]

chi2, pval, dof, expected = chi2_contingency(bird_amphibian)
pval


# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved and sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[29]:


observations = pd.read_csv('observations.csv')
observations.head(10)


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  
# 
# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[30]:


species['is_sheep'] = species['common_names'].apply(lambda x: 'Sheep' in x)


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[31]:


species[species.is_sheep]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[32]:


sheep_species = species[ species.is_sheep & (species.category == 'Mammal') ]
sheep_species


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[33]:


#  Do a left merge on sheep_species with observations on the 'scientific_name' column. 
sheep_observations = sheep_species.merge(observations, how='left', on='scientific_name').drop(['category','is_sheep'], axis=1)

sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[34]:


obs_by_park = sheep_observations.groupby('park_name').sum().drop('is_protected',axis=1)
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[35]:


#  Label plotting code adapted from https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart

x = range(len(obs_by_park))
y = obs_by_park['observations'].values
labels = obs_by_park.index.values

fig = plt.figure(figsize=(12,5))
ax = plt.subplot()
plt.bar(x,y)
rects = ax.patches

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set(ylabel='Number of Observations', title='Observations of Sheep per Week')

for rect in rects:
    # Get X and Y placement of label from rect
    y_value = rect.get_height()
    x_value = rect.get_x() + rect.get_width() / 2

    # Number of points between bar and label. 
    space = 1.1
    # Vertical alignment for positive values
    va = 'bottom'

    # Use Y value as label and format number with one decimal place
    label = "{:.0f}".format(y_value)

    # Create annotation
    plt.annotate(
        label,                     # Use `label` as label
        (x_value, y_value),        # Place label at end of the bar
        xytext=(0, space),         # Vertically shift label by `space`
        textcoords="offset points",# Interpret `xytext` as offset in points
        ha='center',               # Horizontally center label
        va=va)                     
    
plt.savefig('SheepObservations.pdf')
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# ## Note:  I'm assuming the 15% infection rate acrosss all parks, as this isn't explicitly specified that's the case in the text above.

# In[36]:


significance = 0.90
baselineRate = 0.15                   #  infection rate of 15%
minDetectableEffect = 0.05/0.15*100   #  drop of 5% from a rate of 15%

minDetectableEffect


# In[37]:


sampleSizeNeeded = 510    # from Optimizely with significance, baselineRate, and minDetectableEffect as above


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[38]:


weeksAtBryce = sampleSizeNeeded/obs_by_park.loc['Bryce National Park','observations']
weeksAtBryce


# ### Slightly more than two weeks at Bryce National Park.

# In[39]:


weeksAtYellowstone = sampleSizeNeeded/obs_by_park.loc['Yellowstone National Park','observations']
weeksAtYellowstone


# ### About one week at Yellowstone National Park.
