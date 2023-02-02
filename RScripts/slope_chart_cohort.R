library(ggplot2)
library(scales)
theme_set(theme_classic())
df <- read.csv("../UKB/hits_cohort.csv")
rsid=df$rsid
logp0 <- df[df$cohort_decrease==1,]$log_p
logp0.9 <- df[df$cohort_decrease==0.9,]$log_p
logp0.8 <- df[df$cohort_decrease==0.8,]$log_p
logp0.7 <- df[df$cohort_decrease==0.7,]$log_p
logp0.6 <- df[df$cohort_decrease==0.6,]$log_p
logp0.5 <- df[df$cohort_decrease==0.5,]$log_p
logp0.4 <- df[df$cohort_decrease==0.4,]$log_p


df <- data.frame(logp0,
                 logp0.9,
                 logp0.8,
                 logp0.7,
                 logp0.6,
                 logp0.5,
                 logp0.4)

df$class <- ("red")

CHR <- c("01", "06", "07","10", "19")
cols <- c("#41354d", "#78416d", "#b53b73","#d23d69", "#e67d62")

# Plot
ggplot(df, xlim=c(0.10)) +
  geom_segment(aes(x=0, xend=10, y=df$logp0, yend=df$logp0.9, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=10, xend=20, y=df$logp0.9, yend=df$logp0.8, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=20, xend=30, y=df$logp0.8, yend=df$logp0.7, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=30, xend=40, y=df$logp0.7, yend=df$logp0.6, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=40, xend=50, y=df$logp0.6, yend=df$logp0.5, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=50, xend=60, y=df$logp0.5, yend=df$logp0.4, col=CHR), size=1.0, show.legend=F) +
  geom_vline(xintercept=0, linetype="dashed", size=.1) +
  geom_vline(xintercept=10, linetype="dashed", size=.1) + 
  geom_vline(xintercept=20, linetype="dashed", size=.1) +
  geom_vline(xintercept=30, linetype="dashed", size=.1) +
  geom_vline(xintercept=40, linetype="dashed", size=.1) +
  geom_vline(xintercept=50, linetype="dashed", size=.1) +
  geom_vline(xintercept=60, linetype="dashed", size=.1) +
  geom_text(label=rsid[1:5], y=df$logp0, x=c(8,4.4,4,4,8), hjust=2, size=2.5) +
  geom_text(label=rsid[6:10], y=df$logp0.9, x=c(0,0,0,0,0), hjust=-2.5, size=2.5) +
  geom_text(label=rsid[11:15], y=df$logp0.8, x=c(0,0,0,0,-15), hjust=-6, size=2.5) +
  geom_text(label=rsid[16:20], y=df$logp0.7, x=c(1,0,0,-5,-8), hjust=-10.5, size=2.5) +
  geom_text(label=rsid[21:25], y=df$logp0.6, x=c(-30,0,0,0,-30), hjust=-13, size=2.5) +
  geom_text(label=rsid[26:30], y=df$logp0.5, x=c(-3,6,1,1,-2), hjust=-15, size=2.5) +
  geom_text(label=rsid[26:30], y=df$logp0.4, x=c(-3,6,1,1,-2), hjust=-18, size=2.5) +

  scale_x_continuous(breaks= pretty_breaks()) + 
  labs(y="P Value", x="Percents of cohort decrease") +
  ggtitle("CHANGE IN P VALUE OF TOP 5 LOCI WITH RESPECT TO COHORT DECREASE")

rsid[1:5]

rsid
df$sd1logp



ex <- read.csv("https://raw.githubusercontent.com/selva86/datasets/master/gdppercap.csv")
colnames(ex) <- c("continent", "1952", "1957")
left_label <- paste(ex$continent, round(ex$`1952`),sep=", ")
right_label <- paste(ex$continent, round(ex$`1957`),sep=", ")
ex$class <- ifelse((ex$`1957` - ex$`1952`) < 0, "red", "green")
p <- ggplot(ex) + geom_segment(aes(x=1, xend=2, y=`1952`, yend=`1957`, col=class), size=.75, show.legend=F)
p
