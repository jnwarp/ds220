####################################################################
#### Setup
####################################################################
## Install and load libraries
ipak <- function(pkg) {
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}

packages <- c("ggplot2", "reshape2", "gridExtra", "TSA", "astsa", "orcutt", "ggfortify", "e1071", "rgl", "misc3d", "hydroGOF", "leaps", "car")
ipak(packages)

####################################################################
#### Cross Correlation Function
####################################################################

data = read.csv(file="DatePrice_BitCoin copy.csv", header=TRUE, sep=",")

bitcoinData = read.csv(file="/Users/tomokitakasawa/Documents/GitHub/ds220/processed/justBitcoin.csv", header=TRUE, sep=",")
stockData = read.csv(file="/Users/tomokitakasawa/Documents/GitHub/ds220/processed/justStock.csv", header=TRUE, sep=",")

plot(bitcoinData$close_btc, col="red")
points(stockData$close_sp500, col="blue") 

#btc_ts = ts(bitcoinData$close_btc, freq=7)
#stock_ts = ts(stockData$close_sp500, freq=7)

btc_ts = ts(bitcoinData$close_btc)
stock_ts = ts(stockData$close_sp500)
test = cbind(btc_ts, stock_ts)
plot(cor(test))


ccfvalues = ccf (btc_ts, stock_ts)
ccfvalues
lag2.plot (btc_ts, stock_ts, 10)


####################################################################
#### Now Linear model for prediction
####################################################################


alldata=ts.intersect(stock_ts,
                     stock_tslag1=lag(stock_ts,-1), 
                     stock_tslag2=lag(stock_ts,-2),
                     stock_tslag3=lag(stock_ts,-3),
                     stock_tslag4=lag(stock_ts,-4), 
                     btc_tslag5 = lag(btc_ts,-5),
                     btc_tslag6=lag(btc_ts,-6), 
                     btc_tslag7=lag(btc_ts,-7), 
                     btc_tslag8=lag(btc_ts,-8), 
                     btc_tslag9=lag(btc_ts,-9),
                     btc_tslag10=lag(btc_ts,-10))

alldata2=ts.intersect(stock_ts,stock_tslag1=lag(stock_ts,-1), stock_tslag2=lag(stock_ts,-2), btc_tslag5 = lag(btc_ts,-5),
                      btc_tslag6=lag(btc_ts,-6), btc_tslag7=lag(btc_ts,-7), btc_tslag8=lag(btc_ts,-8), btc_tslag9=lag(btc_ts,-9),
                      btc_tslag10=lag(btc_ts,-10), btc_tslag11=lag(btc_ts,-11), btc_tslag12=lag(btc_ts,-12), btc_tslag13=lag(btc_ts,-13))

model1 = lm(stock_ts~btc_tslag5+btc_tslag6+btc_tslag7+btc_tslag8+btc_tslag9+btc_tslag10, data = alldata)
summary (model1)
acf2(residuals(model1))

model2 = lm(stock_ts~stock_tslag1+stock_tslag2+btc_tslag5+btc_tslag6+btc_tslag7+btc_tslag8+btc_tslag9+btc_tslag10,
            data = alldata)
summary (model2)
acf2(residuals(model2))
plot(model2)

model4 = lm(stock_ts~stock_tslag1+stock_tslag2+btc_tslag5+btc_tslag6+btc_tslag7+btc_tslag8+btc_tslag9+btc_tslag10+btc_tslag11+btc_tslag12+btc_tslag13,
            data = alldata2)
summary (model4)
acf2(residuals(model4))
plot(model4)
#plot(btc_ts, stock_ts)
#points(data$close_btc, model2, col = "red", pch=16)



model3 = lm(stock_ts~stock_tslag1+btc_tslag8+btc_tslag9, data = alldata)
summary (model3)
acf2(residuals(model3))

predict(model3, interval = "predict")
#residual 


model_selection_data=ts.intersect(stock_ts,btc_ts,
                                  btc_tslag1=lag(btc_ts,-1),
                                  btc_tslag2=lag(btc_ts,-2),
                                  btc_tslag3=lag(btc_ts,-3),
                                  btc_tslag4=lag(btc_ts,-4),
                                  btc_tslag5=lag(btc_ts,-5),
                                  btc_tslag6=lag(btc_ts,-6), 
                                  btc_tslag7=lag(btc_ts,-7), 
                                  btc_tslag8=lag(btc_ts,-8), 
                                  btc_tslag9=lag(btc_ts,-9),
                                  btc_tslag10=lag(btc_ts,-10))



p_full = 12 # Number of predictors + 1
alldata_df = data.frame(as.matrix(model_selection_data), day=time(model_selection_data))
select_full = regsubsets(stock_ts~btc_ts+btc_tslag1+btc_tslag2+btc_tslag3+btc_tslag4+btc_tslag5+btc_tslag6+btc_tslag7+btc_tslag8+btc_tslag9+btc_tslag10,
                         method = "exhaustive", 
                         nbest = 1, nvmax = p_full-1, data = model_selection_data)
full_sum = summary(select_full)

full_sum$which




## Useful Values
totalSS = sum((alldata_df$stock_ts - mean(alldata_df$stock_ts))^2)
n = nrow(alldata_df)
sigma_hat_full = summary(model2)$sigma

####################################################################
#### Full Model AIC, BIC, Mallows C, Adj R2
####################################################################
## Necessary Values
p_f = 2:p_full
RSS_full = full_sum$rss

## Adjusted R2
R2_adj_full = 1 - (RSS_full/(n - p_f))/(totalSS/(n - 1))
plot(p_f, R2_adj_full, xlab = "Number of betas", ylab = "Adjusted R-squared")  # Manual: 9

## Mallow's C
C_p_full = RSS_full/(sigma_hat_full^2) + 2 * p_f - n
C_p_diff_full = abs(abs(C_p_full) - p_f)
plot(p_f, C_p_full, xlab = "Number of betas", ylab = "Mallow's Cp")  # Manual: 8
abline(0, 1)

## AIC
aic_full = n * log(RSS_full/n) + 2 * p_f
plot(p_f, aic_full, xlab = "Number of betas", ylab = "AIC")

## BIC
bic_full = n * log(RSS_full/n) + p_f * log(n)
plot(p_f, bic_full, xlab = "Number of betas", ylab = "BIC")

## Suggested Number of Betas
r2_f = which.max(R2_adj_full) + 1
mc_f = which.min(C_p_diff_full[1:(p_full-1)]) + 1
aic_f = which.min(aic_full) + 1
bic_f = which.min(bic_full) + 1
full_selection_betas = rbind(c(r2_f, mc_f, aic_f, bic_f))


full_selection_betas



LinearModel2 = lm(stock_ts~btc_ts+btc_tslag10,
            data = model_selection_data)

LinearModel3 = lm(stock_ts~btc_ts+btc_tslag7+btc_tslag10,
                  data = model_selection_data)

summary(LinearModel3)







####################################################################
#### State Vector Machine
####################################################################

library(e1071)

data = read.csv(file="/Users/tomokitakasawa/Documents/GitHub/ds220/processed/svm.csv", header=TRUE, sep=",")

plot3d(data[,-1], col=data$y)
# close_sp,,, close
#modelsvm = svm(y~., data)

plot(data$close_btc,data$close_sp500)

modelsvm = svm(data$close_sp500~data$close_btc, data)
predYsvm = predict(modelsvm, data)
points(data$close_btc, predYsvm, col = "red", pch=16)

W = t(modelsvm$coefs) %*% modelsvm$SV
b = modelsvm$rho

summary(predYsvm)

rmse(predYsvm,data$close_sp500)
rmse(data$close_sp500, predYsvm)


OptModelsvm=tune(svm, data$close_sp500~data$close_btc, data=data,ranges=list(elsilon=seq(0,1,0.1), cost=1:100))

#Print optimum value of parameters
print(OptModelsvm)

#Plot the perfrormance of SVM Regression model
plot(OptModelsvm)





#Find out the best model
BstModel=OptModelsvm$best.model
#Predict Y using best model
PredYBst=predict(BstModel,data)
#Calculate RMSE of the best model 
RMSEBst=rmse(PredYBst,data$close_sp500)


## Plotting SVR Model and Tuned Model in same plot

plot(data, pch=16)
points(data$close_btc, predYsvm, col = "blue", pch=3)
points(data$close_btc, PredYBst, col = "red", pch=4)
points(data$close_btc, predYsvm, col = "blue", pch=3, type="l")
points(data$close_btc, PredYBst, col = "red", pch=4, type="l")


##Calculate parameters of the Best SVR model
#Find value of W
W = t(BstModel$coefs) %*% BstModel$SV
#Find value of b
b = BstModel$rho






