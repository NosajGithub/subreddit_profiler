"""Create a list of the 500 most-commonly used words across all subreddits to be used as stopwords."""

inputFilename = "output/allWords_counted.txt"
inputData = open(inputFilename,"r")
inputData.readline();
 
top500 = []
init = 0
tenth_value = 0
 
for line in inputData:
    words = line.split()
    word = words[0]
    score = words[1]
 
    if init < 500:
        top500.append((int(score), word))
        init += 1
        top500 = sorted(top500)
        tenth_value, _ = top500[0]
        continue
      
    if int(score) > tenth_value:
        top500[0] = ((int(score), word))
        top500 = sorted(top500)
        tenth_value, _ = top500[0]
 
top500 = sorted(top500, reverse = True)
 
output = []
for comment in top500:
    score, word = comment
    output.append(word)

print ", ".join(output)