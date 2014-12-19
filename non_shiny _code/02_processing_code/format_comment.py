"""Turns Reddit data from raw JSON to space-delimited lines ready for MRJob."""

import sys
import json
from boto.s3.connection import S3Connection

#output_folder = "formatted/"
output_folder = "formatted_2/"

reload(sys)  
sys.setdefaultencoding('utf8')

AWS_ACCESS_KEY_ID = #ACCESS KEY
AWS_SECRET_ACCESS_KEY = #SECRET

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
mybucket = conn.get_bucket('redproj')

key = mybucket.get_key('subreddits/subreddits_275.txt')
f = key.get_contents_as_string().split()

"""Check how many subreddits have already been formatted."""
rs = mybucket.list(output_folder)
already_downloaded = -1 # because of /formatted/
for key in rs:
    already_downloaded += 1

total_subreddits = len(f)

subr_count = already_downloaded + 1

"""Format the rest of the subreddits."""
for subreddit in f[already_downloaded:total_subreddits]:
    comments = 0
    key = mybucket.get_key('comments/' + subreddit +'.txt')
    f = key.get_contents_as_string()
     
    data = json.loads(f)
     
    formatted = []     
    for key, value in data.iteritems():
        for key2, value2 in value["com_dict"].iteritems():
            comments += 1
            if comments % 1000 == 0:
                print subreddit, subr_count, comments
            newcomment = "%s %s %i %i %i %i %s %s %s %s\n" % \
                        (subreddit, key2, value2["ups"], value2["downs"], value2["score"], value2["gilded"], value2["author"], key, value2["created_utc"], value2["body"].replace("\r"," ").replace("\n"," ").encode('utf-8'))
    
            formatted.append(newcomment)
    
    output = ''.join(formatted)
#    key = mybucket.new_key(output_folder + subreddit + '_f.txt')
    key = mybucket.new_key(output_folder + subreddit + '_f_t.txt')
    key.set_contents_from_string(output)
    
    with open("comment_count.txt", "a") as l:
        l.write((str(subr_count) + ". " + subreddit + ": " + str(comments) + " comments\n"))
    print "Formatted Subreddit: " + subreddit
    subr_count += 1