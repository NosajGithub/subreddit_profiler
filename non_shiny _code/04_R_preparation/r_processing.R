## Process raw output from MRJob into a format that will work for shiny

library(plyr)
library(reshape2)
library(ggplot2)
#library(sqldf)

setwd("~/Documents/workspace/205_Project/output")

#######################################################################################################################################
###                                             Data Processing Functions                                                            ##
#######################################################################################################################################

output_average <- function(inputfile, average_title){
        data <- read.table(inputfile, sep='\t',col.names = c("subreddit","value_raw"))
        data[,average_title] <- as.numeric(sapply(data$value_raw, function(x) strsplit(substr(x,2,6), ",")[[1]][1]))
        data[,c(1,3)]
}

output_ngram <- function(inputfile){
        data <- read.table(inputfile, col.names = c("subreddit","score","ngram","comma","occurrences"))
        data$score <- as.numeric(gsub(",","",gsub("\\[","",data$score)))
        data$occurrences <- as.integer(gsub("\\]","",data$occurrences))
        arrange(data[,c("subreddit","score","ngram","occurrences")],subreddit, desc(score))
}

#######################################################################################################################################
###                                                             Apply functions                                                      ##
#######################################################################################################################################

## N Grams
one_gram <- output_ngram("1gram.txt")
two_gram <- output_ngram("2gram.txt")
three_gram <- output_ngram("3gram.txt")
four_gram <- output_ngram("4gram.txt")

## Tables
common_words <- read.table("subrWordCount.txt", col.names = c("subreddit","Word", "Appearances"),stringsAsFactors = FALSE)
common_words$Word <- substr(common_words$Word,3,nchar(common_words$Word)-2)
common_words$Appearances <- as.integer(substr(common_words$Appearances,1,nchar(common_words$Appearances)-1))

top10_score <- read.table("topten_score.txt",col.names = c("subreddit","Score","Link"),colClasses = c("character","integer","character"))
top10_score$subreddit <- tolower(top10_score$subreddit)

top10_gilded <- read.table("topten_gilded.txt",col.names = c("subreddit","Gilded","Link"),colClasses = c("character","integer","character"))
top10_gilded$subreddit <- tolower(top10_gilded$subreddit)

bottom_10 <- read.table("bottom_ten.txt",col.names = c("subreddit","Score","Link"),colClasses = c("character","integer","character"))
bottom_10$subreddit <- tolower(bottom_10$subreddit)

## Metrics 
wl <- output_average("wordLength.txt","avgWordLength")
avgSc <- output_average("avgScore.txt","avgScore")
comPerSub <- output_average("ComPerSub.txt","comPerSub")
wPerCom <- output_average("wordsPerComment.txt","wordPerCom")
authors <- read.table("authors.txt", sep='\t',col.names = c("subreddit","author_count"), colClasses = c("character","integer"))
gilded <- read.table("Gilded.txt", sep='\t',col.names = c("subreddit","gilded"), colClasses = c("character","integer"))

## Combine metrics together
all <- Reduce(function(x, y) merge(x, y, by="subreddit"), list(wl, wPerCom, avgSc, gilded, comPerSub, authors))

make_percentiles <- function(table, vector_name){
        table[,paste0(vector_name,"_ptl")] <- round(ecdf(table[,vector_name])(table[,vector_name]),2)*100
        table
}

all <- make_percentiles(all, "avgWordLength")
all <- make_percentiles(all, "wordPerCom")
all <- make_percentiles(all, "avgScore")
all <- make_percentiles(all, "gilded")
all <- make_percentiles(all, "comPerSub")
all <- make_percentiles(all, "author_count")

## Time

#Week
week <- read.table("week.txt", col.names = c("subreddit", "Year", "Week", "Count"), stringsAsFactors = FALSE)
week$subreddit <- substr(week$subreddit,3,nchar(week$subreddit)-2)
week$Year <- substr(week$Year,1,nchar(week$Year)-1)
week$Week <- sprintf("%02d", as.integer(substr(week$Week,1,nchar(week$Week)-1)))

week$date <- as.numeric(as.POSIXct(as.Date(paste0(week$Year,"-",week$Week," 1"),"%Y-%W %u")))*1000

week_sub <- subset(week, subreddit == "4chan")
week_sub <- arrange(week_sub, Year, as.integer(Week))

# n1 <- nPlot(Count ~ date, 
#             data = week_sub, 
#             group = "subreddit",
#             type = "lineChart")
# n1$xAxis( tickFormat="#!function(d) {return d3.time.format('%b %Y')(new Date( d * 86400000 ));}!#" )
# n1$yAxis( axisLabel = "Count of Comments")
# n1$xAxis( axisLabel = "Date" )
# n1$chart(margin = list(left = 100, right = 100))

#week_sub$date2 <- as.numeric(as.POSIXct(week_sub$date))*1000

h1 <- hPlot(y = "Count", x= "date", 
            data = week_sub, 
            group = "subreddit",
            type = "line")
h1$xAxis(type = 'datetime', title = list(text = 'Week'), labels = list(format = '{value:%Y-%m-%d}'))
h1$yAxis(title = list(text = 'Count of Comments'))

#Day of Week
dow <- read.table("dayOfWeek.txt", col.names = c("subreddit", "Day", "Count"), stringsAsFactors = FALSE)
dow$subreddit <- substr(dow$subreddit,3,nchar(dow$subreddit)-2)
dow$Day <- substr(dow$Day,1,nchar(dow$Day)-1)
#dow$Day <- c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")[as.integer(dow$Day)+1]

dow_sub <- subset(dow, subreddit == "4chan")

# n2 <- nPlot(Count ~ Day, 
#             data = dow_sub, 
#             group = "subreddit",
#             type = "multiBarChart")
# n2$chart(showControls = FALSE)
# n2$yAxis( axisLabel = "Count of Comments")
# n2$xAxis( axisLabel = "Day of Week" )
# n2$chart(margin = list(left = 100, right = 100))

h2 <- hPlot(y = "Count", x= "Day", 
            data = dow_sub, 
            group = "subreddit",
            type = "line")
h2$xAxis(title = list(text = 'Day of Week'), categories = c('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'))
h2$yAxis(title = list(text = 'Count of Comments'), min = 0)
h2$tooltip(formatter = "#! function() { return this.x + ', ' + this.y; } !#")

#Hour of Day
hod <- read.table("hourOfDay.txt", col.names = c("subreddit", "Hour", "blank", "Count"), stringsAsFactors = FALSE)[,c(1,2,4)]
hod$subreddit <- substr(hod$subreddit,3,nchar(hod$subreddit)-2)

hod_sub <- subset(hod, subreddit == "nfl")
# n3 <- nPlot(Count ~ Hour, 
#             data = hod_sub, 
#             group = "subreddit",
#             type = "lineChart")
# n3$chart(forceY = c(0, max(hod_sub$Count)+100))
# n3$yAxis( axisLabel = "Count of Comments")
# n3$xAxis( axisLabel = "Hour of Day (Military Time)" )
# n3$chart(margin = list(left = 100, right = 100))

h3 <- hPlot(y = "Count", x= "Hour", 
            data = hod_sub, 
            group = "subreddit",
            type = "line")
h3$xAxis(title = list(text = 'Hour of Day (Military Time)'), tickInterval = 1)
h3$yAxis(title = list(text = 'Count of Comments'), min = 0)




#######################################################################################################################################
###                                                             Write to Output                                                      ##
#######################################################################################################################################

write.csv(ddply(top10_score, .(subreddit), transform, Number= seq_along(subreddit))[,c(1,4,2,3)],"../shiny/www/top10_score.csv", row.names = FALSE)
write.csv(ddply(top10_gilded, .(subreddit), transform, Number= seq_along(subreddit))[,c(1,4,2,3)],"../shiny/www/top10_gilded.csv", row.names = FALSE)
write.csv(ddply(bottom_10, .(subreddit), transform, Number= seq_along(subreddit))[,c(1,4,2,3)],"../shiny/www/bottom_10.csv", row.names = FALSE)
write.csv(ddply(common_words, .(subreddit), transform, Number= seq_along(subreddit))[,c(1,4,2,3)],"../shiny/www/common_words.csv", row.names = FALSE)
write.csv(one_gram,"../shiny/www/one_gram.csv")
write.csv(two_gram,"../shiny/www/two_gram.csv")
write.csv(three_gram,"../shiny/www/three_gram.csv")
write.csv(four_gram,"../shiny/www/four_gram.csv")
write.csv(all,"../shiny/www/all.csv")
write.csv(week,"../shiny/www/week.csv")
write.csv(dow,"../shiny/www/dow.csv")
write.csv(hod,"../shiny/www/hod.csv")
#######################################################################################################################################
###                                                             Other Stuff                                                          ##
#######################################################################################################################################
##  K Means Clustering
k_results <- kmeans(scale(all[,c(-1,-4,-6, -7)]), 4)
all[k_results$cluster == 1, ]
k_results$centers


# widen_table <- function(tablename, name){
#         data <- ddply(tablename, .(subreddit), transform, top_num= seq_along(subreddit))
#         data$top_num <- paste0(data$top_num, ".", name) 
#         data$subreddit <- tolower(data$subreddit)
#         data2 <- reshape(data, timevar = "top_num", idvar = c("subreddit"), direction = "wide")
#         data2
# }
# 
# top10_score_wide <- widen_table(top10_score, "score")
# bottom_10_wide <- widen_table(bottom_10, "bscore")
# top10_gilded_wide <- widen_table(top10_gilded, "gilded")
# widen_1gram <- widen_table(one_gram, "1gram")
# widen_2gram <- widen_table(two_gram, "2gram")

# all <- sqldf(" select a.subreddit, a.avgWordLength, b.avgScore, c.comPerSub, d.wordPerCom, e.author_count, f.gilded  
#         from wl as a 
#         inner join avgSc as b on a.subreddit = b.subreddit
#         inner join comPerSub as c on a.subreddit = c.subreddit
#         inner join wPerCom as d on a.subreddit = d.subreddit
#         inner join authors as e on a.subreddit = e.subreddit
#         inner join gilded as f on a.subreddit = f.subreddit
#       ")


