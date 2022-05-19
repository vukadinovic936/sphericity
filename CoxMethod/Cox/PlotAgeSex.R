library(tidyverse)
library(WVPlots)
df <- read.csv("C:/Users/VukadinoviM/Documents/Beyond_Size/G_results/table1_distributions/data.csv")

#ggplot(df, aes(x=age, y=pheno)) + geom_point(col=I('blue'))
adjust_transparency("black",   alpha = c(0, 0.0, 0.0)) ## name
WVPlots::ScatterHist(df, "age", "pheno",
                     title= "",
                     smoothmethod = "lm",
                     contour = TRUE,
                     point_color = "black")

