import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize connection to Google Trends
pytrends = TrendReq(hl='en-US', tz=360)

# Define keywords and build payload
keywords = ["Electric Cars", "Hybrid Cars", "Gasoline Cars"]
pytrends.build_payload(kw_list=keywords, cat=0, timeframe='today 5-y', geo='IN', gprop='')

# Fetch interest over time
data = pytrends.interest_over_time()

# Check if data is returned
if not data.empty:
    data.reset_index(inplace=True)
    print(data.head())
else:
    print("No data available for the specified keywords or timeframe.")

# Fetch interest by region
region_data = pytrends.interest_by_region()

# Check if region data is returned
if not region_data.empty:
    region_data = region_data.sort_values(by='Electric Cars', ascending=False).head(10)
    print(region_data)
else:
    print("No regional data available.")

# Fetch top charts
try:
    top_charts = pytrends.top_charts(2023, hl='en-US', tz=360, geo='GLOBAL')
    print(top_charts.head(10))
except Exception as e:
    print(f"Error fetching top charts: {e}")

# Fetch related queries with error handling
try:
    related_queries = pytrends.related_queries()
    if related_queries:
        print(related_queries)
    else:
        print("No related queries found for the specified keywords.")
except (IndexError, KeyError) as e:
    print(f"Error fetching related queries: {e}")

# Plot search trends over time
if not data.empty:
    plt.figure(figsize=(10, 5))
    for keyword in keywords:
        plt.plot(data['date'], data[keyword], label=keyword)
    plt.title('Search Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Search Interest')
    plt.legend()
    plt.show()

# Plot regional interest data
if not region_data.empty:
    region_data.reset_index(inplace=True)
    sns.barplot(x='geoName', y='Electric Cars', data=region_data)
    plt.title('Search Interest by Region')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("No regional data available to plot.")