'''Scrape a list of all safe-for-work subreddits in order of subscribers.'''

from __future__ import print_function
import urllib
from bs4 import BeautifulSoup

f = open('subreddits.txt', 'w')

for i in range(1,35):
    content = urllib.urlopen(("http://redditlist.com/sfw?page=%s" % i)) 
    s = content.read()
    
    soup = BeautifulSoup(s)
    
    myh3s = soup.find("h3",text="Subscribers") #Find subscribers
    my2 = myh3s.find_next_sibling('div')       #Skip one
    my2 = my2.find_next_sibling('div')
    
    while(my2 is not None):
        foundItem = my2.find('span',attrs={'class' : 'subreddit-url'})
        print(foundItem.getText(), file = f)
        my2 = my2.find_next_sibling('div')
    
f.close()