"""Run MRJob to get the number of comments on each day of the week by subreddit."""

from mrjob.job import MRJob
import re, sys
import pytz
from datetime import datetime

class MRDOW(MRJob):

    def mapper(self, _, line):
        cline = re.sub("[~`*>#().!?,\[]","",line)
        cline2 = re.sub("(&gt;)|(&amp;)|(&lt;)|\]"," ",cline).lower()
        words = cline2.split()
        subreddit = words[0]
#         comment_id = words[1]
#         ups = words[2]
#         downs = words[3]
#        score = words[4]
#         gilded = words[5]
#         author = words[6]
#         sub_id = words[7]
        created_utc = words[8]  
        sys.stderr.write("({0}, {1})\n".format(subreddit, created_utc))
        yield (subreddit, datetime.fromtimestamp(float(created_utc[:-1]), tz=pytz.timezone('America/New_York')).weekday()), 1
          
    def reducer(self, sub_dow, counts):
        yield sub_dow, sum(counts)

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer)
        ]
        
if __name__ == '__main__':
    MRDOW.run()

