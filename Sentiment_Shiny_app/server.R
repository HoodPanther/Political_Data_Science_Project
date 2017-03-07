library(dygraphs)
library(htmlwidgets)
library(xts)
library(stringr)

trump_sentiment <- read.csv("trump_sentiment_11_07.csv")
trump_cum <- read.csv("trump_sentiment_cum_11_07.csv")
clinton_sentiment <- read.csv("clinton_sentiment_11_07.csv")
clinton_cum <- read.csv("clinton_sentiment_cum_11_07.csv")

datetimes_str <- paste(trump_sentiment$level_0,str_pad(trump_sentiment$level_1,2,side="left",pad='0'),sep=':')
datetimes <- as.POSIXlt(paste0("2016-11-07 ",datetimes_str), format="%Y-%m-%d %H:%M", tz="GMT")+3600*5
start_time <- datetimes[1]
end_time <- datetimes[length(datetimes)]

trump_score <- round(trump_sentiment$score,2)
trump_cum_score <- round(trump_cum$score,2)
clinton_score <- round(clinton_sentiment$score,2)
clinton_cum_score <- round(clinton_cum$score,2)

trump_score_series <- xts(trump_score, order.by = datetimes,tzone="EDT")
trump_cum_score_series <- xts(trump_cum_score, order.by = datetimes,tzone="EDT")
clinton_score_series <- xts(clinton_score, order.by = datetimes,tzone = "EDT")
clinton_cum_score_series <- xts(clinton_cum_score, order.by = datetimes,tzone = "EDT")

colnames(trump_score_series) <- "Trump"
colnames(trump_cum_score_series) <- "Trump_Cumulative"
colnames(clinton_score_series) <- "Clinton"
colnames(clinton_cum_score_series) <- "Clinton_Cumulative"

combined_series <- cbind(trump_score_series, trump_cum_score_series,
                         clinton_score_series, clinton_cum_score_series)

#a JavaScript function to change the display format of the y-axis tick labels, such that it shows the comma separate thousands place
#pass it to axisLabelFormatter and valueFormatter argument of dyAxis
FUNC_JSFormatNumber <- "function(x) {return x.toString().replace(/(\\d)(?=(\\d{3})+(?!\\d))/g, '$1,')}"

# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyServer(function(input, output) {

  output$dygraph1 <- renderDygraph({
    
    dygraph(combined_series, main="Candidate Twitter Sentiment on the Last Day before Election", xlab = "Time",ylab = "Sentiment Score (%)") %>%
      dySeries("Clinton",color="blue",drawPoints=T,pointSize=2,strokeWidth=3) %>%
      dySeries("Trump",color="red",drawPoints=T,pointSize=2,strokeWidth=3) %>%
      dySeries("Clinton_Cumulative",color="blue",drawPoints=T,pointSize=1,strokeWidth=1,strokePattern = 'dashed') %>%
      dySeries("Trump_Cumulative",color="red",drawPoints=T,pointSize=1,strokeWidth=1, strokePattern = 'dashed') %>%
      dyAxis("x",valueRange = c(start_time,end_time),rangePad=7) %>%
      dyAxis("y",valueRange = c(min(trump_score)-1, max(trump_score)+2), axisLabelFormatter=JS(FUNC_JSFormatNumber), valueFormatter=JS(FUNC_JSFormatNumber)) %>%
      dyHighlight(highlightCircleSize = 6, hideOnMouseOut = T) %>%
      dyRangeSelector(height = 25) %>%
      dyLegend(width=800) %>%
      dyOptions(axisTickSize=5,useDataTimezone=F)
  })

})
