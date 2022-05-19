library("survival")
library("survminer")
cox_model<- function(csv_name){

  df = read.csv(csv_name)
  df['norm_pheno'] = scale(df['pheno'])

  res.cox <- coxph(Surv(days_without_incident, status) ~ norm_pheno + age + sex + BMI + pulse_rate + hypertension, data = df)
  #sink(paste(substr(csv_name,1,nchar(csv_name)-4),sep='',"_summary.txt"))
  print(summary(res.cox))
}
## MAIN
#cox_model("myocardial_hw.csv")
cox_model("cardiac_arrest.csv")
# scale si 

