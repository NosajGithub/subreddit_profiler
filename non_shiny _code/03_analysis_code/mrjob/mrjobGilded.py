"""Run MRJob to get the amount of reddit gold by subreddit."""

from mrjob.job import MRJob
import re, sys

class MRGilded(MRJob):

    def mapper(self, _, line):
        cline = re.sub("[~`*>#().!?,\[]","",line)
        cline2 = re.sub("(&gt;)|(&amp;)|(&lt;)|\]"," ",cline).lower()
        words = cline2.split()
        subreddit = words[0]
#         comment_id = words[1]
#         ups = words[2]
#         downs = words[3]
#         score = words[4]
        gilded = words[5]
#         author = words[6]
#         sub_id = words[7]
#         created_utc = words[8]
        if(int(gilded) > 0):
            sys.stderr.write("Mapper: ({0})\n".format(subreddit))
            yield subreddit, int(gilded)

    def reducer(self, subreddit, gilded):
        sys.stderr.write("Reducer: ({0})\n".format(subreddit))
        yield subreddit, sum(gilded)

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer)
        ]
        
if __name__ == '__main__':
    MRGilded.run()