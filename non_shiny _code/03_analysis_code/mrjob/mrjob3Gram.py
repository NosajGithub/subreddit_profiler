"""Run MRJob to get the top scoring 3-grams by subreddit."""

from mrjob.job import MRJob
import re, sys

class MRNGram(MRJob):

    def mapper(self, _, line):
        score_celing = 100

        cline = re.sub("[~`*>#().!?,\[]","",line)
        cline2 = re.sub("(&gt;)|(&amp;)|(&lt;)|\]"," ",cline).lower()
        words = cline2.split()
        subreddit = words[0]
#         comment_id = words[1]
#         ups = words[2]
#         downs = words[3]
        score = words[4]
#         gilded = words[5]
#         author = words[6]
#         sub_id = words[7]
#         created_utc = words[8]    
        ngrams = [words[i] + " " + words[i+1] + " " + words[i+2] for i in range(9, len(words)-2)]
        unique_ngrams = list(set(ngrams))
        score = float(score)
        if (score > score_celing):
            score = score_celing
        for ngram in unique_ngrams:
            sys.stderr.write("Mapper: ({0})\n".format(subreddit))            
            yield (subreddit, ngram),score          

    def reducer_find_average_score(self, sub_word, scores):
        min_appearances = 10
        
        # Adapting code from http://machinelearningbigdata.pbworks.com/w/file/39039071/mrMeanVar.py
        subreddit, word = sub_word
        N = 0.0
        value_sum = 0.0
        for x in scores:
            N += 1
            value_sum += x
        mean = value_sum/N
        if N > min_appearances:
            sys.stderr.write("Reducer1: ({0})\n".format(subreddit))
            yield subreddit, (mean, word, N)

    def reducer_find_max_word(self, subreddit, word_score_pairs):        
        word_score_pairs = sorted(word_score_pairs, reverse=True)
        for i in range(10):
            mean, word, N = word_score_pairs[i]
            sys.stderr.write("Reducer2: ({0})\n".format(subreddit))
            yield subreddit, (round(mean,2), word, N)

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer_find_average_score),
            self.mr(reducer=self.reducer_find_max_word)
        ]
        
if __name__ == '__main__':
    MRNGram.run()

