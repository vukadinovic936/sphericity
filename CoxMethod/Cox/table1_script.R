library(boot) 
library(table1)

df <- read.csv("C:/Users/VukadinoviM/Documents/Beyond_Size/results/table1_distributions/data.csv")
df$used_in_gwas <- 
  factor(df$used_in_gwas, 
         levels=c(1),
         labels=c("Used in GWAS"))

df$sex <- 
  factor(df$sex, levels=c(1,0),
         labels=c("Male", 
                  "Female"))
df$hypertension <-
  factor(df$hypertension, levels=c(0,1),
         labels= c("Absent",

                   "Present"))

label(df$sex) <- "Sex"
label(df$age) <- "Age"
label(df$pulse_rate) = "Pulse Rate"
label(df$hypertension) = "Hypertension"
label(df$BMI) = "BMI"
label(df$cardiomyopathy) = "Cardiomyopathy"
label(df$heart_failure) = "Heart Failure"
label(df$cardiac_arrest) = "Cardiac Arrest"
label(df$atrial_fibrillation) = "Atrial Fibrillation"
table1(~ sex +
         age + 
         pulse_rate + 
         BMI + 
         hypertension | used_in_gwas, data = df,overall="Total")

