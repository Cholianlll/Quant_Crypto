# Author: Chao Li
# 2020 04 23
pacman::p_load(tidyverse,ggfortify,devtools,FactoMineR,factoextra, ggplot2,patchwork)

data <- read.csv('../Data/Clean data/Classification//Clean_data_train.csv',row.names = 1)
data %>% glimpse()
pac_df <- data %>% select(-y_classification) %>% select(seq(1,ncol(.),2))

pca_res <- pac_df %>% prcomp(,scale. = F, center = T)
res.pca <- PCA(pac_df,scale.unit = F, graph = FALSE)
eig.val <- get_eigenvalue(res.pca)

p1 <- fviz_eig(res.pca, addlabels = TRUE, ylim = c(0, 50))+labs(title = 'Eigenvalue plot')


p2 <- fviz_pca_ind(res.pca, label="none", habillage=as.factor(data$y_classification),
                  addEllipses=TRUE, ellipse.level=0.95)+ 
  scale_color_manual(values=c("#999999", "#E69F00"))

p3 <- fviz_pca_biplot(res.pca, label ="var", col.ind="cos2",labelsize = 3) +
  theme_minimal()

p1
ggsave("Plots/PCA1.png", height = 3, width = 8 ,bg = "white")
p2
ggsave("Plots/PCA2.png", height = 7, width = 7 ,bg = "white")
p3
ggsave("Plots/PCA3.png", height = 7, width = 7 ,bg = "white")

