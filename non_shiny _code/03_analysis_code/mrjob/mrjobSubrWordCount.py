"""Run MRJob to get the 10 most common words in comments by subreddit, excluding stopwords."""

from mrjob.job import MRJob
import re, sys

# stopwords = []
# with open ("stopwords.txt", "r") as myfile:
#     stopwords = myfile.read().split()

class MRSubrWordCount(MRJob):

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
#         sub_id = words[7]
#         created_utc = words[8]
        sys.stderr.write("Mapping: ({0})\n".format(subreddit))
        """This isn't a great solution, but it's better than having to feed files into the middle of Hadoop map processes."""
        stopwords = ["the", "to", "a", "i", "and", "of", "that", "it", "is", "you", "in", "for", "this", "on", "but", "was", "have", "be", "with", "not", "are", "my", "they", "as", "if", "just", "like", "so", "it's", "or", "at", "your", "he", "what", "all", "would", "me", "can", "about", "do", "one", "from", "people", "an", "don't", "i'm", "more", "out", "get", "there", "when", "up", "we", "think", "no", "how", "them", "some", "because", "will", "by", "really", "their", "time", "has", "had", "know", "who", "his", "than", "only", "good", "then", "even", "much", "that's", "also", "were", "make", "now", "other", "see", "could", "been", "way", "well", "too", "which", "any", "still", "want", "why", "being", "you're", "very", "go", "something", "her", "into", "did", "she", "most", "him", "going", "should", "right", "i've", "same", "-", "actually", "never", "here", "say", "got", "where", "those", "thing", "work", "first", "over", "back", "use", "pretty", "these", "lot", "though", "can't", "doesn't", "need", "didn't", "off", "game", "things", "after", "better", "sure", "its", "does", "someone", "us", "look", "great", "years", "many", "take", "every", "before", "made", "love", "always", "down", "while", "new", "probably", "am", "deleted", "said", "around", "our", "day", "isn't", "point", "feel", "shit", "two", "find", "used", "thought", "few", "little", "ever", "bad", "best", "guy", "anything", "yeah", "life", "man", ":", "through", "long", "doing", "i'd", "makes", "might", "there's", "money", "maybe", "since", "they're", "enough", "different", "thanks", "mean", "2", "put", "own", "yes", "read", "he's", "getting", "without", "looks", "last", "give", "year", "part", "fuck", "may", "keep", "try", "everyone", "world", "both", "person", "kind", "least", "another", "such", "come", "old", "having", "big", "play", "bit", "post", "trying", "again", "fucking", "hard", "idea", "less", "done", "end", "oh", "nothing", "3", "show", "once", "anyone", "nice", "saying", "tell", "real", "problem", "stuff", "seems", "already", "awesome", "reason", "seen", "i'll", "far", "making", "everything", "games", "wrong", "until", "away", "wouldn't", "using", "times", "place", "edit:", "believe", "1", "else", "job", "whole", "either", "next", "start", "wasn't", "help", "high", "looking", "let", "fact", "live", "able", "reddit", "buy", "understand", "remember", "went", "between", "each", "true", "thank", "almost", "guys", "case", "etc", "guess", "free", "story", "agree", "ago", "instead", "found", "exactly", "aren't", "video", "change", "pay", "name", "hope", "school", "definitely", "gets", "cool", "call", "quite", "comment", "system", "stop", "top", "means", "against", "mind", "run", "god", "friends", "fun", "yet", "car", "rather", "came", "myself", "started", "sense", "usually", "amazing", "days", "women", "won't", "small", "talking", "watch", "care", "op", "however", "left", "saw", "wanted", "called", "course", "took", "home", "must", "sounds", "5", "sorry", "completely", "damn", "second", "please", "often", "full", "4", "side", "set", "water", "thinking", "question", "works", "especially", "under", "hate", "sometimes", "yourself", "seem", "working", "hell", "heard", "playing", "power", "friend", "week", "experience", "matter", "example", "comes", "wait", "kids", "interesting", "government", "worth", "picture", "hours", "wow", "likely", "similar", "face", "house", "head", "possible", "level", "others", "ask", "number", "says", "during", "happen", "movie", "we're", "book", "ones", "goes", "needs", "half", "basically", "happened", "state", "hand", "men", "easy", "black", "happy", "haven't", "seriously", "phone", "link", "told", "huge", "line", "food", "months", "family", "internet", "couple", "10", "lol", "couldn't", "sort", "check", "single", "talk", "whatever", "word", "tried", "later", "taking", "simply", "company", "amount", "unless", "wish", "night", "open", "issue", "based", "reading", "important", "funny", "support", "girl", "imagine", "what's", "hit", "team", "white", "you'll", "hear", "add", "country", "you've", "fine", "turn", "entire", "sex", "close", "deal", "body", "move", "absolutely", "large", "together", "article", "dude", "become", "totally", "three", "today", "human", "knew", "stupid", "war", "music", "sound", "minutes", "lost", "given", "difference", "she's", "past", "coming", "rest", "played", "kid"]
        for word in words[9:]:
            if word not in stopwords:
                yield (subreddit, word),1

    def reducer(self, subr_word, values):
        subreddit, word = subr_word
        sys.stderr.write("Reducing1: ({0})\n".format(subreddit))
        yield subreddit, (sum(values),word)

    def reducer2(self, subreddit, word_score_pairs):
        word_score_pairs = sorted(word_score_pairs, reverse=True)
        sys.stderr.write("Reducing2: ({0})\n".format(subreddit))
        for i in range(10):
            count, word = word_score_pairs[i]
            yield subreddit, (word, count)

    def steps(self):
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer),
            self.mr(reducer=self.reducer2)
        ]
        
if __name__ == '__main__':
    MRSubrWordCount.run()

