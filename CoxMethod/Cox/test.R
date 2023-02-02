install.packages("devtools", repos = "http://cran.us.r-project.org")
#It may be necessary to install required as not all package dependencies are installed by devtools:
install.packages(c("dplyr","tidyr","ggplot2","MASS","meta","ggrepel","DT"),  repos = "http://cran.us.r-project.org")
devtools::install_github("PheWAS/PheWAS")
