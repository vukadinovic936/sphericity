library(ggplot2)
library(scales)
theme_set(theme_classic())
df <- read.csv("../UKB/hits.csv")
rsid=df$rsid
sd0logp <- df[df$noise_sd==0,]$log_p
sd1logp <- df[df$noise_sd==1,]$log_p
sd2logp <- df[df$noise_sd==2,]$log_p
sd3logp <- df[df$noise_sd==3,]$log_p
sd4logp <- df[df$noise_sd==4,]$log_p
sd5logp <- df[df$noise_sd==5,]$log_p
sd6logp <- df[df$noise_sd==6,]$log_p
sd7logp <- df[df$noise_sd==7,]$log_p
sd8logp <- df[df$noise_sd==8,]$log_p
sd9logp <- df[df$noise_sd==9,]$log_p
sd10logp <- df[df$noise_sd==10,]$log_p
df <- data.frame(sd0logp,
                 sd1logp,
                 sd2logp,
                 sd3logp,
                 sd4logp,
                 sd5logp,
                 sd6logp,
                 sd7logp,
                 sd8logp,
                 sd9logp,
                 sd10logp)

df$class <- ("red")

CHR <- c("01", "06", "07","10", "19")
cols <- c("#41354d", "#78416d", "#b53b73","#d23d69", "#e67d62")

# Plot
ggplot(df, xlim=c(0.10)) +
  geom_segment(aes(x=0, xend=2, y=df$sd0logp, yend=df$sd2logp, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=2, xend=4, y=df$sd2logp, yend=df$sd4logp, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=4, xend=6, y=df$sd4logp, yend=df$sd6logp, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=6, xend=8, y=df$sd6logp, yend=df$sd8logp, col=CHR), size=1.0, show.legend=F) +
  geom_segment(aes(x=8, xend=10, y=df$sd8logp, yend=df$sd10logp, col=CHR), size=1.0, show.legend=T) +
  geom_vline(xintercept=0, linetype="dashed", size=.1) +
  geom_vline(xintercept=2, linetype="dashed", size=.1) + 
  geom_vline(xintercept=4, linetype="dashed", size=.1) +
  geom_vline(xintercept=6, linetype="dashed", size=.1) +
  geom_vline(xintercept=8, linetype="dashed", size=.1) +
  geom_vline(xintercept=10, linetype="dashed", size=.1) +
  labs(y="P Value", x="SD of Gaussian Noise") +
  ggtitle("CHANGE IN P VALUE OF TOP 5 LOCI WITH RESPECT TO NOISE")

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
