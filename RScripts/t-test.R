library(irr)
UKB <- na.omit(read.csv("I:/UKB_DATA/tsv_pheno/lv_ef_UKB.tsv", sep='\t'))
OURS <- na.omit(read.csv("I:/UKB_DATA/tsv_pheno/my_ef_same.tsv", sep='\t'))

library(dplyr)
dt3 <- merge(x = UKB, y = OURS, by = "idx")
dt3$pheno.x <- dt3$pheno.x/100

l1 <- dt3$pheno.x
l2 <- dt3$pheno.y

l3 <- l1-l2
x = mean(l3)
n = length(l3)
s = sd(l3)
SE <- s/sqrt(n)
teststat <- (x-0)/SE
(pt(teststat,n-1))

t.test(dt3$pheno.x, dt3$pheno.y)

cor(l1,l2)^2
mean(l1-l2)


data <- data.frame(dt3$pheno.x, dt3$pheno.y)
icc(data, model = "twoway", type = "agreement", unit = "single")
dt3
