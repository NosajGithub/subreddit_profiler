"""Given a PRAW user agent, an S3 bucket and a subreddit name, scrape that subreddit."""

import praw
import json
from boto.s3.connection import S3Connection
import urllib2
from time import sleep

def read_a_subreddit(r, mybucket, subreddit):

    sub_dict = {}

    sub_count = 0

    submissions = r.get_subreddit(subreddit).get_top_from_all(limit=None)
    for submission in submissions:
        sub_count += 1
        print sub_count
        attempts = 0

        com_dict = {}

        while attempts < 10:
            try:

                flat_comments = praw.helpers.flatten_tree(submission.comments)
                for comment in flat_comments:
                    if not isinstance(comment,praw.objects.MoreComments):
                        com_dict[comment.id.encode('utf-8')] = {'author': str(comment.author).encode('utf-8'),
                                                            'body': comment.body.encode('utf-8'),
                                                            'created_utc': comment.created_utc,
                                                            'gilded': comment.gilded,
                                                            'score': comment.score,
                                                            'ups': comment.ups,
                                                            'downs': comment.downs}
                sub_dict[submission.id.encode('ascii','ignore')] = {'permalink': submission.permalink, 'sub_count': sub_count, 'com_dict': com_dict}

                break
            
            """In practice, this part never seemed to catch any errors."""
            except urllib2.HTTPError, e:
                if e.code in [429, 500, 502, 503, 504]:
                    attempts += 1
                    
                    with open("log.txt", "a") as f:
                        f.write("Reddit is down (error %s) for a comment\n" % e.code)
                        f.write("Moving on to attempt %i, sleeping...\n" % attempts)
                    
                    time.sleep(30)
                    pass
                else:
                    attempts += 1
                    with open("log.txt", "a") as f:
                        f.write("Error %s, try again\n" % e.code)
                    pass
            except Exception, e:
                print "couldn't Reddit: %s" % str(e)
                raise

    key = mybucket.new_key('comments/' + subreddit + '.txt')
    key.set_contents_from_string(json.dumps(sub_dict))
