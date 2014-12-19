"""Run MRJob to get the number of unique commenting users by subreddit."""

from mrjob.job import MRJob
import re, sys

class MRAuthors(MRJob):

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
        author = words[6]
#         sub_id = words[7]
#         created_utc = words[8]
        sys.stderr.write("Mapping: ({0},{1})\n".format(subreddit, author))
        yield (subreddit, author), None

    def reducer(self, subr_auth, _):
        subreddit, _ = subr_auth
        sys.stderr.write("Reducing1: ({0})\n".format(subreddit))
        yield subreddit, 1

    def reducer_unique_authors(self, subreddit, author_count):
        sys.stderr.write("Reducing2: ({0})\n".format(subreddit))
        yield subreddit, sum(author_count)

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer),
            self.mr(reducer=self.reducer_unique_authors)
        ]
        
if __name__ == '__main__':
    MRAuthors.run()


