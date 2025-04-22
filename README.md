# Youtube Channel Performance Analysis
**Overview** 

This project is focusing on analysing the performance of Youtube content using metadata exported from a personal channel. The data was cleaned. categorised, and converted from Excel to SQLite format for structured querying and future analysis. 

**Objectives**
- Identify which video genres perform best in terms of views, watch time, and subscriber gain
- Analyse the impact of publish day on video performance
- Explore the relationship between video duration and engagement metrics
- Examine how impressions and CTR influence actual view counts
- Establish a performance baseline to cokmpare with a follow-up analysis after 6 months
- Derive actionable insights to guide content planning and posting strategies
  
**Tools Used**
- Excel
- DB Browser for SQLite
- Terminal to commit&push




# Metadata Description
The initial metadata is an Excel file which has exported from Youtube. Metadata was transformed into .db format, enabling performance analysis in DB Browser.

- ContentID: A unique identifier assigned to each Youtube video
- Title: The name of the video
- Genre: The type or category of the video content (e.g., flat life, nz vlog, kr vlog, travel)
- Video Publish Date: The date when the video was published on Youtube
- Watch Time: The total amount of time viewers have spent watching the video (in seconds, will be transforming mm:ss format on SQLite)
- Subscribers: The number of subscribets gained from the video
- Impressions: The number of times the video thumbnail was shown to viewers
- Impressions click-through rate (%): The percentage of impressions that resulted in views (i.e., how often viewers clicked after seeing the thumbnail)

**About my Youtube Channel**
This meta data was collected from my own Youtube Channel 'BinnieBae' which means this is not a fictional data. 
I am very welcome if you visit my channel! Enjoy🎥 https://www.youtube.com/@BaEbAe417
