require(ggplot2)
require(Cairo)

verner.df <- readRDS('verner_data_for_analysis.Rds')

verner.df.small <- verner.df[verner.df$lemma.macroinfl.id=="leusan-|1+3PastSgInd|C"|
                             verner.df$lemma.macroinfl.id=="leusan-|PastPlInd+2PastSgInd|V"|
                             verner.df$lemma.macroinfl.id=="teuhan-|1+3PastSgInd|C"|
                             verner.df$lemma.macroinfl.id=="teuhan-|PastPlInd+2PastSgInd|V"|
                             verner.df$lemma.macroinfl.id=="fleuhan-|PastPlInd+2PastSgInd|C"|
                             verner.df$lemma.macroinfl.id=="fleuhan-|PastPlInd+2PastSgInd|V",]


change.type <- rep(NA,nrow(verner.df.small))
change.type[verner.df.small$lemma.macroinfl.id=="leusan-|1+3PastSgInd|C"] <- "verlieren, 1+3PastSgInd, s->r"
change.type[verner.df.small$lemma.macroinfl.id=="leusan-|PastPlInd+2PastSgInd|V"] <- "verlieren, PastPlInd+2PastSgInd, u->o"
change.type[verner.df.small$lemma.macroinfl.id=="teuhan-|1+3PastSgInd|C"] <- "ziehen, 1+3PastSgInd, h->g"
change.type[verner.df.small$lemma.macroinfl.id=="teuhan-|PastPlInd+2PastSgInd|V"] <- "ziehen, PastPlInd+2PastSgInd, u->o"
change.type[verner.df.small$lemma.macroinfl.id=="fleuhan-|PastPlInd+2PastSgInd|C"] <- "fliehen, PastPlInd+2PastSgInd, g->h"
change.type[verner.df.small$lemma.macroinfl.id=="fleuhan-|PastPlInd+2PastSgInd|V"] <- "fliehen, PastPlInd+2PastSgInd, u->o"

verner.df.small$change.type <- change.type

colnames(verner.df.small)[2]='date.norm'
colnames(verner.df.small)[30]='date'
colnames(verner.df.small)[23]='variant'

CairoPDF('verb_trends.pdf',height=4,width=8)
ggplot(data=verner.df.small) + geom_point(aes(color=change.type,x=date,y=variant),alpha=.5) + 
  geom_smooth(aes(color=change.type,x=date,y=variant),
                                                            method = "gam", method.args = list(family = "binomial"),se=F) + 
              #method = "loess") + 
  #scale_colour_manual(values = c("blue", "dodgerblue", "red", "orange", "green", "limegreen"))
  #scale_colour_manual(values = c("blue", "dodgerblue", "red", "orange", "purple", "salmon"))
  #scale_colour_manual(values = c("#0072B2","#56B4E9","#E69F00","#F0E442","#D55E00","#CC79A7"))
scale_colour_manual(values = c("#0072B2","#56B4E9","#009E73","limegreen","#D55E00","#CC79A7"))
dev.off()