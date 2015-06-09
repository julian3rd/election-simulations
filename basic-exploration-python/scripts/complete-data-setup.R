#!/usr/bin/env Rscript

# Script used to calculate percentage of money
# donated and spent to the campaigns of the two main
# candidates for the 2012 US Presidential election.
# Some columns are also scaled in order to facilitate fitting
# logistic regression models (done in Python).
# Data are set up to be plotted via the googleVis 
# library; future iterations will use different maps,
# e.g., hexbins or some other method.

# chloropleth maps for FEC data combined with census data

# what to plot: 
# 1. if candidate won the state
# 2. absolute amount
# 3. scaled amount
# 4. log10 amount
# 5. log10 amount scaled
# 6. amount by population
# 7. amount by density
# 8. amount by electoral votes
# 9. log10 amount by population
# 10. log10 amount by density
# 11. log10 amount by electoral votes
# 12. scaled amount by population
# 13. scaled amount by density
# 14. scaled amount by electoral votes
# 15. log10 scaled amount by population
# 16. log10 scaled amount by density
# 17. log10 scaled amount by electoral votes

# all scaling is done via z-score


# read in, format state data for chloropleth maps -------------------------

# all FEC data

data.dir <- '~/GitHub/election-simulations/basic-exploration-python/data'

fec.data.net.contributions.state <- 
  read.csv(file.path(data.dir,'fec-data-net-contributions-state.csv'),
           stringsAsFactors = FALSE)

# remove X column (row indices from pandas)

fec.data.net.contributions.state$X <- NULL

# rename columns to something friendlier

fec.data.net.contributions.state <- 
  dplyr::rename(fec.data.net.contributions.state, Candidate = cand_nm,
                Date = contb_receipt_dt_format, Dollars = contb_receipt_amt)



# converting Date colums to actual dates

fec.data.net.contributions.state$Date <- 
  as.Date(fec.data.net.contributions.state$Date)

# restrict timeline to just before election

fec.data.net.contributions.state <- 
  subset(fec.data.net.contributions.state, Date <= '2012-11-05')



# compute totals and percentages for each candidate
library(plyr)

campaign.total <- 
  ddply(fec.data.net.contributions.state, .(contbr_st), 
        summarize, sumState = sum(Dollars))

campaign.total <- campaign.total[rep(1:nrow(campaign.total), each = 2), ]


campaign.cand.state.total <- 
  ddply(fec.data.net.contributions.state, .(Candidate, contbr_st), 
        summarize, sumDollars = sum(Dollars))

campaign.cand.state.total <- arrange(campaign.cand.state.total, contbr_st)



# percentage of money by state for each candidate
campaign.cand.state.total$pctDollars <- 
  campaign.cand.state.total$sumDollars/campaign.total$sumState



# separate for each candidate
# obama data.frame ultimately used for prediction

obama.campaign.pct.total <- 
  subset(campaign.cand.state.total, Candidate == 'Obama, Barack')

obama.campaign.pct.total <- droplevels(obama.campaign.pct.total)

demographic.columns <- 
  colnames(fec.data.net.contributions.state)[c(1, 3:38)]

# obama campaign net
obama.net.state <- 
  subset(fec.data.net.contributions.state, Candidate == 'Obama, Barack')

obama.net.state <- 
  ddply(obama.net.state, .variables = demographic.columns, 
        summarise, Dollars = (sum(Dollars)))

obama.net.state <- arrange(obama.net.state, state_name)

obama.net.state <- droplevels(obama.net.state)

obama.net.state$state_name <- as.character(obama.net.state$state_name)

obama.net.state$amount.scale <- scale(obama.net.state$Dollars)
obama.net.state$logDollars <- log10(obama.net.state$Dollars)
obama.net.state$logDollars.scale <- scale(obama.net.state$logDollars)

obama.net.state$dollarsPop <- 
  obama.net.state$Dollars/obama.net.state$population

obama.net.state$dollarsDensity <- 
  obama.net.state$Dollars/obama.net.state$pop_density

obama.net.state$dollarsElecVotes <- 
  obama.net.state$Dollars/obama.net.state$electoral_votes

obama.net.state$logDollarsPop <- 
  obama.net.state$logDollars/obama.net.state$population

obama.net.state$logDollarsDensity <- 
  obama.net.state$logDollars/obama.net.state$pop_density

obama.net.state$logDollarsElecVotes <- 
  obama.net.state$logDollars/obama.net.state$electoral_votes

obama.net.state$dollarsPop.scale <- scale(obama.net.state$dollarsPop)
obama.net.state$dollarsDensity.scale <- scale(obama.net.state$dollarsDensity)
obama.net.state$dollarsElecVotes.scale <- scale(obama.net.state$dollarsElecVotes)

obama.net.state$logDollarsPop.scale <- scale(obama.net.state$logDollarsPop)

obama.net.state$logDollarsDensity.scale <- 
  scale(obama.net.state$logDollarsDensity)

obama.net.state$logDollarsElecVotes.scale <- 
  scale(obama.net.state$logDollarsElecVotes)

obama.net.state <- arrange(obama.net.state, contbr_st)

obama.net.state$sumDollars <- obama.campaign.pct.total$sumDollars
obama.net.state$pctDollars <- obama.campaign.pct.total$pctDollars



# chloropeth map settings -------------------------------------------------

library(googleVis)


obama.map.options  <- 
  list(region = 'US', displayMode = 'regions', 
       resolution = 'provinces', colors ="['#1f78b4']")


# obama net ---------------------------------------------------------------


obama.net.dollars.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'Dollars', options = obama.map.options)

obama.net.dollars.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'amount.scale', options = obama.map.options)

obama.net.log.dollars.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollars', options = obama.map.options)

obama.net.log.dollars.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollars.scale', options = obama.map.options)

obama.net.dollars.pop.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'dollarsPop', options = obama.map.options)

obama.net.dollars.density.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'dollarsDensity', options = obama.map.options)

obama.net.dollars.electoral.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'dollarsElecVotes', options = obama.map.options)

obama.net.log.dollars.pop.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollarsPop', options = obama.map.options)

obama.net.log.dollars.density.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollarsDensity', options = obama.map.options)

obama.net.log.dollars.electoral.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollarsElecVotes', options = obama.map.options)

obama.net.dollars.pop.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'dollarsPop.scale', options = obama.map.options)

obama.net.dollars.density.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'dollarsDensity.scale', options = obama.map.options)

obama.net.dollars.electoral.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'dollarsElecVotes.scale', 
               options = obama.map.options)

obama.net.log.dollars.pop.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollarsPop.scale', options = obama.map.options)

obama.net.log.dollars.density.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollarsDensity.scale', 
               options = obama.map.options)

obama.net.log.dollars.electoral.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'logDollarsElecVotes.scale', 
               options = obama.map.options)

obama.net.pct.dollars.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'pctDollars', 
               options = obama.map.options)

obama.net.pct.dollars.scale.map <- 
  gvisGeoChart(obama.net.state, locationvar = 'state_name', 
               colorvar = 'pctDollars.scale', 
               options = obama.map.options)

# viewer(plot(obama.net.dollars.map))
# viewer(plot(obama.net.dollars.scale.map))
# 
# viewer(plot(obama.net.log.dollars.map))
# viewer(plot(obama.net.log.dollars.scale.map))
# 
# viewer(plot(obama.net.dollars.pop.map))
# viewer(plot(obama.net.dollars.density.map))
# viewer(plot(obama.net.dollars.electoral.map))
# 
# viewer(plot(obama.net.log.dollars.pop.map))
# viewer(plot(obama.net.log.dollars.density.map))
# viewer(plot(obama.net.log.dollars.electoral.map))
# 
# viewer(plot(obama.net.dollars.pop.scale.map))
# viewer(plot(obama.net.dollars.density.scale.map))
# viewer(plot(obama.net.dollars.electoral.scale.map))
# 
# viewer(plot(obama.net.log.dollars.pop.scale.map))
# viewer(plot(obama.net.log.dollars.density.scale.map))
# viewer(plot(obama.net.log.dollars.electoral.scale.map))
# 
# 
# viewer(plot(obama.net.pct.dollars.map))
# viewer(plot(obama.net.pct.dollars.scale.map))


# join obama data with 2008 results ---------------------------------------

# join obama data to 2008 results (for export and prediction)
results.2008 <- 
  read.csv(file.path(data.dir, '2008results.csv'), stringsAsFactors = FALSE)

results.2008 <- arrange(results.2008, State)

# net data
obama.net.state$population.scale <- scale(obama.net.state$population)
obama.net.state$pop_density.scale <- scale(obama.net.state$pop_density)
obama.net.state$males.scale <- scale(obama.net.state$males)
obama.net.state$females.scale <- scale(obama.net.state$females)
obama.net.state$sex_ratio.scale <- scale(obama.net.state$sex_ratio)

obama.net.state$under_18_count.scale <- scale(obama.net.state$under_18_count)
obama.net.state$under_18_pct.scale <- scale(obama.net.state$under_18_pct)

obama.net.state$eighteen_to_forty_four_count.scale <- 
  scale(obama.net.state$eighteen_to_forty_four_count)

obama.net.state$eighteen_to_forty_four_pct.scale <- 
  scale(obama.net.state$eighteen_to_forty_four_pct)

obama.net.state$forty_five_to_sixty_four_count.scale <- 
  scale(obama.net.state$forty_five_to_sixty_four_count)

obama.net.state$forty_five_to_sixty_four_pct.scale <- 
  scale(obama.net.state$forty_five_to_sixty_four_pct)

obama.net.state$sixty_five_over_count.scale <- 
  scale(obama.net.state$sixty_five_over_count)

obama.net.state$sixty_five_over_pct.scale <- 
  scale(obama.net.state$sixty_five_over_pct)

obama.net.state$median_age.scale <- scale(obama.net.state$median_age)

obama.net.state$total_households.scale <- 
  scale(obama.net.state$total_households)

obama.net.state$husband_wife_household.scale <- 
  scale(obama.net.state$husband_wife_household)

obama.net.state$husband_wife_child_under_18.scale <- 
  scale(obama.net.state$husband_wife_child_under_18)

obama.net.state$female_household.scale <- 
  scale(obama.net.state$female_household)

obama.net.state$female_child_under_18.scale <- 
  scale(obama.net.state$female_child_under_18)

obama.net.state$male_household.scale <- 
  scale(obama.net.state$male_household)

obama.net.state$male_child_under_18.scale <- 
  scale(obama.net.state$male_child_under_18)

obama.net.state$one_person_nonfamily.scale <- 
  scale(obama.net.state$one_person_nonfamily)

obama.net.state$one_person_sixty_five_older.scale <- 
  scale(obama.net.state$one_person_sixty_five_older)

obama.net.state$one_person_at_least_two.scale <- 
  scale(obama.net.state$one_person_at_least_two)

obama.net.state$avg_per_family.scale <- 
  scale(obama.net.state$avg_per_family)

obama.net.state$avg_per_householdy.scale <- 
  scale(obama.net.state$avg_per_household)

obama.net.state$eighty_five_over_count.scale <- 
  scale(obama.net.state$eighteen_to_forty_four_count)

obama.net.state$eighty_five_over_pct.scale <- 
  scale(obama.net.state$eighteen_to_forty_four_pct)

obama.net.state.results.2008 <- 
  dplyr::bind_cols(obama.net.state, results.2008)

obama.net.state.results.2008$DemMargin <- 
  obama.net.state.results.2008$Obama.Pct - 
  obama.net.state.results.2008$McCain.Pct

obama.net.state.results.2008$DemMargin.scale <- 
  scale(obama.net.state.results.2008$DemMargin)

obama.net.state.results.2008$X <- NULL

obama.net.state.results.2008$Winner2008 <- 
  ifelse(obama.net.state.results.2008$Obama.Pct > obama.net.state.results.2008$McCain.Pct,
         1, 0)

# turn census and economic regions into factors
# use numeric values for regressions later

obama.net.state.results.2008$census_region <- 
  as.factor(obama.net.state.results.2008$census_region)

obama.net.state.results.2008$economic_region <- 
  as.factor(obama.net.state.results.2008$economic_region)

obama.net.state.results.2008$census_region_num <- 
  as.numeric(obama.net.state.results.2008$census_region)

obama.net.state.results.2008$economic_region_num <- 
  as.numeric(obama.net.state.results.2008$economic_region)

obama.net.state.results.2008$winner_binary <- 
  ifelse(obama.net.state.results.2008$winner == 'Obama', 1, 0)

write.csv(obama.net.state.results.2008, 
          file.path(data.dir, 'obama-prediction-net-money-complete.csv'),
          row.names = F, na = '')

# save data ---------------------------------------------------------------

output.dir <- 
  '~/GitHub/election-simulations/basic-exploration-python/output'

save.image(file.path(output.dir, 'fec-chloropleth-maps.rda'))
