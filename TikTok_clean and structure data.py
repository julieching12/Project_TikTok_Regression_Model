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

# Import packages for data manipulation
import pandas as pd
import numpy as np

# Import packages for data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset into dataframe
data = pd.read_csv("tiktok_dataset.csv")

# Display and examine the first few rows of the dataframe
data.head()

# Get the size of the data
data.size

# Get the shape of the data
data.shape

# Get basic information about the data
data.info()

# Generate a table of descriptive statistics
data.describe()

# Create a boxplot to visualize distribution of `video_duration_sec`
plt.figure(figsize=(5, 1))
sns.boxplot(data=data, x='video_duration_sec', showfliers=True)  #mine, seems no outliers for this variable
#sns.boxplot(x=data['video_duration_sec'])  #exemplar
plt.title('Distribution of Video Duration Sec')

# Create a histogram
plt.figure(figsize=(6, 2))
sns.histplot(data['video_duration_sec'],bins=range(0,61,5))
plt.title('Video Duration Histogram')

# Create a boxplot to visualize distribution of `video_view_count`
plt.figure(figsize=(5, 1))
sns.boxplot(x=data['video_view_count'], showfliers=True)
plt.title('Distribution of Video View Count')

# Create a histogram
plt.figure(figsize=(6, 2))
#sns.histplot(data['video_view_count'], bins=range(0, 1000000+1, 100000)) #xaxis unit is 1000000
sns.histplot(data['video_view_count'], bins=range(0, 10**6+1, 10**5)) #xaxis unit is 1e6
plt.title('Video View Histogram')

# Create a boxplot to visualize distribution of `video_like_count`
plt.figure(figsize=(10, 1))
sns.boxplot(data['video_like_count'], showfliers=True)
plt.title('Distribution of Video Like Count')

# Create a histogram
plt.figure(figsize=(10, 3))
ax = sns.histplot(data['video_like_count'], bins=range(0,7*10**5+1,10**5))
ax.set_xticks(range(0,7*10**5+1,10**5))
ax.set_xticklabels([0] + [str(i) + 'k' for i in range(100,701,100)])
plt.title('Video Like Count Histogram')

# Create a boxplot to visualize distribution of `video_comment_count`
plt.figure(figsize=(10, 1))
sns.boxplot(data['video_comment_count'], showfliers=True)
plt.title('Distribution of Video Comment Count')

# Create a histogram
plt.figure(figsize=(5, 3))
ax = sns.histplot(data['video_comment_count'], bins=range(0,10**4+1,10**3))
ax.set_xticks(range(0,10**4+1,10**3))
ax.set_xticklabels([0] + [str(i) + 'k' for i in range(1,10,1)])
plt.title('Video Comment Count Histogram')

# Create a boxplot to visualize distribution of `video_share_count`
plt.figure(figsize=(10, 1))
sns.boxplot(data['video_share_count'], showfliers=True)
plt.title('Distribution of Video Share Count')

# Create a histogram
plt.figure(figsize=(6, 3))
sns.histplot(data['video_share_count'], bins=range(0, 270001, 10000)) #xaxis unit is 1e6
plt.title('Video Share Histogram')

# Create a boxplot to visualize distribution of `video_download_count`
plt.figure(figsize=(10, 1))
sns.boxplot(data['video_download_count'], showfliers=True)
plt.title('Distribution of Video Download Count')

# Create a histogram
plt.figure(figsize=(10, 3))
sns.histplot(data['video_download_count'], bins=range(0, 15001, 500)) #xaxis unit is 1e6
plt.title('Video Download Histogram')

# Create a histogram
plt.figure(figsize=(7, 4))
sns.histplot(data=data,x='claim_status',hue='verified_status',multiple='dodge',shrink=0.9)
plt.title('Claims by Verification Status Histogram')

# Create a histogram
plt.figure(figsize=(7, 4))
sns.histplot(data=data,x='claim_status',hue='author_ban_status',multiple='dodge',shrink=0.9,
             hue_order=['active','under review','banned'],
            palette={'active':'green','under review':'orange','banned':'red'},
            alpha=0.5)      #alpha is transparent rate
plt.title('Claims by Author Ban Status Histogram')

# Create a bar plot
#ban_status_median_view = data.groupby(['author_ban_status']).median()[['video_view_count']]  #this not work when rendering plot

ban_status_median_view = data.groupby(['author_ban_status']).median(
   numeric_only=True).reset_index()   #has to be like this a tabular format data
fig = plt.figure(figsize=(5,3))
sns.barplot(data=ban_status_median_view,
            x='author_ban_status',
            y='video_view_count',
            order=['active', 'under review', 'banned'],
            palette={'active':'green', 'under review':'orange', 'banned':'red'},
            alpha=0.5)
plt.title('Median View Counts by Ban Status')

# Calculate the median view count for claim status.
data.groupby('claim_status')['video_view_count'].median()

data.groupby('claim_status')['video_view_count'].mean()

# Create a pie graph
total_view_claim_status = data.groupby(['claim_status'])[['video_view_count']].sum()
#total_view_claim_status
plt.figure(figsize=(3,3))
plt.pie(data=total_view_claim_status, x='video_view_count',labels=['claim', 'opinion'])
plt.title('Total Views by Video Claim Status')

# Determine outliers
counts = ['video_view_count','video_like_count','video_share_count','video_download_count','video_comment_count']
number_of_outliers = {}
for i in counts:
    median = data[i].median()
    percentile25 = data[i].quantile(0.25)
    percentile75 = data[i].quantile(0.75)
    iqr = percentile75 - percentile25
    outlier_threshold = median + 1.5 * iqr
    #outliers_threshold[i] = outlier_threshold   #the threshold is not outliers
    outlier_count = (data[i] > outlier_threshold).sum() #when data[i] series values greater than threshold
    number_of_outliers[i] = outlier_count

print("Number of outliers for each count: ")
#number_of_outliers

# Create a scatterplot of `video_view_count` versus `video_like_count` according to 'claim_status'
sns.scatterplot(x=data['video_view_count'], y=data['video_like_count'],hue=data['claim_status'],s=10,alpha=0.3)
plt.show()

# Create a scatterplot of ``video_view_count` versus `video_like_count` for opinions only
opinions_only = data[data['claim_status'] == 'opinion']
sns.scatterplot(x=opinions_only['video_view_count'], y=opinions_only['video_like_count'],s=10,alpha=0.3)
plt.show()
