library("survival")
library("survminer")
library("scales")
library("ggplot2")


csv_name = 'cardiac_arrest.csv'
myocardial = read.csv(csv_name)
## make time in years
myocardial['years_without_incident'] = myocardial['days_without_incident']/365
## split in lower 20 percentile mid 60 and top 20
hw_20_60_20 <- myocardial
hw_20_60_20['norm_hw']=hw_20_60_20['pheno']
p_20 <- quantile(hw_20_60_20$norm_hw, probs = 0.2)
p_80 <- quantile(hw_20_60_20$norm_hw, probs = 0.8)
# 1 will stand for bottom 20, 2 for mid 60 and 3 for top 20
hw_20_60_20['group'] = 0
g1 <- c(hw_20_60_20['norm_hw']<=p_20)
g2 <- c( (hw_20_60_20['norm_hw']>p_20 & hw_20_60_20['norm_hw'] < p_80 ))
g3 <- c(hw_20_60_20['norm_hw'] >= p_80)
hw_20_60_20[g1,]['group'] = 3
hw_20_60_20[g2,]['group'] = 2
hw_20_60_20[g3,]['group'] = 1
# now we have groups, how to plot them?

km.fit <- survfit(Surv(years_without_incident, status) ~ group, data = hw_20_60_20)
km.surv <- ggsurvplot(km.fit,
                      risk.table = "nrisk_cumevents",
                      xlim = c(0,10),
                      risk.table.title="Number at risk (Number of Events)",
                      legend.labs=c("Top 20","Mid 60","Bot 20"))
km.surv

res.cox <- coxph(Surv(years_without_incident, status) ~ group + age + sex + BMI + pulse_rate + hypertension, data = hw_20_60_20)
summary(res.cox)
hw_df <- with(hw_20_60_20,
              data.frame(group = c(1, 2, 3),
                         sex = rep(mean(sex,na.rm = TRUE),3),
                         age = rep(mean(age,na.rm= TRUE),3),
                         BMI = rep(mean(BMI, na.rm = TRUE),3),
                         pulse_rate = rep(mean(pulse_rate, na.rm = TRUE),3),
                         hypertension = rep(mean(hypertension, na.rm = TRUE),3)
              ))

fit <- survfit(res.cox, newdata = hw_df)
plot <- ggsurvplot(fit, 
           conf.int = TRUE, 
           data=hw_20_60_20,
           legend.labs=c("Top 20", "Mid 60", "Bot 20"),
           ylim= c(0.0,0.001),
           xlim = c(0,10),
           xlab="Time from Cardiac MRI (years)",
           ylab="Cumulative Incidence (%)",
           fun="event",
           censor=FALSE,
           risk.table=TRUE,
           surv.scale = c("percent"),
           risk.table.col="strata") + ggtitle("Cardiac Arrest")
plot$table <- km.surv$table
print(plot, risk.table.height=0.3)
print(plot)
# https://github.com/kassambara/survminer/issues/231
#plot$plot <- plot$plot + 
#scale_y_continuous(breaks = seq(0,1,by=0.1), labels = seq(0,100,by=10))
## saves file to csv_name.png
#myocardial = read.csv(csv_name)
#myocardial['norm_hw'] = scale(myocardial['hw'])
#res.cox <- coxph(Surv(days_without_incident, status) ~ norm_hw + age + sex + BSA, data = myocardial)
#summary(res.cox)
#res.cox

