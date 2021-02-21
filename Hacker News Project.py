#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Hacker News Project through Data Quest
#Opened file and read as list

opened_file = open('HN_posts_year_to_Sep_26_2016.csv', encoding="utf8")
from csv import reader
read_file = reader(opened_file)
hn = list(read_file)
print(hn[:5])


# In[2]:


#Separated header row from data

headers = hn[0]
hn = hn[1:]
print(headers)
print('\n')
print(hn[0:5])


# In[3]:


#separating specific data, looking at post title starting with 'ask hn' and 'show hn'

ask_post = []
show_post = []
other_post = []
for row in hn:
    title = row[1]
    
    if title.lower().startswith('ask hn'):
        ask_post.append(row)
    if title.lower().startswith('show hn'):
        show_post.append(row)
    else:
        other_post.append(row)
        
print('Total Ask Hn Post:' , len(ask_post))
print('Total Show Hn Post:' , len(show_post))
print('Total Other Hn Post:' , len(other_post))
print(ask_post[:5])


# In[4]:


#finding number of comments and average comments per post specifically for 'ask hn' posts and 'show hn' posts

total_ask_comments = 0
for row in ask_post:
    num_comments = int(row[4])
    total_ask_comments += num_comments
    avg_ask_comments = total_ask_comments / len(ask_post)
print('Total Ask Comments:' , total_ask_comments)
print('Average Ask Comments', avg_ask_comments)

total_show_comments = 0
for row in show_post:
    num_comments = int(row[4])
    total_show_comments += num_comments
    avg_show_comments = total_show_comments / len(show_post)
print('Total Show Comments:' , total_show_comments)
print('Average Show Comments', avg_show_comments)
    
#looks like 'Ask Hn' gets a little over twice as many comments as "Show Hn" posts. "Ask Hn" posts gets an average of 10.39 comments per post


# In[5]:


#converted dates to months using strptime/strftime and used them as keys in a dictionary to calculate total number of posts
#and comments.

import datetime as dt
results_list = []
for row in ask_post:
    created_at = row[6]
    num_comments = int(row[4])
    results_list.append([created_at,num_comments])
    
counts_by_hours = {}
comments_by_hours = {}
date_format = "%m/%d/%Y %H:%M"
for row in results_list:
    entry_datetime = row[0]
    num_comments = row[1]
    hour = dt.datetime.strptime(entry_datetime , date_format).strftime("%H")
    
    if hour not in counts_by_hours:
        counts_by_hours[hour] = 1
        comments_by_hours[hour] = num_comments
    else:
        counts_by_hours[hour] += 1
        comments_by_hours[hour] += num_comments
    
print(counts_by_hours)
print('\n')
print(comments_by_hours)

    


# In[8]:


#finding average comments per post in each hour

avg_by_hour = []
for hour in comments_by_hours:
    avg_by_hour.append([hour, comments_by_hours[hour] / counts_by_hours[hour]])

print('\n')
print('Average comments per hour')
print('-------------------------')
for row in avg_by_hour:
    hour = row[0]
    avg = row[1]
    print(hour, ':', round(avg, 2))


# In[24]:


#find top 5 hours of the day when comments per post is highest
#first swapping the elements in our list so that avg comments per hour comes first and then sorting
#then formatting our datetime object and printing in a readable format

swap_avg_by_hour = []
for row in avg_by_hour:
    hour = row[0]
    avg_comment = row[1]
    swap_avg_by_hour.append([avg_comment, hour])
print(swap_avg_by_hour)

sorted_swap = sorted(swap_avg_by_hour, reverse = True)
print('\n')
print(sorted_swap[:5])
print('\n')

print('Top 5 Hours (Highest Comments per Post)')
print('--------------------------------------')
time_format = '%H'
for row in sorted_swap[0:5]:
    avg_comments = row[0]
    hour = row[1]
    hour_formatted = dt.datetime.strptime(hour, time_format).strftime('%H:%M')
    print(hour_formatted, ':', '{:.2f}'.format(avg_comments))


# In[ ]:


#Base on our results posts on Hacker Rank get the most comments per post at 3pm, 1pm, and noon in that order then 2am and 10am.
#3pm is peak hour for comments per post by far
#We can say comment traffic is highest in the early afternoon time especially between 3pm-4pm
#It would be interesting to see what days of the week get the most comments per post

