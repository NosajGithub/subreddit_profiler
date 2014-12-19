"""Run MRJob to get the number of comments per submission by subreddit."""

from mrjob.job import MRJob
from math import sqrt
import re, sys

class MRComPerSub(MRJob):

    def mapper(self, _, line):
        cline = re.sub("[~`*>#().!?,\[]","",line)
        cline2 = re.sub("(&gt;)|(&amp;)|(&lt;)|\]"," ",cline).lower()
        words = cline2.split()
        subreddit = words[0]
#         comment_id = words[1]
#         ups = words[2]
#         downs = words[3]
#         score = words[4]
#         gilded = words[5]
#         author = words[6]
        sub_id = words[7]
#         created_utc = words[8]
        sys.stderr.write("Mapping: ({0},{1})\n".format(subreddit, sub_id))
        yield (subreddit, sub_id), 1

    def reducer(self, subr_subm_id, comments):
        subreddit, _ = subr_subm_id
        sys.stderr.write("Reducing 1: ({0})\n".format(subreddit))
        yield subreddit, sum(comments)

    def reducer_find_average_comments(self, subreddit, comments_per_sub):
        # Adapting code from http://machinelearningbigdata.pbworks.com/w/file/39039071/mrMeanVar.py
        N = 0.0
        value_sum = 0.0
        sumsq = 0.0
        for x in comments_per_sub:
            N += 1
            value_sum += x
            sumsq += x*x
        mean = value_sum/N
        sd = sqrt(sumsq/N - mean*mean)
        results = [round(mean,2),sd]
        sys.stderr.write("Reducing2: ({0})\n".format(subreddit))
        yield subreddit, results

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer),
            self.mr(reducer=self.reducer_find_average_comments)
        ]
        
if __name__ == '__main__':
    MRComPerSub.run()

