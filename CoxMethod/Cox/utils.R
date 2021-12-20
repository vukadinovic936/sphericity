library("survival")
library("survminer")
cox_model<- function(csv_name){
  #  Attributes
  #    csv_name : str
  #      name of the file containing the following columns: hw,days_without_incident,sex,age,BSA,
  #  Return:
  #    csv_name.jpg : plot
  #      cox 20-80 plot
  #      
  #    csv_name_summary : txt
  #      cox analysis summary
  
  myocardial = read.csv(csv_name)
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
  ggsurvplot(fit, 
             conf.int = TRUE, 
             data=hw_20_80,
             legend.labs=c("Top 80", "Bot 20"),
             ylim= c(0.0,0.1),
             xlim = c(0,10),
             xlab="Time from Cardiac MRI (years)",
             ylab="Cumulative Incidence",
             fun="event",
             ggtheme = theme_minimal())
  #             risk.table=T, 
  ## saves file to csv_name.png
  ggsave( paste(substr(csv_name,1,nchar(csv_name)-3),sep='',"png"))
  
  myocardial = read.csv(csv_name)
  myocardial['norm_hw'] = scale(myocardial['hw'])
  res.cox <- coxph(Surv(days_without_incident, status) ~ norm_hw + age + sex + BSA, data = myocardial)
  sink(paste(substr(csv_name,1,nchar(csv_name)-4),sep='',"_summary.txt"))
  summary(res.cox)
}
## MAIN
#cox_model("myocardial_hw.csv")
cox_model("cardiomyopathy.csv")
cox_model("atrial_fibrillation.csv")
cox_model("heart_failure_date.csv")
cox_model("cardiac_arrest.csv")

