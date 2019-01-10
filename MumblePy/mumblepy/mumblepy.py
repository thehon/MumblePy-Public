from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import sqlite3
from datetime import datetime, timedelta

from .login import loginUser

from .interact import likeUserMostRecent
from .interact import followUser
from .interact import getFromFeed
from .interact import likeFromUrl

from .find import getLikersFromSong

from sys import maxsize

from .find import getFollowersFromUser
from .find import getFollowersFromUser2

from .db import getTodayCampaign
from .db import addUser
from .db import addCampaign
from .db import addTrack
from .db import getTodaysCampaigns
from .db import getUsersFromDate
from .db import recordApiCall
from .db import addFollowers

from .campaign import Campaign

class MumblePy:

    def __init__(self,username=None,password=None):
        self.driver = webdriver.Chrome()
        self.doFollow = False
        self.numFollow = 0
        self.doLike = False
        self.followPercentage = 0
        self.username = username
        self.password = password
        self.ignoreUsers = []
        self.userUrl = ''

        self.upperFollowerLimit = 1000
        self.lowerFollowerLimit = 0

        #set up cursors so we dont have to later
        self.userDbConnection = sqlite3.connect('./db/user.db')
        self.userDbCursor = self.userDbConnection.cursor()
        self.campaignDbConnection = sqlite3.connect('./db/campaign.db')
        self.campaignDbCursor = self.campaignDbConnection.cursor()
        self.tracksDbConnection = sqlite3.connect('./db/tracks.db')
        self.tracksDbCursor = self.tracksDbConnection.cursor()
        self.apiCallsDbConnection = sqlite3.connect('./db/apicalls.db')
        self.apiCallsDbCursor = self.apiCallsDbConnection.cursor()
        self.ownerDBConnection = sqlite3.connect('./db/owner.db')
        self.ownerDbCursor = self.ownerDBConnection.cursor()
        self.followerDbConnection = sqlite3.connect('./db/follower.db')
        self.followerDbCursor = self.followerDbConnection.cursor()

        #campaign stuff
        self.isBusy = False
        self.currentCampaignType = 'Waiting'
        self.CampaignTags = []
        self.numToLike = 0
        self.percentageFollow = 0
        self.postSleep = 0
        self.campaignID = 0

        self.apiDailyLimit = 0
        self.apiCallsToday = 0


    def updateUserFollowers(self):
        myFollowers = getFollowersFromUser2(self.driver,10,self.userUrl,emptyList)
        addFollowers(myFollowers)
        return self



    def login(self):
        if not loginUser(self.driver,self.username,self.password):
            print('Couldnt log in')
            return False
        else:
            print('Logged in succesfully')
            recordApiCall(self,'Login','Home')
            userNavButton = self.driver.find_element_by_class_name('userNav__button')
            userUrl = userNavButton.get_property('href')
            userUrl = userUrl.split('/')
            userUrl = userUrl[3]
            self.userUrl = userUrl
            self.updateUserFollowers()
            return True

    def setIgnoreUsers(self,users=None):
        self.ignoreUsers.append(users)
        return self

    def setUpperFollowerLimit(self,upperLimit):
        self.upperFollowerLimit = upperLimit
        return self

    def setLowerFollowerLimit(self,lowerLimit):
        self.lowerFollowerLimit = lowerLimit
        return self

    def setDoFollow(self,enabled=False,percentage=0):
        self.doFollow = enabled
        self.followPercentagepercentage = percentage
        return self

    def likeFromUser(self,users,toLike):
        liked = 0
        followed = 0
        links = []
        for index, user in enumerate(users):
            liked = 0
            followed = 0
            try:
                links = getFollowersFromUser2(self.driver,toLike,users[index],self.ignoreUsers)
                for link in links:
                    try:
                        like, userInfo = likeUserMostRecent(self.driver,link,self.upperFollowerLimit,self.lowerFollowerLimit)
                        if like:
                            liked = liked + 1
                            today = datetime.date(datetime.today())
                            addTrack(userInfo['link'],userInfo['username'],str(today),self.campaignID)
                            addUser(userInfo['username'],userInfo['link'],userInfo['numFollowers'],userInfo['numTracks'],str(today),self.campaignID)
                            print('Liked Song')
                            if liked >= toLike:
                                break
                            if self.doFollow:
                                follow = random.randint(0,100) <= self.followPercentage
                                if follow:
                                    try:
                                        didFollow = followUser(self.driver,link)
                                        if didFollow:
                                            followed = followed + 1
                                            print('Followed')
                                    except Exception as err:
                                        print('Error following {}'.format(err))
                    except Exception as err:
                        print('Error liking song from user: {}'.format(err))
                        print('Err reason: {}'.format(err.__reason__))

            except Exception as err:
                print('Error occured getting links {}'.format(err))
            print('Finished with {} \n Liked {} songs \n Followed {} users'.format(user,liked,followed))

        print('Finished liking from users')
        return self

    def doTodaysCamp():
        anyThere, todayCamp = getTodayCampaign()
        if anyThere:
            if todayCamp['type'] == 'user':
                user = []
                user.append(todayCamp['user'])
                likeFromUser(user,todayCamp['toLike'])
        return self

    def doDaysCampaigns(self,date):
        campaigns = []
        campaigns = getTodaysCampaigns(self,date)
        print('Got {} Campaigns'.format(len(campaigns)))
        if campaigns != None:
            for camp in campaigns:
                self.campaignID = camp.campaignID
                todayApiCalls = getNumApiCallsToday()
                if (todayApiCalls < self.apiDailyLimit):
                    print('This campaign: \nType: {}\n Tag = {}\nTo like = {}\nAfterwards I will sleep for {} seconds'.format(camp.cType,camp.tag,camp.toLike,camp.sleep,camp.campaignID))
                    #try:
                    if camp.cType == 'feed':
                        self.likeFeed(camp.toLike)
                    elif camp.cType == 'likeFromSong':
                        songLinks = []
                        songLinks = camp.tag
                        self.likeFromSong(songLinks,camp.toLike)
                    elif camp.cType == 'likeFromUser':
                        users = []
                        users = camp.tag
                        self.likeFromUser(users,camp.toLike)
                    self.currentCampaignType = 'Sleep'
                    print('Sleeping for {} seconds'.format(camp.sleep))
                    sleep(camp.sleep)
                    camp.completeCampaign()
                else:
                    print('NUmber of api calls {} exceeds daily limit {}'.format(todayApiCalls,self.apiDailyLimit))
                    return self
                    #except Exception as err:
                #    print('Error occured while doing today\'\s campaigns \n{}'.format(err))
        return self

    def likeFromSong(self,songLinks,amount):
        links = []
        try:
            for link in songLinks:
                links = links + getLikersFromSong(self.driver,amount,link,self.ignoreUsers)
        except Exception as err:
            print('Error Getting links {}'.format(err))

        for link in links:
            print('link {}'.format(link))
            liked,userInfo = likeUserMostRecent(self.driver,link,self.upperFollowerLimit,self.lowerFollowerLimit)
            if liked:
                liked = liked + 1
                print('liked Song\nLiked {} songs so far'.format(liked))
                today = datetime.date(datetime.today())
                addUser(userInfo['username'],userInfo['link'],userInfo['numFollowers'],userInfo['numTracks'])
                addTrack(userInfo['link'],userInfo['username'],str(today))
                if self.doFollow:
                    follow = random.randint(0,100) <= self.followPercentage
                    if follow:
                        didFollow = followUser(self.driver,userinfo['link'])
                        if didFollow:
                            followed = followed + 1
                            print('Followed {} . Followed {} users so far').format(userInfo['username'],followed)
        return self

    def likeFeed(self,amount):
        links = getFromFeed(amount)
        numLiked = 0
        for link in links:
            todayApiCalls = getNumApiCallsToday()
            if (todayApiCalls < self.apiDailyLimit):
                print('Doing: {}'.format(link))
                if (numLiked <= amount):
                    liked, userInfo, songInfo = likeFromUrl(link)
                    if liked:
                        numLiked = nunLiked + 1
                        addUser(userInfo['username'],userInfo['link'],userInfo['numFollowers'],userInfo['numTracks'])
                        addTrack(userInfo['link'],userInfo['username'],str(today))
                        print('Liked song {} from user {}'.format(userInfo['link'],userInfo['username']))
                    else:
                        print('Didnt like song {}')
                    print('Liked {} songs from {}'.format(numLiked,amount))
                else:
                    break
            else:
                print('Api limit of {} daily api calls has been reached'.format(self.apiDailyLimit))
                return self
        return self

    def setApiLimit(self,limit):
        self.limit = limit
        return self

    #def recordApiCall(self,apiType):

    def populateIgnoreUsers(self,days):
        daysBehind = []
        today = datetime.date(datetime.today())
        i = 0
        while (i < days):
            daysBehind.append(str(today - timedelta(i)))
            i = i + 1
        users = getUsersFromDate(self,daysBehind)
        if users is not None:
            for user in users:
                self.ignoreUsers.append(user)
        print('ignore users: {}'.format(self.ignoreUsers))
        return self

    def finishSesh(self):
        print("Finishing up here")
        self.driver.quit()
        return self

    def getUserFollowers(self):
        emptyList = []
        myFollowers = getFollowersFromUser2(self.driver,10,self.userUrl,emptyList)
        today = datetime.date(datetime.today())
        return self


    def updateUserFollowers(self):
        emptyList = []
        today = datetime.date(datetime.today())
        myFollowers = getFollowersFromUser2(self.driver,10,self.userUrl,emptyList)
        addFollowers(self,myFollowers,str(today))
        return self
