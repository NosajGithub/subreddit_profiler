library(shiny)
library(ggplot2)
library(stringr)
library(rCharts)

one_gram <- read.csv("www/one_gram.csv")
two_gram <- read.csv("www/two_gram.csv")
three_gram <- read.csv("www/three_gram.csv")
four_gram <- read.csv("www/four_gram.csv")
grams <- list(one_gram, two_gram, three_gram, four_gram)

all <- read.csv("www/all.csv",)[,-1]
varlist = c("Average Word Length (Characters)", 
            "Words Per Comment", 
            "Average Score", 
            "Total Reddit Gold",
            "Comments Collected Per Submission", 
            "Number of Distinct Users Commenting")

bottom_10 <- read.csv("www/bottom_10.csv")
bottom_10$Link <- paste0("<a href='",  bottom_10$Link, "?context=10000' target='_blank'>",bottom_10$Link,"</a>")

top10_score <- read.csv("www/top10_score.csv")
top10_score$Link <- paste0("<a href='",  top10_score$Link, "?context=10000' target='_blank'>",top10_score$Link,"</a>")

top10_gilded <- read.csv('www/top10_gilded.csv')
top10_gilded$Link <- paste0("<a href='",  top10_gilded$Link, "?context=10000' target='_blank'>",top10_gilded$Link,"</a>")

common_words <- read.csv('www/common_words.csv')

week <- read.csv('www/week.csv')
hod <- read.csv('www/hod.csv')
dow <- read.csv('www/dow.csv')

# Define a server for the Shiny app
shinyServer(function(input, output) {

        output$var_table <- renderDataTable({
                all_limited <- as.data.frame(all[all$subreddit == input$chosen_subreddit,])
                all_final <- as.data.frame(cbind(varlist, t(all_limited[2:7]),t(all_limited[8:13])),
                                           stringsAsFactors = FALSE,row.names = "")
                colnames(all_final) <- c("Metric","Value","Percentile Rank (Over All 275 Subreddits)")
                all_final[6,2] <- formatC(as.integer(all_final[6,2]),format="d",big.mark=",")
                all_final
                },
                options = list(pagingType = "simple", bFilter = FALSE, bPaginate = FALSE, bSearchable = FALSE) 
        )
                
        # Fill in the spot we created for a plot
        output$ngramPlot <- renderPlot({
                
                # Render a barplot
                print(ggplot(subset(grams[[as.integer(input$gram_number)]],subreddit == input$chosen_subreddit),aes(x=reorder(ngram, score), y= score)) + geom_bar(stat='identity', width=0.4, fill = '#058DC7') +
                        geom_text(aes(x=ngram, y=score,label=sprintf("%.2f (%d)", round(score,2),occurrences), hjust=-.1)) + 
                        ylim(0, 120) +
                        ylab("Average Score (# of Appearances)") +
                        xlab("NGram") +
                        theme_bw() +
                        #ggtitle("Top 10 NGrams") +
                        theme(axis.title.y=element_text(vjust=0.1, color = "grey55"),
                              axis.title.x=element_text(color="grey55"),
                              axis.text.y  = element_text(size=12, color = "black")
                              #,plot.title = element_text(vjust=0.4,size=16, face="bold")
                              ) +
                        scale_x_discrete(labels = function(x) str_wrap(x, width = 50)) +
                        coord_flip())
                
        })
        
        output$table <- renderDataTable({
                data <- switch(input$chosen_table, 
                               "Highest Scoring Comments" = top10_score,
                               "Lowest Scoring Comments" = bottom_10,
                               "Most Gilded Comments" = top10_gilded,
                               "Most Common Words" = common_words)

                data[data$subreddit == input$chosen_subreddit, -2]},
                options = list(pagingType = "simple", bFilter = FALSE, bPaginate = FALSE, bSearchable = FALSE) 
        )
        
        output$timechart <- renderChart2({
                
                if(input$chosen_time == "Week"){
                        week_sub <- subset(week, subreddit == input$chosen_subreddit)
                        week_sub <- arrange(week_sub, Year, as.integer(Week))
                        
                        h1 <- hPlot(y = "Count", x= "date", 
                                    data = week_sub, 
                                    group = "subreddit",
                                    type = "line")
                        h1$xAxis(type = 'datetime', title = list(text = 'Week'), labels = list(format = '{value:%Y-%m-%d}'))
                        h1$yAxis(title = list(text = 'Count of Comments'))
                        
                        return(h1)
                        
                } else if (input$chosen_time == "Day of Week") {
                        dow_sub <- subset(dow, subreddit == input$chosen_subreddit)
                        h2 <- hPlot(y = "Count", x= "Day", 
                                    data = dow_sub, 
                                    group = "subreddit",
                                    type = "column")
                        h2$xAxis(title = list(text = 'Day of Week'), 
                                 categories = c('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'))
                        h2$yAxis(title = list(text = 'Count of Comments'))
                        h2$tooltip(formatter = "#! function() { return this.x + ', ' + this.y; } !#")
                        
                        return(h2)
                        
                } else {
                        hod_sub <- subset(hod, subreddit == input$chosen_subreddit)
                        h3 <- hPlot(y = "Count", x= "Hour", 
                                    data = hod_sub, 
                                    group = "subreddit",
                                    type = "line")
                        h3$xAxis(title = list(text = 'Hour of Day (Military Time, EST)'), tickInterval = 1)
                        h3$yAxis(title = list(text = 'Count of Comments'), min = 0)
                        
                        return(h3)
                }
        })
})

