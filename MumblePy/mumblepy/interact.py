from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from .db import recordApiCall


def likeUserMostRecent(driver,url,upperFollowerLimit,lowerFollowerLimit):
    try:
        userInfo = {}

        liked = False
        driver.get(url)
        sleep(5)

        u = driver.current_url.split('/')
        username = u[3]

        sideBar = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]')
        stats = sideBar.find_elements_by_class_name('infoStats__value')
        followers = int(stats[0].text)
        following = int(stats[1].text)
        tracks = int(stats[2].text)

        #go to their tracks and like the most recent
        if tracks > 0:
            url = driver.current_url
            url = url + '/tracks'
            driver.get(url)
            sleep(4)

            u = url.split('/')
            username = u[3]
            userInfo = {}
            userInfo['username'] = username
            userInfo['numFollowers'] = followers
            userInfo['numFollowing'] = following
            userInfo['numTracks'] = int(tracks)
            userInfo['liked'] = liked


            if followers > upperFollowerLimit:
                liked = False
                print('Too many followers... {} is greater than upper threshold {}'.format(followers,upperFollowerLimit))
                return liked, userInfo
            elif followers < lowerFollowerLimit:
                liked = False
                print('Not enough followers... {} is lower than lower threshold {}'.format(followers,lowerFollowerLimit))
                return liked, userInfo


            try:
                likeButton = driver.find_element_by_class_name('sc-button-like')
                if likeButton.get_property('title') != 'Like':
                    print('Song already liked. Skipping..')
                else:
                    ActionChains(driver).move_to_element(likeButton).click().perform()
                    songsList = driver.find_elements_by_class_name('soundList__item')
                    firstSong = songsList[0].find_element_by_class_name('sound__coverArt')
                    firstSongLink = firstSong.get_attribute('href')
                    userInfo['link'] = firstSongLink
                    liked = True
                    userInfo['liked'] = liked
                    recordApiCall('Like',userInfo['link'])
                    print('Liked Song: {}, by user: {}'.format(firstSongLink, username))
                    sleep(4)
            except Exception as err:
                print('error liking photo {}'.format(err))
                print('Reason error {}'.format(err.__cause__))
                liked = False
        else:
            liked = False
            print('User {}has no tracks to like'.format(username))
    except Exception as err:
        print('Error liking song {}'.format(err))
        print('Reason error {}'.format(err.__cause__))
        return False, userInfo
    return liked, userInfo

def followUser(driver,url):
    #get the follow button
    driver.get(url)
    sleep(4)
    followButton = driver.find_element_by_class_name('sc-button-follow')
    if followButton.text == 'Follow':#you are not following this person
        ActionChains(driver).move_to_element(followButton).click().perform()
        followed = True
        recordApiCall('follow',url)
        sleep(4)
        return True
    else:
        return False


def likeFromUrl(self,url):
    #work out whether the song has already been liked
    likeButton = self.driver.find_element_by_class_name('sc-button-like')
    userInfo = {}
    songInfo = {}
    liked = False
    if likeButton.get_property('title') != 'Like':
        print('Already liked song {}. Skipping'.format(url))
    else:
        #lets make sure the user fits our requisites (followers etc)
        userData = self.driver.find_element_by_class_name('userBadge__usernameLink')
        username = userData.text
        userLink = userData.get_property('href')

        userStats = self.driver.find_element_by_class_name('userStats')
        userStats = userStats.text
        userStats = userStats.split('\n')

        tracks = userStats[2]
        tracks = tracks.split(' ')
        numTracks = int(tracks[0])
        followers = userStats[0].split(' ')
        numFollowers = int(followers)

        userInfo['username'] = username
        userInfo['link'] = userLi
        userInfo['numFollowers'] = numFollowers
        userInfo['numTracks'] = numTracks

        songInfo['link'] = url
        songInfo['username'] = username

        if (numFollowers > self.upperFollowerLimit):
            print('User {} has too many followers: {}.\n Not liked'.format(userLink,numFollowers))
        else:
            ActionChains(self.driver).move_to_element(likeButton).click().perform()
            sleep(4)
            recordApiCall('Like',userlink)
            liked = True
        return liked, userInfo,songInfo



def getFromFeed(self,amount):
    url = 'https://soundcloud.com/stream'
    self.driver.get(url)
    sleep(4)
    numLiked = 0
    #play some music to throw off some shit
    playButton = self.driver.find_element_by_class_name('sc-button-play')
    print('play btn {}'.format(playButton))
    if playButton.text != "":
        ActionChains(self.driver).move_to_element(playButton).click().perform()
    i = 10
    for i in range(amount):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    songs = self.driver.find_elements_by_class_name('soundList__item')

    links = []
    for song in songs:
        link = song.find_element_by_class_name('sound__coverArt')
        links.append(link.get_property('href'))
    return self,links

#def unFollowUser(self,user):
