library("survival")
library("survminer")

csv_name = 'hypertension.csv'
myocardial = read.csv(csv_name)
## make time in years
myocardial['years_without_incident'] = myocardial['days_without_incident']/365
## split in lower 20 percentile mid 60 and top 20
hw_20_60_20 <- myocardial
hw_20_60_20['norm_hw']=scale(hw_20_60_20['hw'])
p_20 <- quantile(hw_20_60_20$norm_hw, probs = 0.2)
p_80 <- quantile(hw_20_60_20$norm_hw, probs = 0.8)
# 1 will stand for bottom 20, 2 for mid 60 and 3 for top 20
hw_20_60_20['group'] = 0
g1 <- c(hw_20_60_20['norm_hw']<=p_20)
g2 <- c( (hw_20_60_20['norm_hw']>p_20 & hw_20_60_20['norm_hw'] < p_80 ))
g3 <- c(hw_20_60_20['norm_hw'] >= p_80)
hw_20_60_20[g1,]['group'] = 1
hw_20_60_20[g2,]['group'] = 2
hw_20_60_20[g3,]['group'] = 3
# now we have groups, how to plot them?
res.cox <- coxph(Surv(years_without_incident, status) ~ group + age + sex + BSA, data = hw_20_60_20)
summary(res.cox)
hw_df <- with(hw_20_60_20,
              data.frame(group = c(1, 2, 3),
                         sex = rep(mean(sex,na.rm = TRUE),3),
                         age = rep(mean(age,na.rm= TRUE),3),
                         BSA = rep(mean(BSA, na.rm = TRUE),3)
              ))
fit <- survfit(res.cox, newdata = hw_df)
ggsurvplot(fit, 
           conf.int = TRUE, 
           data=hw_20_60_20,
           legend.labs=c("Bot 20", "Mid 60", "Top 20"),
           ylim= c(0.0,0.5),
           xlim = c(0,10),
           xlab="Time from Cardiac MRI (years)",
           ylab="Cumulative Incidence",
           fun="event",
           ggtheme = theme_minimal(),
           risk.table=T) + ggtitle("Hypertension")

## saves file to csv_name.png
#myocardial = read.csv(csv_name)
#myocardial['norm_hw'] = scale(myocardial['hw'])
#res.cox <- coxph(Surv(days_without_incident, status) ~ norm_hw + age + sex + BSA, data = myocardial)
#summary(res.cox)
#res.cox

