
#%%
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np

#===== STEP 1 & 2 Functions =====
def get_data_from_json(url): 
    with open(url, 'r') as f:
        return json.load(f)
     
def convert_to_datetime_obj(timestamp_str):
    #converting without time (only date)
    if(len(timestamp_str) < 11):
         return datetime.strptime(timestamp_str, '%Y-%m-%d')
    #converting with time and date
    else:
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

def calculate_fraction_of_followers(influencer1, influencer2, all_data):
    reference_date = '2022-04-30'
    reference_date_obj = convert_to_datetime_obj(reference_date)
    followers_set = set()
    shared_followers = 0
    influencer1_followers = 0
    influencer2_followers = 0

    for data in all_data:
        
        #if timestamp is incorrect OR influencer_uid doesn't match influencer1 and influencer2, continue
        if(convert_to_datetime_obj(data['follow_timestamp'][0:10]) > reference_date_obj or data['influencer_uid'] != influencer1 and data['influencer_uid'] != influencer2):
            continue 
        
        #checking if shared follower
        if(data['follower_uid'] in followers_set):
            shared_followers += 1  
        else:
            followers_set.add(data['follower_uid'])

        #counting influencer followers so we can check for least followers at end
        if(data['influencer_uid'] == influencer1):
                influencer1_followers += 1
        else:
                influencer2_followers += 1
    
    least_followers = min(influencer1_followers, influencer2_followers)

    #prevent division by 0 if least followers is 0
    if(least_followers == 0):
         return 0
    else:
        return shared_followers / least_followers
    
def calculate_fraction_of_engangers(influencer1, influencer2, all_data):
    reference_date_lower_bound = convert_to_datetime_obj('2022-04-22')
    reference_date_upper_bound = convert_to_datetime_obj('2022-04-30')
    engagers_set = set()
    shared_engagers = 0
    influencer1_engagers = 0
    influencer2_engagers = 0

    for data in all_data:

        engaged_dt = convert_to_datetime_obj(data['engaged_dt'])
        
        #if timestamp is incorrect OR influencer_uid doesn't match influencer1 and influencer2, continue
        if(engaged_dt < reference_date_lower_bound and engaged_dt > reference_date_upper_bound or data['influencer_uid'] != influencer1 and data['influencer_uid'] != influencer2):
            continue 
        
        #checking if shared engager
        if(data['follower_uid'] in engagers_set):
            shared_engagers += 1  
        else:
            engagers_set.add(data['follower_uid'])

        #counting influencer engagers so we can check for least engagers at end
        if(data['influencer_uid'] == influencer1):
                influencer1_engagers += 1
        else:
                influencer2_engagers += 1
    
    least_engagers = min(influencer1_engagers, influencer2_engagers)

    #prevent division by 0 if least followers is 0
    if(least_engagers == 0):
         return 0
    else:
        return shared_engagers / least_engagers

#===== STEP 3 Functions =====

def create_influencer_map(all_data):

    m = {} #key: influencer_uid => val: [followers]

    for data in all_data:
        if(data["influencer_uid"] in m):
            m[data["influencer_uid"]].append(data["follower_uid"])
        else:
            m[data["influencer_uid"]] = []
    
    return m
     
def get_overlap(influencers_map):
    overlap_arr = []
    influencers_arr = list(influencers_map.keys())

    #loop through all the influencers and compare each pair of influencers
    for i in range(len(influencers_arr)):
        for j in range(i+1, len(influencers_arr)):
            for follower in influencers_map[influencers_arr[i]]:
                #check if the follower is shared between the two influencers
                if(follower in influencers_map[influencers_arr[j]]):
                    #if follower is shared, append the follower to overlap_arr
                    overlap_arr.append(int(follower))
    
    return overlap_arr     

def plotHistogram(data):
     plt.hist(data)
     plt.show()

#===== STEP 5 Functions =====
def perform_and_plot_OLS_regression(network_overlap, engagers_overlap):
     
    # Create a Pandas DataFrame
    df = pd.DataFrame({'network_overlap': network_overlap, 'engagers_overlap': engagers_overlap})

    # Perform OLS Regression
    x = sm.add_constant(df['network_overlap'])
    y = df['engagers_overlap']
    model = sm.OLS(y, x).fit()

    # Regression Summary
    print(model.summary())

    # Scatter Plot
    plt.scatter(df['network_overlap'], df['engagers_overlap'], alpha=0.5)
    plt.xlabel('Network overlap')
    plt.ylabel('Engagement overlap')

    # Line Plot of Predicated Values from Model
    x_pred = np.linspace(df['network_overlap'].min(), df['network_overlap'].max(), 100)
    x_pred2 = sm.add_constant(x_pred)
    y_pred = model.predict(x_pred2)
    plt.plot(x_pred, y_pred, color='red')
   

def main():

    #===== STEP 1 & 2 =====

    influencer1 = "902200087" #sample influencer ids for testing
    influencer2 = "969221141347913734"

    following_data = get_data_from_json('datasets/following.json')
    engagement_data = get_data_from_json('datasets/engagement.json')

    fraction_of_followers = calculate_fraction_of_followers(influencer1, influencer2, following_data)
    fraction_of_engagers = calculate_fraction_of_engangers(influencer1, influencer2, engagement_data)
    
    print(f'Fraction of followers over total followers of the less follower influencer is: {fraction_of_followers}')
    print(f'Fraction of engagers over total engagers of the less engaged influencer is: {fraction_of_engagers}')
    
    #===== STEP 3 =====

    followers_map = create_influencer_map(following_data)
    engagers_map = create_influencer_map(engagement_data)

    all_network_overlap = get_overlap(followers_map) #this function takes too long to run due to the nature of the datasets, use some test data
    all_engagers_overlap = get_overlap(engagers_map) #this function takes too long to run due to the nature of the dataset, use some test data

    # Plotting histograms
    plotHistogram(all_network_overlap)
    plotHistogram(all_engagers_overlap)

    #===== STEP 5 =====

    #performing OLS regression
    perform_and_plot_OLS_regression(all_network_overlap, all_engagers_overlap)

    #===== STEP 6 =====

    # Since I was unable to run the plots with the provided data due to the datasets
    # being too large and the code taking too long to execute, I used test data and from
    # that, the hypothesis I concluded on the determinants of the difference between network
    # vs engagement overlap is that if the OLS regression shows a positive relationship 
    # between the network overlap and engagement overlap, it suggests that influencers with 
    # a higher network overlap tend to have higher engagement overlap while a negative relationship
    # suggests the opposite where influencers with a higher network overlap tend to have a lower engagement
    # overlap

    # In terms of a hypothesis for what makes two influencers have a high network overlap but a low engagment overlap
    # or vice versa, I hypothesize that this could be caused by several factors. Firstly, I believe that content is
    # a large factor of the determinants of the difference between network vs engagement overlap. Two influencers could
    # appeal to the same demographic which causes a high network overlap, but could have different motives behind their posts
    # such as posting for more aesthetic purposes or posting for educational/informative purposes. If this is the case, 
    # then the more educational influencer would most likely have more engagement compared to the influencer who is posting
    # for aesthetic purposes. Another factor could be due to audience demographics. For example, the two influencers could
    # be within the same social circle and post content for similar demographics, but the more popular influencer is a large reason
    # why people will also follow the less popular influencer since they share some form of relationship. This results in a high
    # network overlap, but a lower engagement overlap since many of the followers are only there for the more popular influencer.

if __name__ == "__main__":
    main()



# %%
