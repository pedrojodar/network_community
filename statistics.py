import json 
import pandas as pd

def obtain_statistics ():
    with open('message.json', 'r') as f:
        data = json.load(f)
    with open('stored_data/followers_info_'+data['user']+'.json', 'r') as f:
        res = json.load(f)
    value = pd.DataFrame(res['data'])
    properties_of_followers ={}
    mean_number_of_following = 0
    mean_number_of_followers = 0
    for i in range (len(value)):
        mean_number_of_followers+=value['public_metrics'][i]['followers_count']
        mean_number_of_following+=value['public_metrics'][i]['following_count']
    properties_of_followers.update({
        "mean_following": mean_number_of_following/len(value),
        "mean_followers":mean_number_of_followers/len(value)}) 
    text = "Properties of your followers"+'\n'
    text=text+"mean number of following"+str(properties_of_followers["mean_following"])+'\n'
    text = text + "mean number of followers"+str(properties_of_followers["mean_followers"])+'\n'

    return properties_of_followers, text
