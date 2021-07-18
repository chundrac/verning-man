require(brms)
require(Cairo)
load('BRMS_fit_cub.Rmd')

new.labels <- "fliehen, PretSg, h->g
fliehen, PretSg, o->u
fliehen, PretPl, g->h
fliehen, PretPl, u->o
fliehen, ppl, g->h
fliehen, ppl, o->u
NA
fliehen, PresSg, eu->ie
frieren, PretSg, s->r
frieren, PresSg, s->r
(kièsen), PretSg, s->r
(kièsen), PretSg, o->u
(kièsen), PretPl, r->s
(kièsen), PretPl, u->o
(kièsen), ppl, r->s
(kièsen), ppl, o->ie/u
(kièsen), PresPl, s->r
NA
(kièsen), PresSg, s->r
(kièsen), PresSg, eu->ie
verlieren, PretSg, s->r
verlieren, PretSg, o->u
verlieren, PretPl, u->o
verlieren, ppl, o->?
verlieren, PresPl, s->r
NA
verlieren, PresSg, s->r
verlieren, PresSg, eu->ie
leihen, PretSg, ei->ie
leihen, PretPl, g->h
leihen, ppl, g->h
leihen, ppl, ie->Vi
(rīsen), PretSg, ei->ie
(rīsen), PretPl, r->s
(rīsen), PretPl, ie->ei
ziehen, PretSg, h->g
ziehen, PretSg, o->u
ziehen, PretPl, g->h
ziehen, PretPl, u->o
ziehen, ppl, g->h
ziehen, ppl, o->?
ziehen, PresPl, h->g
NA
ziehen, PresSg, h->g
ziehen, PresSg, eu->ie
zeihen, PretSg, h->g
zeihen, PretSg, e(i)->ie
zeihen, ppl, g->h
zeihen, ppl, ie->e(i)"

new.labels <- read.delim(textConnection(new.labels),header=F)[,1]

names(new.labels) <- levels(verner.df$lemma_macroinfl_ID)

new.labels <- na.omit(new.labels)

conditions <- data.frame(lemma_macroinfl_ID=names(new.labels))
rownames(conditions) <- new.labels
c.eff<-conditional_effects(fit,conditions=conditions,re_formula=NULL)

CairoPDF('conditional_effects.pdf',width=9,height=3)
c.eff
dev.off()

newdata.summ <- expand.grid(seq(min(verner.df$date),max(verner.df$date),length.out=1000),levels(verner.df$lemma_macroinfl_ID))
colnames(newdata.summ) <- c('date','lemma_macroinfl_ID')

fitted.vals.summ <- fitted(fit,newdata=newdata.summ,re_formula=~(1+date+I(date^2)+I(date^3)|lemma_macroinfl_ID),summary=T)
lemma_macroinfl_ID.levels.to.compare <- c()
for (i in 1:length(levels(verner.df$lemma_macroinfl_ID))) {
  x <- which(newdata.summ$lemma_macroinfl_ID==levels(verner.df$lemma_macroinfl_ID)[i])
  if (max(fitted.vals.summ[x,1]) > .5) {
    lemma_macroinfl_ID.levels.to.compare <- c(lemma_macroinfl_ID.levels.to.compare,levels(verner.df$lemma_macroinfl_ID)[i])
  }
}

lemma_macroinfl_ID.levels.to.compare <- lemma_macroinfl_ID.levels.to.compare[lemma_macroinfl_ID.levels.to.compare %in% names(new.labels)]

n.grid <- 1000

#newdata <- expand.grid(seq(min(verner.df$date),max(verner.df$date),length.out=n.grid),levels(verner.df$lemma_macroinfl_ID))
newdata <- expand.grid(c(seq(min(verner.df$date),max(verner.df$date),length.out=n.grid),seq(max(verner.df$date),max(verner.df$date)+2*(max(verner.df$date)-min(verner.df$date))),2*n.grid),levels(verner.df$lemma_macroinfl_ID))
colnames(newdata) <- c('date','lemma_macroinfl_ID')

fitted.vals <- fitted(fit,newdata=newdata,re_formula=~(1+date+I(date^2)+I(date^3)|lemma_macroinfl_ID),summary=F)

max.grid <- NULL
cutoff <- .99
for (i in 1:length(lemma_macroinfl_ID.levels.to.compare)) {
  x <- which(newdata$lemma_macroinfl_ID==lemma_macroinfl_ID.levels.to.compare[i])
  max.grid.x <- apply(fitted.vals[,x],1,function(x){ifelse(length(which(x>cutoff)) > 0,which(x>cutoff)[1],n.grid+1)})
  #names(max.grid.x) <- rep(levels(verner.df$lemma_macroinfl_ID)[i],length(max.grid.x))
  max.grid <- rbind(max.grid,max.grid.x)
}

#for (i in 1:length(lemma_macroinfl_ID.levels.to.compare)) {
#  for (j in 1:length(lemma_macroinfl_ID.levels.to.compare)) {
#    if (i != j) {
#      #print(length(which(max.grid[i,] < max.grid[j,]))/ncol(max.grid))
#      if (length(which(max.grid[i,] < max.grid[j,]))/ncol(max.grid) >= .95) {
#        print(paste(lemma_macroinfl_ID.levels.to.compare[i],lemma_macroinfl_ID.levels.to.compare[j],sep=' '))
#      }
#    }
#  }
#}

cont.1 <- c()
cont.2 <- c()
prop <- c()
for (i in 1:length(lemma_macroinfl_ID.levels.to.compare)) {
  for (j in 1:length(lemma_macroinfl_ID.levels.to.compare)) {
    if (i != j) {
      cont.1 <- c(cont.1,lemma_macroinfl_ID.levels.to.compare[i])
      cont.2 <- c(cont.2,lemma_macroinfl_ID.levels.to.compare[j])
      prop <- c(prop,length(which(max.grid[i,] < max.grid[j,]))/ncol(max.grid))
    }
  }
}

#contrasts <- cbind(cont.1,cont.2,prop)
#contrasts[,3] <- as.numeric(contrasts[,3])

contrasts <- data.frame(cont.1,cont.2,prop)
contrasts$cont.1 <- as.character(contrasts$cont.1)
contrasts$cont.2 <- as.character(contrasts$cont.2)

contrasts <- contrasts[contrasts$prop >= .85,]

contrasts.sameverb <- contrasts[unlist(lapply(strsplit(contrasts[,1],'|',fixed=T),function(x) {return(x[1])}))==unlist(lapply(strsplit(contrasts[,2],'|',fixed=T),function(x) {return(x[1])})),]

contrasts.sameverb$cont.1 <- as.character(new.labels[contrasts.sameverb$cont.1])
contrasts.sameverb$cont.2 <- as.character(new.labels[contrasts.sameverb$cont.2])

verb.nodes <- unique(c(contrasts.sameverb$cont.1,contrasts.sameverb$cont.2))

write('\\documentclass{standalone}
\\usepackage[pdf]{graphviz}

\\begin{document}
   \\digraph{verbchange}{
     {
'
      ,file='verbchange.tex'
)

for (i in 1:length(verb.nodes)) {
  write(paste(i,' [label=\"',verb.nodes[i],'\"]',sep=''),file='verbchange.tex',append=T)
}

write('}
      rankdir=LR;',file='verbchange.tex',append=T)

for (i in 1:nrow(contrasts.sameverb)) {
  if (contrasts.sameverb[i,]$prop >= .75 & contrasts.sameverb[i,]$prop < .85) {
    write(paste(which(verb.nodes==contrasts.sameverb[i,1]),' ','->',' ',which(verb.nodes==contrasts.sameverb[i,2]),' [ style=dotted ]',sep=''),file='verbchange.tex',append=T)
  }
  if (contrasts.sameverb[i,]$prop >= .85 & contrasts.sameverb[i,]$prop < .95) {
    write(paste(which(verb.nodes==contrasts.sameverb[i,1]),' ','->',' ',which(verb.nodes==contrasts.sameverb[i,2]),' [ style=dashed ]',sep=''),file='verbchange.tex',append=T)
  }
  if (contrasts.sameverb[i,]$prop >= .95) {
    write(paste(which(verb.nodes==contrasts.sameverb[i,1]),' ','->',' ',which(verb.nodes==contrasts.sameverb[i,2]),' [ style=solid ]',sep=''),file='verbchange.tex',append=T)
  }
}

write('   }
\\end{document}',file='verbchange.tex',append=T)


"
contrasts <- data.frame(cont.1,cont.2,prop)
contrasts$cont.1 <- as.character(contrasts$cont.1)
contrasts$cont.2 <- as.character(contrasts$cont.2)

contrasts <- contrasts[contrasts$prop >= .99,]

#contrasts.sameverb <- contrasts[unlist(lapply(strsplit(contrasts[,1],'|',fixed=T),function(x) {return(x[1])}))==unlist(lapply(strsplit(contrasts[,2],'|',fixed=T),function(x) {return(x[1])})),]
contrasts.sameverb <- contrasts

contrasts.sameverb$cont.1 <- as.character(new.labels[contrasts.sameverb$cont.1])
contrasts.sameverb$cont.2 <- as.character(new.labels[contrasts.sameverb$cont.2])

verb.nodes <- unique(c(contrasts.sameverb$cont.1,contrasts.sameverb$cont.2))

write('\\documentclass{standalone}
\\usepackage[pdf]{graphviz}

\\begin{document}
   \\digraph{verbchange}{
     {
'
      ,file='verbchange.tex'
)

for (i in 1:length(verb.nodes)) {
  write(paste(i,' [label=\"',verb.nodes[i],'\"]',sep=''),file='verbchange.tex',append=T)
}

write('}
      rankdir=TB;',file='verbchange.tex',append=T)

for (i in 1:nrow(contrasts.sameverb)) {
  #if (contrasts.sameverb[i,]$prop >= .75 & contrasts.sameverb[i,]$prop < .85) {
  #  write(paste(which(verb.nodes==contrasts.sameverb[i,1]),' ','->',' ',which(verb.nodes==contrasts.sameverb[i,2]),' [ style=dotted ]',sep=''),file='verbchange.tex',append=T)
  #}
  #if (contrasts.sameverb[i,]$prop >= .85 & contrasts.sameverb[i,]$prop < .95) {
  #  write(paste(which(verb.nodes==contrasts.sameverb[i,1]),' ','->',' ',which(verb.nodes==contrasts.sameverb[i,2]),' [ style=dashed ]',sep=''),file='verbchange.tex',append=T)
  #}
  if (contrasts.sameverb[i,]$prop >= .99) {
    write(paste(which(verb.nodes==contrasts.sameverb[i,1]),' ','->',' ',which(verb.nodes==contrasts.sameverb[i,2]),' [ style=solid ]',sep=''),file='verbchange.tex',append=T)
  }
}

write('   }
\\end{document}',file='verbchange.tex',append=T)


"

