"""
The purpose of this project is to investigate and understand the data provided. This activity will:
1.Acquaint you with the data
2.Compile summary information about the data
3.Begin the process of EDA and reveal insights contained in the data
4.Prepare you for more in-depth EDA, hypothesis testing, and statistical analysis

The goal is to construct a dataframe in Python, perform a cursory inspection of the provided dataset,
and inform TikTok data team members of your findings.

NOTE: below codes are run in Jupyter Notebook environment.
"""

# Import packages
import pandas as pd
import numpy as np

# Load dataset into dataframe
data = pd.read_csv("tiktok_dataset.csv")

# Display and examine the first ten rows of the dataframe
data.head(10)

# Get summary info
data.info()

# Get summary statistics
data.describe()

# What are the different values for claim status and how many of each are in the data?
data['claim_status'].value_counts()

# Start by using Boolean masking to filter the data according to claim status, then calculate the mean and median view
# counts for each claim status.
# What is the average view count of videos with "claim" status?
mean_view_count = data[data['claim_status'] == 'claim']['video_view_count'].mean()
print(mean_view_count)
median_view_count = data[data['claim_status'] == 'claim']['video_view_count'].median()
print(median_view_count)

# What is the average view count of videos with "opinion" status?
mean_view_count = data[data['claim_status'] == 'opinion']['video_view_count'].mean()
print(mean_view_count)
median_view_count = data[data['claim_status'] == 'opinion']['video_view_count'].median()
print(median_view_count)

# Get counts for each group combination of claim status and author ban status
data.groupby(['claim_status', 'author_ban_status']).count()[['#']]

# Calculate the median video share count of each author ban status
data.groupby(['author_ban_status'])[['video_share_count']].median()

# What's the median video share count of each author ban status?
#data.groupby('author_ban_status')[['video_share_count']].median()
data.groupby(['author_ban_status']).median(numeric_only=True)[['video_share_count']]

# Use groupby() to group the data by author_ban_status, then use agg() to get the count, mean, and median for these 3
# columns.
data.groupby(['author_ban_status']).agg(
    {'video_view_count': ['count', 'mean', 'median'],
     'video_like_count': ['count', 'mean', 'median'],
     'video_share_count': ['count', 'mean', 'median']}
    )

# Create a likes_per_view column
data['likes_per_view'] = data['video_like_count'] / data['video_view_count']

# Create a comments_per_view column
data['comments_per_view'] = data['video_comment_count'] / data['video_view_count']

# Create a shares_per_view column
data['shares_per_view'] = data['video_share_count'] / data['video_view_count']

# Compile the information in each of the three newly created columns for each combination of categories of claim status
# and author ban status, and calculate the count, the mean, and the median of each group.
data.groupby(['claim_status', 'author_ban_status']).agg(
    {'likes_per_view': ['count', 'mean', 'median'],
     'comments_per_view': ['count', 'mean', 'median'],
     'shares_per_view': ['count', 'mean', 'median']}
    )

