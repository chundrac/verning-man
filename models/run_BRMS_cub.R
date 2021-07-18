require(brms)

verner.df <- readRDS(file='verner_data_for_analysis.Rds')

verner.df <- verner.df[,c(
  'date',
  'dialect.place',
  'PGmc',
  'class',
  'cons',
  'V.C',
  'macroinfl',
  'response',
  'dial.lemma.id',
  'dial.infl.id',
  'lemma.macroinfl.id',
  'dial.exp.out.id'
)]

colnames(verner.df) <- c('date','dialect_ID','lemma','class','cons','V.C','macroinfl','response','dialect_lemma_ID','dialect_infl_ID','lemma_macroinfl_ID','dialect_exp_out_ID')

fit <- brm(formula = response ~ date + I(date^2) + I(date^3) + (1+date+I(date^2)+I(date^3)|dialect_ID) + (1+date+I(date^2)+I(date^3)|dialect_lemma_ID) + (1+date+I(date^2)+I(date^3)|dialect_infl_ID) + (1+date+I(date^2)+I(date^3)|lemma_macroinfl_ID) + (1+date+I(date^2)+I(date^3)|dialect_exp_out_ID), 
           data=verner.df, 
           family=bernoulli(), 
           prior = c(set_prior("normal(0,5)", class = "b"), 
                     set_prior("cauchy(0,1)", class = "sd"), 
                     set_prior("lkj(2)", class = "cor")), warmup = 1000, iter = 2000, chains = 4, control = list(adapt_delta = 0.95))

save.image('BRMS_fit_cub.Rmd')