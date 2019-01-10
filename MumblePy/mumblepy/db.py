import sqlite3
from .campaign import Campaign
from datetime import datetime

#Class for interacting with various DB's we have

#adds a user to the DB
def addUser(username="",link="",numFollowers=0,numFollowing=0,numTracks=0,date=0,campaignID = 0):
    succesfull = False
    try:
        #do this without the existing db connects
        conn = sqlite3.connect('./db/user.db')
        c = conn.cursor()
        c.execute('insert into user values(?,?,?,?,?,?)',(username,link,numFollowers,numFollowing,numTracks,date,campaignID))
        conn.commit()
        c.close()
        conn.close()
        #self.userDbCursor.execute('insert into user values(?,?,?,?,?)',(username,link,numFollowers,numFollowing,numTracks))
        #self.userDbConnection.commit()
        succesfull = True
    except Exception as err:
        print("Error adding user to db: {}".format(err))
    return succesfull

#add a track to our db
def addTrack(link,name,dateLiked):
    succesfull = False
    try:
        conn = sqlite3.connect('./db/tracks.db')
        c = conn.cursor()
        c.execute('insert into tracks values (?,?,?,?)',(link,name,dateLiked,campaignID))
        conn.commit()
        c.close()
        conn.close()
        succesfull = True
    except Exception as err:
        print('Error adding track to db {}'.format(err))
    return succesfull

#add a campaign - this is the backbone of the operations of MumblePy - Each one is acted on in turn after a designated amount of sleep
def addCampaign(self,thisCampaign):
    succesfull = False
    try:
        conn = sqlite3.connect('./db/campaign.db')
        c = conn.cursor()
        c.execute('select campaignID from campaign order by campaignID desc limit 1')
        campaignId = c.fetchone()
        thisCampaign['campaignID'] = campaignID
        c.execute('insert into campaign values (?,?,?,?,?,?,?,?,?)',(thisCampaign))
        conn.commit()
        c.close()
        conn.close()
        succesfull = True
    except Exception as err:
        print('Error adding campaign to DB {}'.format(err))
    return succesfull

#return 1 campaign scheduled for today 
def getTodayCampaign():
    succesfull = False
    today = datetime.date(datetime.today())
    campaign = {}
    try:
        self.campaignDbCursor.execute('select * from campaign where date = (?) and complete = 0 limit 1',(str(today)))
        todaysCamp = self.campaignDbCursor.fetchone()
        campaign['type'] = todaysCamp[1]
        campaign['tag'] = todaysCamp[2]
        campaign['toLike'] = int(todaysCamp[3])
        campaign['doFollow'] = todaysCamp[4]
        campaign['percentageFollow'] = int(todaysCamp[5])
        campaign['sleep'] = int(todaysCamp[6])
        campaign['campaignID'] = int(todaysCamp[7])
        succesfull = True
    except Exception as err:
        print("Couldnt get any of today's campaigns {}".format(err))

    return succesfull, campaign

#get all of todays campaigns
def getTodaysCampaigns(self,date):
    camps = []
    returnCamps = []
    self.campaignDbCursor.execute('select * from campaign where date = (?) and complete = 0',(date,))
    camps = self.campaignDbCursor.fetchall()
    print('How many i got: {}'.format(camps))
    for camp in camps:
        returnCamps.append(Campaign(camp[0],camp[1],camp[2],int(camp[3]),camp[4],int(camp[5]),int(camp[6]),int(camp[7]),int(camp[8])))
    return returnCamps

#records an API call that weve made to Soundcloud - useful for making sure we dont go over 
def recordApiCall(self,apiType,url):
    try:
        today = datetime.date(datetime.today())
        today = str(today)
        self.apiCallsDbCursor.execute('insert into apicalls values(?,?,?)',(today,apiType,url))
        self.apiCallsDbConnection.commit()
    except Exception as err:
        print('Error recording API Call {}'.format(err))
        return False
    return True

def getNumApiCallsToday(self):
    try:
        today = datetime.date(datetime.today())
        today = str(today)
        self.apiCallsDbCursor.execute('select count(*) from apicalls where date = ?',(today))
        numCalls = self.apiCallsDbCursor.fetchone()
        if numCalls is not None:
            numCalls = int(numCalls[0])
        else:
            numCalls = 0
    except Exception as err:
        print('Error occured getting todays api calls: {}'.format(err))
    return numCalls


def getUsersFromDate(self,dates):
    users = []
    #try:
    for date in dates:
        self.userDbCursor.execute("select username from user where date = ?",(date,))
        dayUsers = self.userDbCursor.fetchall()
        if dayUsers is not None:
            for user in dayUsers:
                users.append(user)
    #except Exception as err:
    #    print('Error getting users form userdb GetusersFromDate {}'.format(err))
    return users

#add followers of owner to db
def addFollowers(self,followers,date):
    try:
        for follower in followers:
            self.followerDbCursor.execute('INSERT INTO follower values (?,?)', (follower,date))
        self.followerDbConnection.commit()
    except Exception as err:
        print('error adding follower to DB {}'.format(err))
        return False
    return True
