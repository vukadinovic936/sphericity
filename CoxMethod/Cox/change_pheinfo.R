df <- load("pheinfo.rda")
nrow(pheinfo)

de <- data.frame("1000.1","systolic blood pressure",19,"quantitative measurements","golden rod")
names(de)<-c("phecode","description", "groupnum", "group", "color")
pheinfo <- rbind(pheinfo, de)

de <- data.frame("1001.1","diastolic blood pressure",19,"quantitative measurements","golden rod")
names(de)<-c("phecode","description", "groupnum", "group", "color")
pheinfo <- rbind(pheinfo, de)

de <- data.frame("1002.1","pulse rate",19,"quantitative measurements","golden rod")
names(de)<-c("phecode","description", "groupnum", "group", "color")
pheinfo <- rbind(pheinfo,de)
c(pheinfo['phecode'])

save(pheinfo,file="newpheinfo.rda")