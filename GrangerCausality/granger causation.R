# check data
bitstock <- read.csv(file.choose())
head(bitstock)
attach(bitstock)
par(mar=c(1,1,1,1))
plot.ts(close_btc)
plot.ts(close_sp500)

# make stationary
library(forecast)
library(lmtest)
ndiffs(close_btc)
ndiffs(close_sp500)

# differenced time series
btc <- diff(close_btc)
sp500 <- diff(close_sp500)
plot.ts(btc)
plot.ts(sp500)

# does sp500 granger cause btc?
grangertest(sp500 ~ btc, order=2)
grangertest(sp500 ~ btc, order=3)
grangertest(sp500 ~ btc, order=4)
grangertest(sp500 ~ btc, order=5)

# does btc granger cause sp500?
grangertest(btc ~ sp500, order=2)
grangertest(btc ~ sp500, order=3)
grangertest(btc ~ sp500, order=4)
grangertest(btc ~ sp500, order=5)