"""Print out a list of the 10 lowest-scoring words by subreddit."""

import os, re

for fn in [fn for fn in os.listdir('./formatted/') if not fn.startswith('.')]:
    subreddit = re.sub("(_f.txt)","",fn)
    
    inputFilename = "formatted/" + subreddit + "_f.txt";
    inputData = open(inputFilename,"r")
    inputData.readline();
     
    bottom10 = []
    init = 0
    tenth_value = 0

    """For each subreddit, try out each comment. 
    If it's lower than the highest comment in the top 10 pile, add it and remove the highest.
    """
    for line in inputData:
        words = line.split()
        comment_id = words[1]
        score = words[4]
        sub_id = words[7]    
     
        if init < 10:
            bottom10.append((int(score), sub_id, comment_id))
            init += 1
            bottom10 = sorted(bottom10, reverse = True)
            tenth_value, _, _ = bottom10[0]
            continue
          
        if int(score) < tenth_value:
            bottom10[0] = ((int(score), sub_id, comment_id))
            bottom10 = sorted(bottom10, reverse = True)
            tenth_value, _, _ = bottom10[0]
     
    bottom10 = sorted(bottom10)
     
    for comment in bottom10:
        score, sub_id, comment_id = comment
        print subreddit + "    " + str(score) + "    http://www.reddit.com/r/" + subreddit + "/comments/" + sub_id + "/_/" + comment_id 
