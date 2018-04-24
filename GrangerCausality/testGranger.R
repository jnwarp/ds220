# READ QUARTERLY DATA FROM CSV
library(zoo)
ts1 <- read.zoo('Documents/Github/ds220/raw/bitpayUSD.csv', header = T, sep = ",", FUN = as.yearqtr)

# CONVERT THE DATA TO STATIONARY TIME SERIES
ts1$hpi_rate <- log(ts1$hpi / lag(ts1$hpi))
ts1$unemp_rate <- log(ts1$unemp / lag(ts1$unemp))
ts2 <- ts1[1:nrow(ts1) - 1, c(3, 4)]

# METHOD 1: LMTEST PACKAGE
library(lmtest)
grangertest(unemp_rate ~ hpi_rate, order = 1, data = ts2)
# Granger causality test
#
# Model 1: unemp_rate ~ Lags(unemp_rate, 1:1) + Lags(hpi_rate, 1:1)
# Model 2: unemp_rate ~ Lags(unemp_rate, 1:1)
#   Res.Df Df      F  Pr(>F)
# 1     55
# 2     56 -1 4.5419 0.03756 *
# ---
# Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# METHOD 2: VARS PACKAGE
library(vars)
var <- VAR(ts2, p = 1, type = "const")
causality(var, cause = "hpi_rate")$Granger
#         Granger causality H0: hpi_rate do not Granger-cause unemp_rate
#
# data:  VAR object var
# F-Test = 4.5419, df1 = 1, df2 = 110, p-value = 0.0353

# AUTOMATICALLY SEARCH FOR THE MOST SIGNIFICANT RESULT
for (i in 1:4)
{
  cat("LAG =", i)
  print(causality(VAR(ts2, p = i, type = "const"), cause = "hpi_rate")$Granger)
} 

