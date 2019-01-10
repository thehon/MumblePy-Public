# This is the file that finds all the users/tracks to like
from time import sleep
from selenium import webdriver

#get the profiles of followers of a specific user - returns the links to their profile
def getFollowersFromUser(driver,amount,username):
    url = "https://soundcloud.com/{}/followers".format(username)
    sleep(5)
    i = 10
    while i < amount:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        i = i + 10
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    bodyelements = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div/div/ul/li')
    numLinks = len(bodyelements)
    links = []
    for element in bodyelements:
        a = link.find_elements_by_tag_name('a')
        print(a[1].get_property('href'))
        links.append(a[1].get_property('href'))
    return links


def getUserLinksFromList(driver,url,ignoreUsers,amount):
    driver.get(url)
    i = 24 # start with 24 links
    while (i < amount):
        sleep(5)
        links = []
        loopLinks = []
        try:
            if loopLinks == driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div/div/ul/li'):
                break
            else:
                loopLinks = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div/div/ul/li')
                for element in looopLinks:
                    a = element.find_elements_by_tag_name('a')
                    thisLink = a[1].get_property('href')
                    z = thisLink.split('/')
                    if z[3] not in ignoreUsers:
                        links.append(thisLink)
            i = i + 24 #24 cos we get 24 more per scroll
        except Exception as err:
            print('Problem getting followers {}'.format(err))

    sleep(5)

    bodyelements = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div/div/ul/li')
    links = []

    for element in bodyelements:
        a = element.find_elements_by_tag_name('a')
        thisLink = a[1].get_property('href')
        z = thisLink.split('/')
        if z[3] not in ignoreUsers:
            links.append(thisLink)
    return links


def getFollowersFromUser2(driver,amount,username,ignoreUsers):

    url = "https://soundcloud.com/{}/followers".format(username)
    links = getUserLinksFromList(driver,url,ignoreUsers,amount)
    return links[:amount]

def getLikersFromSong(driver,amount,songLink,ignoreUsers):
    url = songLink + '/likes'
    links = getUserLinksFromList(driver,url,ignoreUsers,amount)
    return links[:amount]
