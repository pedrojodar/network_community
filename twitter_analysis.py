import pandas as pd
import numpy as np
import tweepy
import time
import tweepy
import networkx as nx
import mysql.connector
import matplotlib.pyplot as plt
"""

On going project: 

It creates 

"""

res_2=open('access_3.txt','r').read().splitlines()
res=open('access_2_cla.txt','r').read().splitlines()
Client = tweepy.Client(bearer_token=res_2[2], consumer_key=res_2[0],consumer_secret= res_2[1], access_token=res[2], access_token_secret=res[3], return_type = dict, wait_on_rate_limit =False)
"""
Due to the constraint of basis twitter developper account I cannot perform more than 15 queries every quarter of hour, so, I set a time between each query. 
"""


waiting_time = 60
class database:
    def __init__ (database_name='eltwitters', table_name = 'followers'):
        my=open('my.txt').read().splitlines()
        mydb=mysql.connector.connect(host="localhost", user=my[0], password=my[1],  auth_plugin='mysql_native_password')
        name_of_the_data_file = (database_name,)
        exists=False
        mycursor = mydb.cursor()
        print (name_of_the_data_file)
        mycursor.execute("SHOW DATABASES")
        for i in mycursor:
            print (i)
            if (i==name_of_the_data_file):
                print ('Exists')
                exists=True
                break
        if ( not exists):
            print ('Database is created')
            mycursor.execute("CREATE DATABASE eltwitters")
            mydb=mysql.connector.connect(host="localhost", user=my[0], password=my[1], database= database_name, auth_plugin='mysql_native_password')
            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE "+table_name+" (source VARCHAR(20), target VARCHAR(20))")
            mydb=mysql.connector.connect(host="localhost", user=my[0], password=my[1], database= database_name, auth_plugin='mysql_native_password')
            self.mycursor = mydb.cursor()    
        else:
            print ('The database has already been created')
            my=open('my.txt').read().splitlines()
            mydb=mysql.connector.connect(host="localhost", user=my[0], password=my[1], database= database_name, auth_plugin='mysql_native_password')
            self.mycursor = mydb.cursor()    
    
    def add_info(info, table, ):
        try:
            sql = "INSERT INTO "+table+" (source, target) VALUES (%s, %s)"
            #val = (follower_user[i]['username'], following_of_the_follower[k]['username'])
            val = (info[0], info[1])
            self.mycursor.execute(sql, val)
        except:
            print ('Problem inserting information in the data base ')


class obtain_info:
    def followers (self, username_val):
        user = Client.get_user(username =username_val,  user_auth=False)
        print ('Followers account ', user)
        time.sleep(waiting_time)

        page = Client.get_users_followers(user['data']['id'], max_results = 400, user_auth=False)
        if ( ('data' in page)):
            followers_total=[]
            followers_total.extend(page['data'])
            print ('Meta ',page['meta'])
            first = True
            n_page=0
            while ('next_token' in  page['meta']):
                print ('Inside', user['data']['id'])
                if (first):
                    time.sleep(waiting_time)
                    first = False
                if (n_page>10):
                    print ('A deu perfil ')
                    break
                page = Client.get_users_followers(user['data']['id'],  pagination_token=page['meta']['next_token'], max_results = 400, user_auth=False)
                if ('data' in page):
                    followers_total.extend(page['data'])
                else : 
                    print (page)
                time.sleep(waiting_time)
                n_page+=1
            return followers_total

        else:
            print (user['data']['username'], 'is private')
            return[]

    def elements_in_commom(self, series_id_1, series_id_2):
        return pd.Series(list(set(series_id_1).intersection(set(series_id_2))))


    def following (self, username_val):
        user = Client.get_user(username =username_val,  user_auth=False)
        print (user)
        followers_total=[]
        time.sleep(waiting_time)
        page = Client.get_users_following(user['data']['id'], max_results = 400, user_auth=False)
        try:
            followers_total.extend(page['data'])
            print ('Meta ',page['meta'])
            first = True
            while ('next_token' in  page['meta']):
                if (first):
                    time.sleep(waiting_time)
                    first = False

                page = Client.get_users_following(user['data']['id'],  pagination_token=page['meta']['next_token'], max_results = 400, user_auth=False)
                if ('data' in page):
                    followers_total.extend(page['data'])
                else:
                    print (page)
                time.sleep(waiting_time)
        except (RuntimeError, TypeError, NameError):
            print (RuntimeError, TypeError, NameError)
        return followers_total
        

        
    def info_profile (self, username_val):
        print ('Dentro')
        follow_er  = self. followers(username_val)
        follow_ing = self.following (username_val)
        try:
            follow_er_id = pd.DataFrame(follow_er)['id']
        except:
            print (follow_er)
        follow_ing_id = pd.DataFrame(follow_ing)['id']
        followers_following_id = self.elements_in_commom(follow_er_id,follow_ing_id)
        print ('Account property')
        print (len(follow_er), ' followers')
        print ('Is following ', len(follow_ing))
        print (len(followers_following_id)/len(follow_ing_id))
        print (len(followers_following_id), len(follow_ing_id))
        return follow_er, follow_ing

    def __init__ (self, properties):
        first=0
        if (properties['unfinished']):
            first=properties['first']
        properties['unfinished']=True
        follower_user, following_user = self.info_profile (properties['username'])
        follow_er_id = pd.DataFrame(follower_user)['id']
        follow_ing_id = pd.DataFrame(following_user)['id']
        graph = pd.DataFrame(columns=['source','target'])
        follower_number=[]
        """
        Checkeo si se ha creado una base de datos  
        """
        r=database()
        first = open('initial.txt','r').read().splitlines()[0]
        total_time = len(follow_er_id)
        for i in range (int(first), len(follow_er_id)):
            print (follower_user[i]['username'], i, total_time, ' minutes remaining')
            total_time-=1
            following_of_the_follower = self.followers(follower_user[i]['username'])
            if (following_of_the_follower!=[]):
                following_of_the_follower_id = pd.DataFrame(following_of_the_follower)['id']
                f2=open('followers.txt','a')
                f2.write(follower_user[i]['username']+'\t')
                for k in range (len(following_of_the_follower_id)):
                    r.add_info('followers', [follower_user[i]['username'], following_of_the_follower[k]['username']])
                    f2.write( following_of_the_follower[k]['username']+'\t')
                f2.write('\n')
                f2.close()
            properties['unfinished']=i

            
        properties['unfinished']=False
        
        

import json 

with open('properties.json', 'r') as f:
  data = json.load(f)

print (data)
user='pedrojodar_'
n = obtain_info(data)
#follower, followings =your_network(user)
