"""Print out a list of the 10 most-gilded words by subreddit."""

import os, re

for fn in [fn for fn in os.listdir('./formatted/') if not fn.startswith('.')]:
    subreddit = re.sub("(_f.txt)","",fn)
    
    inputFilename = "formatted/" + subreddit + "_f.txt";
    inputData = open(inputFilename,"r")
    inputData.readline();
     
    top10 = []
    init = 0
    tenth_value = 0
     
    """For each subreddit, try out each comment. 
    If it's more gilded than the least-gilded comment in the top 10 pile, add it and remove the least-gilded.
    """
    for line in inputData:
        words = line.split()
        comment_id = words[1]
        gilded = words[5]
        sub_id = words[7]    
     
        if init < 10:
            top10.append((int(gilded), sub_id, comment_id))
            init += 1
            top10 = sorted(top10)
            tenth_value, _, _ = top10[0]
            continue
          
        if int(gilded) > tenth_value:
            top10[0] = ((int(gilded), sub_id, comment_id))
            top10 = sorted(top10)
            tenth_value, _, _ = top10[0]
     
    top10 = sorted(top10, reverse = True)
     
    for comment in top10:
        gilded, sub_id, comment_id = comment
        print subreddit + "    " + str(gilded) + "    http://www.reddit.com/r/" + subreddit + "/comments/" + sub_id + "/_/" + comment_id 
