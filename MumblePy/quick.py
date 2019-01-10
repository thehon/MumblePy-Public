from datetime import datetime
from mumblepy.mumblepy import MumblePy

username = ''
password = ''

users = ['madeintyo']
song = ['https://soundcloud.com/navybluethewaterbearer/sets/yvan-wen']
today = str(datetime.date(datetime.today()))

session = MumblePy(username=username,password=password)
session.setDoFollow(enabled=True,percentage=30)
session.login()
session.doDaysCampaigns(date=today)
session.finishSesh()

#session.finishSesh()
