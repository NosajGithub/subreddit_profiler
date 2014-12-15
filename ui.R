require(shiny)

pkgTest <- function(x)
{
        if (!require(x,character.only = TRUE))
        {
                if(x != "rCharts"){
                        install.packages(x,dep=TRUE)
                } else {
                        install_github('rCharts', 'ramnathv')
                }
                if(!require(x,character.only = TRUE)) stop("Package not found")
        }
}

pkgTest("rCharts")

one_gram <- read.csv("www/one_gram.csv")

# Define the overall UI
shinyUI(
        
        # Use a fluid Bootstrap layout
        fluidPage(theme = "bootstrap.css",    
                
                # Give the page a title
                titlePanel("Subreddit Profiler"),
                
                fluidRow(
                        column(3,
                               selectInput("chosen_subreddit", "Subreddit:", choices=unique(one_gram$subreddit)),
                               br()
                        ),
                fluidRow(
                        column(12,
                               tabsetPanel(type = "tabs", 
                                           tabPanel("Upvoted Phrases", 
                                                    fluidRow(
                                                            column(3,
                                                                   h3("Selection"),
                                                                   selectInput("gram_number", "Words in Phrase:", 
                                                                               choices=c(1,2,3,4)),
                                                                   helpText("The graph shows the 10 phrases whose comments had the highest average score. 
                                                                            In parentheses is the number of times that phrase appeared in comments."),
                                                                   br(),
                                                                   helpText("Only phrases with at least 10 appearances in the subreddit were considered.
                                                                            Also, comment scores were capped at 100 to prevent undue influence from outliers.")
                                                            ),
                                                            column(9,
                                                                   h3("Top 10 Most Upvoted Phrases"),
                                                                   plotOutput("ngramPlot")
                                                            )
                                                    )
                                           ),
                                           tabPanel("Tables",
                                                    fluidRow(
                                                            column(3,
                                                                   selectInput("chosen_table", "Choose a table:", 
                                                                               choices=c("Highest Scoring Comments",
                                                                                         "Lowest Scoring Comments",
                                                                                         "Most Gilded Comments",
                                                                                         "Most Common Words"))
                                                                   )
                                                            ),
                                                    fluidRow(
                                                            dataTableOutput("table")
                                                    )
                                           ),
                                           tabPanel("Metrics",
                                                    dataTableOutput("var_table")
                                           ),
                                           tabPanel("Time",
                                                    fluidRow(
                                                            column(3,
                                                                    selectInput("chosen_time", "View comment count by:", 
                                                                        choices=c("Week",
                                                                                  "Day of Week",
                                                                                  "Hour of Day"))
                                                            )
                                                    ),
                                                    showOutput("timechart", "highcharts")
                                            ),
                                           tabPanel("About",
                                                    p(br(),
                                                            strong("The Data:"), br(),
                                                             HTML(paste0(tags$span(style="color:#BEBEBE",
                                                            "In November 2014, I scraped comments from the 275 SFW subreddits with the most subscribers per ",a("RedditList",href="http://redditlist.com/sfw"),".", br(), 
                                                            "For each subreddit, I scraped the top 1,000 submissions in its history.", br(), 
                                                            "For each submission, I scraped the first page of comments.", br(), 
                                                            "That includes anything that's visible without clicking 'more comments,' up to 200 comments per submission.", br(),
                                                            "The final dataset includes 30,984,017 comments.", br(), br(),
                                                            
                                                            em("Note"),": This isn't every comment in any given subreddit.",br(), 
                                                            "It's not even every comment over a given period of time in a given subreddit.", br(), 
                                                            "It's a subset of the comments for the highest-scoring 1,000 submissions.", br(), 
                                                            "Since reddit has grown in popularity over time, that favors more recent submissions.", br(), br()))),
                                                            
                                                            strong("The Code and Tools:"),br(), 
                                                            HTML(paste0(tags$span(style="color:#BEBEBE","All of the code for this project can be found on Github", a("here", href="https://github.com/NosajGithub"),".",br(), 
                                                            "I scraped the data with ", a("PRAW",href="https://praw.readthedocs.org/en/"), ". I stored the data on ",a("S3",href="http://aws.amazon.com/s3/"),".",br(),
                                                            "I analyzed the data with ",a("Amazon Elastic Map Reduce",href="http://aws.amazon.com/elasticmapreduce/")," and ",a("MRJob",href="https://pythonhosted.org/mrjob/"),".",br(),
                                                            "This is a ",a("Shiny app",href="http://www.rstudio.com/products/shiny/"),".",br(),br()))),
                                                      
                                                            strong("The Author:"),br(),
                                                            HTML(paste0(tags$span(style="color:#BEBEBE","I'm Jason Goodman, a ",a("Masters in Information and Data Science",href="http://datascience.berkeley.edu/")," student at UC Berkeley.",br(),
                                                            "Feel free to message me about this project on reddit - I'm ",a("u/NosajReddit",href="http://www.reddit.com/user/NosajReddit/"),".",br(),
                                                            "If you want to read my ",a("blog",href="http://nosajtblr.tumblr.com/")," or my ",a("LinkedIn profile",href="http://www.linkedin.com/in/jasonkgoodman/"),", that's cool too.")))
                                                    )
                                                    )
                               )
                        )
                )
        )
        )
)


