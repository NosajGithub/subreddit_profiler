"""Run MRJob to get the average word length by subreddit."""

from mrjob.job import MRJob
from math import sqrt
import re, sys

class MRCommentWordLength(MRJob):

    def mapper(self, _, line):
        cline = re.sub("[~`*>#().!?,\[\]]|http[s]?:\/\S+","",line) #Remove links for this one
        cline2 = re.sub("(&gt;)|(&amp;)|(&lt;)"," ",cline).lower() 
        words = cline2.split()
        subreddit = words[0]
#         comment_id = words[1]
#         ups = words[2]
#         downs = words[3]
#         score = words[4]
#         gilded = words[5]
#         author = words[6]
#         sub_id = words[7]
#         created_utc = words[8]
        for word in words[9:]:
#           if(len(word) >= 3):
            sys.stderr.write("Mapping: ({0})\n".format(subreddit))
            yield subreddit, len(word)

    def reducer(self, subreddit, wordlens):
        # Adapting code from http://machinelearningbigdata.pbworks.com/w/file/39039071/mrMeanVar.py
        N = 0.0
        value_sum = 0.0
        sumsq = 0.0
        for x in wordlens:
            N += 1
            value_sum += x
            sumsq += x*x
        mean = value_sum/N
        sd = sqrt(sumsq/N - mean*mean)
        results = [round(mean,2),sd]
        sys.stderr.write("Reducing: ({0})\n".format(subreddit))
        yield subreddit, results

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer)
        ]
        
if __name__ == '__main__':
    MRCommentWordLength.run()

