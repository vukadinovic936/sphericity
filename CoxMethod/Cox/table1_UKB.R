library(boot) 
library(table1)

df <- read.csv("I:/UKB_DATA/table1/all_UKB.csv")
df$diabetes <- as.integer(as.logical(df$diabetes))
df$ancestry <- as.integer(as.logical(df$ancestry))
df$mri_taken <- as.integer(as.logical(df$mri_taken))

df$mri_taken <- 
  factor(df$mri_taken, 
         levels=c(0,1),
         labels=c("NO MRI", "MRI"))

df$sex <- 
  factor(df$sex, levels=c(1,0),
         labels=c("Male", 
                  "Female"))
df$hypertension <-
  factor(df$hypertension, levels=c(0,1),
         labels= c("Absent",
                   "Present"))
df$diabetes <-
  factor(df$diabetes, levels=c(0,1),
         labels= c("Absent",
                   "Present"))
df$MI <-
  factor(df$MI, levels=c(0,1),
         labels= c("Absent",
                   "Present"))
df$ancestry <-
  factor(df$ancestry, levels=c(1,0),
         labels= c("White British",
                   "Other"))

label(df$sex) <- "Sex"
label(df$age) <- "Age"
label(df$pulse_rate) = "Pulse Rate"
label(df$hypertension) = "Hypertension"
label(df$BMI) = "BMI"
label(df$pulse_rate_x) = "Pulse Rate"
label(df$diabetes) = "Diabetes"
label(df$MI) = "Prior Myocardial Infarction"
label(df$ancestry) = "Ancestry"
table1(~ sex +
         age + 
         pulse_rate_x + 
         BMI + 
         hypertension + diabetes + MI + ancestry | mri_taken, data = df,overall="Total")

