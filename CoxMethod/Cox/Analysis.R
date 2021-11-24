library("survival")
library("survminer")

# Create Cox Model plot
myocardial = read.csv("myocardial_infraction.csv")
## make time in years
myocardial['years_without_incident'] = myocardial['days_without_incident']/365
## split in lower 20 percentile and top 80 percentile
hw_20_80 <- myocardial
p_20 <- quantile(hw_20_80$hw, probs = 0.2)
hw_20_80['hw'] <- hw_20_80['hw']<p_20
# true is bottom 20 percentile, false is top 80 percentile
hw_20_80['hw'] <- c(lapply(hw_20_80['hw'],as.integer))
res.cox <- coxph(Surv(years_without_incident, status) ~ hw + age + sex + BSA, data = hw_20_80)
hw_df <- with(hw_20_80,
              data.frame(hw = c(FALSE, TRUE),
                         sex = rep(mean(sex,na.rm=TRUE),2),
                         age = rep(mean(age,na.rm=TRUE),2),
                         BSA = rep(mean(BSA, na.rm = TRUE),2)
              ))
fit <- survfit(res.cox, newdata = hw_df)
# risk table = TRUE shows the number of patients
# that were under observation in the specific time frame
ggsurvplot(fit, 
           conf.int = TRUE, 
           data=hw_20_80,
           legend.labs=c("Top 80", "Bot 20"),
           ylim= c(0.95,1.0),
           risk.table=TRUE,
           ggtheme = theme_minimal())

## Cox model on numerical hw
myocardial = read.csv("myocardial_infraction.csv")
myocardial['norm_hw'] = scale(myocardial['hw'])
res.cox <- coxph(Surv(days_without_incident, status) ~ norm_hw + age + sex + BSA, data = myocardial)
summary(res.cox)

ggsurvplot(survfit(res.cox),
           data=myocardial,
           pallete = "#2E9FDF",
           ylim = c(0.95,1.0),
           ggtheme = theme_minimal())

# hazard ratio: 0.728
# 95% conf interval: 0.6449 - 0.8217
# number of cases: 279
# number of non-cases: 31437
