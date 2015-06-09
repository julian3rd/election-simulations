# Summary
This folder contains the source code for the initial retroactive simulations and analyses. The summaries of the main FEC dataset are performed in Python with additional summarization and scaling of predictors done in R. The simulations themselves are implemented in Python. Additional analyses are provided via the `BreakoutDetection` R package.

# Sources
The project design was motivated by the examples in Wes McKinney's book *Python for Data Analysis* and the IPython notebook [Desperately seeking Silver](http://nbviewer.ipython.org/github/cs109/content/blob/master/HW2.ipynb). Many of the code manipulations, summaries and functions for the Python code are copied or modified from those sources. Several datasets from the latter were also used to assist in creating the simulations.

## Datasets

### Simulation/prediction
`obama-prediction-net-money-complete`: used for predictions  
`2008results`, `2012results`: results from 2008 and 2012 elections  
`electoral_votes`: Electoral College votes allocated to each state  
`net-money-classifier-success`: success in predicting outcome of 2012 election for each model  
`net-money-probabilities`: probability of Obama winning a state for each model  
`obama-net-money-summary`: text file with performance of each model

### Time series/breakout detection analysis
For each day in the FEC dataset and for each campaign, summaries of the amount of money for each state was calcualted. These values were used to visualize the time course of cash flow and any breakouts in net cash flow, donations, or expenditures.
`fec-data-net-contributions`: time series of net cash flow  
`fec-data-census-regions-net-contributions`: time series of net cash flow with Census Bureau region labels  
`fec-data-economic-regions-net-contributions`: time series of net cash flow with Bureau of Economic Analysis region labels  

`donation-data-candidate-idx`: time series of donations  
`donation-data-census-regions-candidate-idx`: time series of donations with Census Bureau region labels  
`donation-data-economic-regions-candidate-idx`: time series of donations with Bureau of Economic Analysis region labels  

`expenditure-data-candidate-idx`: time series of expenditures  
`expenditure-data-census-regions-candidate-idx`: time series of expenditures with Census Bureau region labels  
`expenditure-data-economic-regions-candidate-idx`: time series of expenditures with Bureau of Economic Analysis region labels  

## Scripts
`fec-data-exploration-repo-version.py`: Python scripts to implement summaries and basic plots of the data  
`complete-data-setup.R`: summarizes and sets up data for simulations in Python; calculation of percentages and scaling of predictors is implemented here  
`fec-census-election-simulation.py`: Python script that implements the simulations  
`fec-r-breakout-analysis.R`: implementation of time series plots and breakout detection

## Output and Notebooks
`obama-net-money-summary.class_result.class_result`: text file containing the performance of each of the models implemented  
`fec-r-breakout-analysis.pdf`: PDF file with commands from breakout detection R script
