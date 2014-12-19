"""Manage scraping subreddits based on what's already been scraped."""

import praw
from boto.s3.connection import S3Connection
from read_subreddit import read_a_subreddit

AWS_ACCESS_KEY_ID = #ACCESS_KEY
AWS_SECRET_ACCESS_KEY = #SECRET_KEY

user_agent = ("Comment scraper 1.0 by /u/NosajReddit" "github.com/NosajGithub/reddit-scraper")
r = praw.Reddit(user_agent=user_agent)

r.set_oauth_app_info(client_id=#CLIENT_ID, 
                     client_secret=#CLIENT_SECRET, 
                     redirect_uri=#REDIRECT_URL)

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
mybucket = conn.get_bucket('redproj')
key = mybucket.get_key('subreddits/subreddits.txt')
f = key.get_contents_as_string().split()

rs = mybucket.list("comments")
already_downloaded = -1 #because of /comments/
for key in rs:
    already_downloaded += 1

total_subreddits = len(f) - 1

for subreddit in f[already_downloaded:total_subreddits]:
    print subreddit
    read_a_subreddit(r=r,mybucket=mybucket,subreddit=subreddit)
