import sqlite3

class Campaign:
    def __init__(self,date = None,cType=None,tag=None,toLike=None,doFollow=None,percentageFollow=None,sleep=None,complete=None):
        self.date = date
        self.cType = cType
        self.tag = tag
        self.toLike = toLike
        self.doFollow = doFollow
        self.percentageFollow = percentageFollow
        self.sleep = sleep
        self.complete = complete
        self.campaignID = getCampaignId()

    def getCampaignID(self):
        conn = sqlite3.connect('./db/campaign.db')
        c = conn.cursor()
        c.execute('select campaignID from campaign order by campaignID desc')
        campaignID = c.fetchone()
        campaignID = int(campaignID)
        return campaignID + 1

    def saveToDb(self):
        didSave = False
        me = {}
        me['date'] = self.date
        me['cType'] = self.cType
        me['tag'] = self.tag
        me['toLike'] = self.toLike
        me['doFollow'] = self.doFollow
        me['percentageFollow'] = self.percentageFollow
        me['sleep'] = self.sleep
        me['complete'] = self.complete
        me['campaignId'] = self.campaignID

        conn = sqlite3.connect('./db/campaign.db')
        c = conn.cursor()
        c.execute('insert into campaign values (')
        return me

    def completeCampaign(self):
        self.complete = True
        conn = sqlite3.connect('./db/campaign.db')
        c = conn.cursor()
        c.execute('update campaign set complete = 1 where id=?',(self.campaignID))
        conn.commit()
        c.close()
        conn.close()
        return True

    
