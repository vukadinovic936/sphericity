library(tidyverse)

# histogram
df <- read.table("C:/Users/VukadinoviM/Documents/Beyond_Size/G_results/phenotypes/BSA_width.tsv",sep='\t',header = TRUE)

qplot(df$pheno,
      geom="histogram",
      fill=I("lightblue"),
      col=I("blue"),
      xlab="BSA indexed width")

max(df$pheno)


# scatter plot
df1 <- read.table("C:/Users/VukadinoviM/Documents/Beyond_Size/G_results/phenotypes/raw_width.tsv",sep='\t',header = TRUE)
df2 <- read.table("C:/Users/VukadinoviM/Documents/Beyond_Size/G_results/phenotypes/raw_length.tsv",sep='\t',header = TRUE)
df$length=df2$pheno
df$width = df1$pheno
ggplot(df, aes(x=width, y=length)) + geom_point(col=I('blue'))
