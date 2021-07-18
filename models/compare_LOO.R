require(brms)

load('BRMS_fit_lin.Rmd')

loo(fit)

load('BRMS_fit_quad.Rmd')

loo(fit)

load('BRMS_fit_cub_no_quad.Rmd')

loo(fit)

load('BRMS_fit_cub.Rmd')

loo(fit)

load('BRMS_fit_null.Rmd')

loo(fit)

load('BRMS_fit_cub_class.Rmd')

loo(fit)

load('BRMS_fit_cub_only_class.Rmd')

loo(fit)