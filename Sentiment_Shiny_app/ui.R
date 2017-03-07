library(dygraphs)

# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyUI(fluidPage(

  # Application title
  titlePanel("11/7/16 Sentiment Analysis"),

                # Show the time series plot of the twitter follower counts
                mainPanel(
                  dygraphOutput("dygraph1",height = "500px")
                )
  )                
)
