setwd("D:\\Projects\\ds220\\final_project\\")

# import bitcion data
bitpay = read.csv("raw\\bitpayUSD.csv", header=FALSE)
colnames(bitpay) <- c('Timestamp', 'USD', 'Vol')

bitpay['Timestamp'] <- transform(bitpay['Timestamp'], class=as.POSIXct(bitpay['Timestamp'], origin="1970-01-01"))
