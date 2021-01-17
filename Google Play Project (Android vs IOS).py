#!/usr/bin/env python
# coding: utf-8

# In[1]:


from csv import reader

# The Google Play data set 
opened_file = open('googleplaystore.csv', encoding="utf8")
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

# The App Store data set
opened_file = open('AppleStore.csv', encoding="utf8")
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[2]:


#function to explore slices of of our data set, or a range of rows, also totaling number of items in one list 'columns', and number of rows total in the dataset
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


print(android_header)
print('\n')
explore_data(android, 0, 4, True)


# In[4]:


print(ios_header)
print('\n')
explore_data(ios, 0, 4, True)


# In[5]:


#our peers have informed us that row 10472 is missing information, and we would like to detect this row and check, function below finds rowss that don't have the same number of items and the header
#and we would like to compare this row to a normal row, and the header
for row in android:
    if len(row) != len(android_header):
        print(android.index(row))
        print(android[10472])
        print(android_header)
        print(android[5])


# In[6]:


#deleting the row with the missing information (missing 'category') so this does not cause errors with our analysis later on
print(len(android))
del android[10472]
print(len(android))


# In[7]:


#identifying if there are duplicate rows for speciifc apps

unique_apps = []
duplicate_apps = []

for row in android:
    app_name = row[0]
    
    if row[0] in unique_apps:
        duplicate_apps.append(app_name)
        
    else: 
        unique_apps.append(app_name)
    
print('Number of Duplicate Entries:' , len(duplicate_apps))
print('\n')
print('Example of Duplicate Entreies:' , duplicate_apps[:10])
      
#We won't remove the duplicates randomly, rather we will keep the one app entry with the highest # of reviews
      


# In[8]:


print('Expected Number of Entries:' , len(android) - 1181)


# In[9]:


#creating dictionary containing app names with only its highest ratings (thus minusing the duplicates)
reviews_max = {}

for row in android:
    name = row[0]
    n_reviews = float(row[3])

    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print(len(reviews_max))
print(reviews_max)


# In[10]:


#we use the dictionary we created above to grab the apps with those ratings from our original dataset, and we use an 'already_added' list as a check system to make sure we don't have duplicate app entries
android_clean = []
already_added = [] #we need this for the apps that have duplicate high ratings

for row in android:
    name = row[0]
    n_reviews = float(row[3])
   
    if reviews_max[name] == n_reviews and name not in already_added: 
        android_clean.append(row)
        already_added.append(name)
        
print(len(android_clean))


# In[11]:


explore_data(android_clean ,0 ,4 ,True)


# In[12]:


#defining a function that checks a strings character to make sure the characters are in english
#character under 127 ascii are considered english characters, ord() function allows us to check the character's ascii value
def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False
    
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# In[13]:


#allowing strings with up to 3 characters over 127 ascii to pass as english - not perfectly accurate function to define english apps but will do for now
def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    
    else:
        return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# In[14]:


android_english = []
ios_english = []

for row in android_clean:
    if is_english(row[0]):
        android_english.append(row)
        
for row in ios:
    if is_english(row[1]):
        ios_english.append(row)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# In[15]:


#creating a new final list of adroid and ios apps to analyze with only free apps
android_free = []
ios_free = []

for row in android_english:
    price = row[7]
    
    if price == '0':
        android_free.append(row)
        
for row in ios_english:
    price = row[4]
    
    if price == '0.0':
        ios_free.append(row)
        
print(len(android_free))
print(len(ios_free))


# In[16]:


#creating a function that creates a frequency table for chosen index from our dataset and then turn them into 
#percentage values
def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage
    
    return table_percentages 

#takes the percent frequency table created above and converts it into a list of tuples, with value number before the key, 
#in order to sort the list, then reversing the positions when printing our final table
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[17]:


#iOS percent by genre
display_table(ios_free, 11)


# In[18]:


#Based on the percent frequency table above, we can see that for our english apps, more than half are games (58.16%)
#According to information we've collected, entertainment apps are used far more that productivity apps on the App Store


# In[19]:


#Android percent by category
display_table(android_free, 1)


# In[20]:


###Info above shows that google play has far less game representation than the App Store, there are more 'practicial' apps in Google Play relative to the App Store
###There are still a large majority of games on Google Play. The 'Family' genre constitues of mostly games


# In[21]:


#Android percent by genre
display_table(android_free, 9)


# In[22]:


#Apps by genre paint the same story. There are far more practical apps to entertainment apps in google play relative to the app store (ie. tools, educations, business, producitivty, lifestlye, finance, etc.)
#There is a more even distribution of app categories in google play than the app store. Let's look at # of downloads info next!


# In[23]:


#nested for loop below alows us to calculate the average rating count (index 5 in iOS free) based on genre
genres_ios = freq_table(ios_free, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    
    for app in ios_free:
        genre_app = app[-5]
        if genre_app == genre:
            rating_tot = float(app[5])
            total += rating_tot
            len_genre += 1
    
    avg_genre_rating = total / len_genre    
    print(genre, ":", avg_genre_rating)


# In[24]:


#Navigation, Reference, and Social Networking have the highest average user rating in the app store, but not sure if this is a KPI for the types of apps we want to focus on for our goal of developing new day to day user apps


# In[25]:


display_table(android_free, 5) #number of installs column in google play data


# In[32]:


#creating function to calculate average installs by genre. We used the replace method to convert installs string into a float. Our install numbers are not percise but it will do for this exercise
categories_android = freq_table(android_free, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_free:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[37]:


#Let's take a look at the highest installed communication apps, since communication apps have the most average installs
for app in android_free:
    if app[1] == 'COMMUNICATION'and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ":", app[5])


# In[38]:


#These apps with huge installs skews the average installs for communication apps, and these are giants that are difficult to compete with


# In[39]:


#Let's take a look at 'NEWS_AND_MAGAZINES' and few other popular categories. We will pull out apps with the higest number of installs


# In[40]:


for app in android_free:
    if app[1] == 'NEWS_AND_MAGAZINES'and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ":", app[5])


# In[43]:


for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE'and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ":", app[5])


# In[44]:


#one more
for app in android_free:
    if app[1] == 'GAME'and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ":", app[5])


# In[46]:


#Lets look in these same categories, but with a more average number of installs
for app in android_free:
    if app[1] == 'NEWS_AND_MAGAZINES'and (app[5] == '50,000,000+' or
                                          app[5] == '10,000,000+' or
                                          app[5] == '5,000,000+' or
                                          app[5] == '1,000,000+'):
        print(app[0], ":",app[5])
                                        


# In[48]:


for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE'and (app[5] == '50,000,000+' or
                                          app[5] == '10,000,000+' or
                                          app[5] == '5,000,000+' or
                                          app[5] == '1,000,000+'):
        print(app[0], ":",app[5])


# In[50]:


for app in android_free:
    if app[1] == 'GAME'and (app[5] == '50,000,000+' or
                                          app[5] == '10,000,000+' or
                                          app[5] == '5,000,000+' or
                                          app[5] == '1,000,000+'):
        print(app[0], ":",app[5])


# In[ ]:


#we have simple code above to extract apps with and high and mid number of installs. We can see that for books and referenes, there still only a few high installs so perhaps there is potential there.
#We can also look into the other categories and choose to make app with similarties to our mid to higher installed products because of there likeability and features

