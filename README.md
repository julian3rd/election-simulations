# Overview
This repo contains files for an electiom simulation data science project I used to teach myself Python and simulating outcomes in general. I received most of the information from the ['Desperately Seekinng Silver'](http://nbviewer.ipython.org/github/cs109/content/blob/master/HW2.ipynb) homework and tutorial. They are retroactive simulations/analyses for the 2012 US Presidential election, but the methods could be applied to future elections as well.  

## Basic simulations
The baic simulations  use the percentage of money donated to the final two candidates and demographic information to calculate the probability of a candidate winning a particular state. Use of the R package `BreakoutDetection` was also used to determine when there were especially large spikes in net cash flow, expenditures, or donations. While the initial simulations were implemented with  combination of Python and R, a parallel implementation was also performed in Julia.  

## Ongoing simulations
In order to create more sophisticated models, ongoing projects will use a combination of polling data, contribution information and weighting importance by date. These will be updated periodically (meaning, as I get to it).