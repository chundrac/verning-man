df <- read.csv('verner_data_for_analysis.tsv',sep='\t')

sub.df <- df[df$inflcat=='PastSgInd1'|
               df$inflcat=='PastSgInd2'|
               df$inflcat=='PastSgInd3'|
               df$inflcat=='PastPlInd1'|
               df$inflcat=='PastPlInd2'|
               df$inflcat=='PastPlInd3'|
               df$inflcat=='ppl'|
               df$inflcat=='PresSgInd1'|
               df$inflcat=='PresSgInd2'|
               df$inflcat=='PresSgInd3'|
               df$inflcat=='impSg.2'|
               df$inflcat=='inf'|
               df$inflcat=='prespl'|
               df$inflcat=='PresPlInd1'|
               df$inflcat=='PresPlInd2'|
               df$inflcat=='PresPlInd3'|
               df$inflcat=='impPl.1'|
               df$inflcat=='impPl.2',]

sub.df$macroinfl <- NA
#sub.df$macroinfl <- as.character(sub.df$macroinfl)

sub.df[sub.df$inflcat=='PastSgInd1'|sub.df$inflcat=='PastSgInd3',]$macroinfl <- '1+3PastSgInd'

sub.df[sub.df$inflcat=='PastSgInd2'|
         sub.df$inflcat=='PastPlInd1'|
         sub.df$inflcat=='PastPlInd2'|
         sub.df$inflcat=='PastPlInd3',]$macroinfl <- 'PastPlInd+2PastSgInd'

sub.df[sub.df$inflcat=='ppl',]$macroinfl <- 'ppl'

sub.df[sub.df$inflcat=='PresSgInd1'|
         sub.df$inflcat=='PresSgInd2'|
         sub.df$inflcat=='PresSgInd3'|
         sub.df$inflcat=='impSg.2',]$macroinfl <- 'PresSgInd'

sub.df[sub.df$inflcat=='PresPlInd1'|
         sub.df$inflcat=='PresPlInd2'|
         sub.df$inflcat=='PresPlInd3'|
         sub.df$inflcat=='impPl.1'|
         sub.df$inflcat=='impPl.2'|
         sub.df$inflcat=='prespl'|
         sub.df$inflcat=='inf',]$macroinfl <- 'PresPlInd'

sub.df$macroinfl <- as.factor(sub.df$macroinfl)

sub.df <- sub.df[sub.df$PGmc!='wesan-' & sub.df$PGmc!='werþan-',]

verb.counts <- xtabs( ~ PGmc, sub.df)

lemmas.to.keep <- names(verb.counts[verb.counts>=10])

sub.df <- sub.df[sub.df$PGmc %in% lemmas.to.keep,]

#NA rows are Dutch/Low German, get rid of them
#sub.df[is.na(sub.df$dialect.place),]$dialect.place <- "-"

sub.df <- na.omit(sub.df)

sub.df <- droplevels(sub.df)

V.C <- c(rep('V',nrow(sub.df)),rep('C',nrow(sub.df)))

#expected outcome prior to analogical change
exp.out <- c(as.character(sub.df$V.exp),as.character(sub.df$C.exp))

response <- c(sub.df$V.coding,sub.df$C.coding)-1

verner.df <- rbind(sub.df,sub.df)

verner.df$response <- response
verner.df$V.C <- V.C
verner.df$exp.out <- exp.out

verner.df$dial.lemma.id <- as.factor(paste(verner.df$dialect.place,verner.df$PGmc,sep='|'))
verner.df$dial.infl.id <- as.factor(paste(verner.df$dialect.place,verner.df$macroinfl,sep='|'))
verner.df$lemma.macroinfl.id <- as.factor(paste(verner.df$PGmc,verner.df$macroinfl,verner.df$V.C,sep='|'))
verner.df$dial.exp.out.id <- as.factor(paste(verner.df$dialect.place,verner.df$exp.out,sep='|'))

verner.df <- droplevels(verner.df[verner.df$macroinfl=='ppl'|verner.df$macroinfl=='PastPlInd+2PastSgInd'|verner.df$macroinfl=='1+3PastSgInd'|(verner.df$class==2&verner.df$macroinfl=='PresPlInd')|(verner.df$class==2&verner.df$macroinfl=='PresSgInd'),])

categories.to.keep <- c(
  #'fleuhan-|1+3PastSgInd|C',
  #'fleuhan-|1+3PastSgInd|V',
  'fleuhan-|PastPlInd+2PastSgInd|C',
  'fleuhan-|PastPlInd+2PastSgInd|V',
  'fleuhan-|ppl|C',
  #'fleuhan-|ppl|V',
  #'fleuhan-|PresPlInd|C',
  #'fleuhan-|PresPlInd|V',
  #'fleuhan-|PresSgInd|C',
  'fleuhan-|PresSgInd|V',
  'freusan-|1+3PastSgInd|C',
  #'freusan-|1+3PastSgInd|V',
  #'freusan-|PastPlInd+2PastSgInd|C',
  'freusan-|PastPlInd+2PastSgInd|V',
  #'freusan-|ppl|C',
  #'freusan-|ppl|V',
  'freusan-|PresPlInd|C',
  #'freusan-|PresPlInd|V',
  'freusan-|PresSgInd|C',
  'freusan-|PresSgInd|V',
  'keusan-|1+3PastSgInd|C',
  #'keusan-|1+3PastSgInd|V',
  #'keusan-|PastPlInd+2PastSgInd|C',
  'keusan-|PastPlInd+2PastSgInd|V',
  'keusan-|ppl|C',
  #'keusan-|ppl|V',
  #'keusan-|PresPlInd|C',
  #'keusan-|PresPlInd|V',
  'keusan-|PresSgInd|C',
  'keusan-|PresSgInd|V',
  'leusan-|1+3PastSgInd|C',
  #'leusan-|1+3PastSgInd|V',
  #'leusan-|PastPlInd+2PastSgInd|C',
  'leusan-|PastPlInd+2PastSgInd|V',
  #'leusan-|ppl|C',
  #'leusan-|ppl|V',
  'leusan-|PresPlInd|C',
  #'leusan-|PresPlInd|V',
  'leusan-|PresSgInd|C',
  'leusan-|PresSgInd|V',
  #'līhwan-|1+3PastSgInd|C',
  'līhwan-|1+3PastSgInd|V',
  'līhwan-|PastPlInd+2PastSgInd|C',
  #'līhwan-|PastPlInd+2PastSgInd|V',
  'līhwan-|ppl|C',
  'līhwan-|ppl|V',
  #'rīsan-|1+3PastSgInd|C',
  'rīsan-|1+3PastSgInd|V',
  'rīsan-|PastPlInd+2PastSgInd|C',
  #'rīsan-|PastPlInd+2PastSgInd|V',
  'rīsan-|ppl|C',
  'rīsan-|ppl|V',
  #'sīhwan-|ppl|C',
  #'sīhwan-|ppl|V',
  'teuhan-|1+3PastSgInd|C',
  #'teuhan-|1+3PastSgInd|V',
  #'teuhan-|PastPlInd+2PastSgInd|C',
  'teuhan-|PastPlInd+2PastSgInd|V',
  'teuhan-|ppl|C',
  'teuhan-|ppl|V',
  'teuhan-|PresPlInd|C',
  #'teuhan-|PresPlInd|V',
  'teuhan-|PresSgInd|C',
  'teuhan-|PresSgInd|V',
  'tīhan-|1+3PastSgInd|C',
  'tīhan-|1+3PastSgInd|V',
  #'tīhan-|PastPlInd+2PastSgInd|C',
  #'tīhan-|PastPlInd+2PastSgInd|V',
  'tīhan-|ppl|C',
  'tīhan-|ppl|V'
  #'þinhan-|1+3PastSgInd|C',
  #'þinhan-|1+3PastSgInd|V',
  #'þinhan-|ppl|C',
  #'þinhan-|ppl|V'
)

#verner.df <- droplevels(verner.df[verner.df$lemma.macroinfl.id %in% categories.to.keep,])

change.props <- prop.table(xtabs( ~ lemma.macroinfl.id + response, verner.df),1)[,2]

categories.to.keep <- names(change.props)[which(change.props>0)]

verner.df <- droplevels(verner.df[verner.df$lemma.macroinfl.id %in% categories.to.keep,])

verner.df$date.norm <- verner.df$date

verner.df$date <- (verner.df$date-mean(verner.df$date))/(2*sd(verner.df$date))

saveRDS(verner.df,file='../models/verner_data_for_analysis.Rds')

