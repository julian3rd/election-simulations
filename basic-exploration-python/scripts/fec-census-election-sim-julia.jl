#!/usr/bin/env julia

# parallel implemention of initial/basic Python simulations in Julia

dataset = "~/GitHub/election-simulations/basic-exploration-python/data/obama-prediction-net-money-complete.csv"
electoral = "~/GitHub/election-simulations/basic-exploration-python/data/electoral_votes.csv"

using DataFrames

obama_net_data = readtable(expanduser(dataset), header = true);

electoral_votes = readtable(expanduser(electoral));

# sort money DataFrame and electoral voted DataFrame
# by state name to ensure order

electoral_votes = sort(electoral_votes);

obama_net_data = sort(obama_net_data);

#--------------------------------------------------------------------

# election simulation models
using GLM

# simle models with money and region
model0 = glm(Winner2008 ~ pctDollars + pop_density_scale,
             obama_net_data, Binomial(), LogitLink());

model1 = glm(Winner2008 ~ pctDollars + economic_region_num,
             obama_net_data, Binomial(), LogitLink());

model2 = glm(Winner2008 ~ pctDollars + census_region_num,
             obama_net_data, Binomial(), LogitLink());

model3 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num,
             obama_net_data, Binomial(), LogitLink());

model4 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num,
             obama_net_data, Binomial(), LogitLink());


# models that incorporate money, region, demographic information

model5 = glm(Winner2008 ~ pctDollars + pop_density_scale +
               economic_region_num + sex_ratio_scale,
             obama_net_data, Binomial(), LogitLink());

model6 = glm(Winner2008 ~ pctDollars + pop_density_scale +
               census_region_num + sex_ratio_scale,
             obama_net_data, Binomial(), LogitLink());

model7 = glm(Winner2008 ~ pctDollars + pop_density_scale +
               economic_region_num + sex_ratio_scale + under_18_count_scale,
             obama_net_data, Binomial(), LogitLink());

model8 = glm(Winner2008 ~ pctDollars + pop_density_scale +
               census_region_num + sex_ratio_scale + under_18_count_scale,
             obama_net_data, Binomial(), LogitLink());

model9 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
               sex_ratio_scale + under_18_count_scale +
               forty_five_to_sixty_four_count_scale, obama_net_data,
             Binomial(), LogitLink());

model10 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                sex_ratio_scale + under_18_count_scale +
                forty_five_to_sixty_four_count_scale, obama_net_data,
              Binomial(), LogitLink());

model11 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                sex_ratio_scale + under_18_count_scale +
                forty_five_to_sixty_four_count_scale + sixty_five_over_count_scale,
              obama_net_data, Binomial(), LogitLink());

model12 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                sex_ratio_scale + under_18_count_scale +
                forty_five_to_sixty_four_count_scale + sixty_five_over_count_scale,
              obama_net_data, Binomial(), LogitLink());

model13 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                median_age_scale, obama_net_data,
              Binomial(), LogitLink());

model14 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                median_age_scale, obama_net_data,
              Binomial(), LogitLink());

# models that icorporate money, region, household information

model15 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                total_households_scale, obama_net_data,
              Binomial(), LogitLink());

model16 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                total_households_scale, obama_net_data,
              Binomial(), LogitLink());

model17 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                husband_wife_household_scale, obama_net_data,
              Binomial(), LogitLink());

model18 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                husband_wife_household_scale, obama_net_data,
              Binomial(), LogitLink());

model19 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                husband_wife_child_under_18_scale, obama_net_data,
              Binomial(), LogitLink());

model20 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                husband_wife_child_under_18_scale, obama_net_data,
              Binomial(), LogitLink());

model21 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                female_household_scale, obama_net_data,
              Binomial(), LogitLink());

model22 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                female_household_scale, obama_net_data,
              Binomial(), LogitLink());

model23 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                female_child_under_18_scale, obama_net_data,
              Binomial(), LogitLink());

model24 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                female_child_under_18_scale, obama_net_data,
              Binomial(), LogitLink());

model25 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                male_household_scale, obama_net_data,
              Binomial(), LogitLink());

model26 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                male_household_scale, obama_net_data,
              Binomial(), LogitLink());

model27 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                male_child_under_18_scale, obama_net_data,
              Binomial(), LogitLink());

model28 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                male_child_under_18_scale, obama_net_data,
              Binomial(), LogitLink());

model29 = glm(Winner2008 ~ pctDollars + pop_density_scale + economic_region_num +
                one_person_nonfamily_scale + one_person_sixty_five_older_scale +
                one_person_at_least_two_scale, obama_net_data,
              Binomial(), LogitLink());

model30 = glm(Winner2008 ~ pctDollars + pop_density_scale + census_region_num +
                one_person_nonfamily_scale + one_person_sixty_five_older_scale +
                one_person_at_least_two_scale, obama_net_data,
              Binomial(), LogitLink());

# omnibus household data goes here (does not converge)

model31 = glm(Winner2008 ~  pctDollars + pop_density_scale + economic_region_num + husband_wife_household_scale +
              female_household_scale + male_household_scale + one_person_nonfamily_scale +
                one_person_sixty_five_older_scale + one_person_at_least_two_scale,
              obama_net_data, Binomial(), LogitLink());

model32 = glm(Winner2008 ~  pctDollars + pop_density_scale + census_region_num + husband_wife_household_scale +
              female_household_scale + male_household_scale + one_person_nonfamily_scale +
                one_person_sixty_five_older_scale + one_person_at_least_two_scale,
              obama_net_data, Binomial(), LogitLink());

#--------------------------------------------------------------------
# model predictions: chance of winning a state based on logisitic regression
model0_predict = predict(model0);
model1_predict = predict(model1);
model2_predict = predict(model2);
model3_predict = predict(model3);
model4_predict = predict(model4);
model5_predict = predict(model5);
model6_predict = predict(model6);
model7_predict = predict(model7);
model8_predict = predict(model8);
model9_predict = predict(model9);
model10_predict = predict(model10);
model11_predict = predict(model11);
model12_predict = predict(model12);
model13_predict = predict(model13);
model14_predict = predict(model14);
model15_predict = predict(model15);
model16_predict = predict(model16);
model17_predict = predict(model17);
model18_predict = predict(model18);
model19_predict = predict(model19);
model20_predict = predict(model20);
model21_predict = predict(model21);
model22_predict = predict(model22);
model23_predict = predict(model23);
model24_predict = predict(model24);
model25_predict = predict(model25);
model26_predict = predict(model26);
model27_predict = predict(model27);
model28_predict = predict(model28);
model29_predict = predict(model29);
model30_predict = predict(model30);



#--------------------------------------------------------------------
# election simulation function

function simulate_election(predictions, n_sim, votes)
  # simulate_election(predictions, n_sim, votes)
  # simulate an election outcome using predictions from
  # a GLM n_sim times. returns a matrix with wins, losses
  # and electroal college votes allocated per simulation
  srand(29393848)
  prob_matrix = zeros(length(predictions), n_sim)
  vote_matrix = zeros(length(predictions), n_sim)
  for (row, state) in zip(1:51, 1:n_sim)
    prob_matrix[row, :] = transpose(rand(Binomial(1, predictions[row]), n_sim))
    vote_matrix[row, :] = ifelse(prob_matrix[row, :] .== 1, votes[row, :Votes], 0)
  end
  return prob_matrix, vote_matrix
end

#--------------------------------------------------------------------
# simulations

model0_probs, model0_votes = simulate_election(model0_predict, 1000001, electoral_votes);
model1_probs, model1_votes = simulate_election(model1_predict, 1000001, electoral_votes);
model2_probs, model2_votes = simulate_election(model2_predict, 1000001, electoral_votes);
model3_probs, model3_votes = simulate_election(model3_predict, 1000001, electoral_votes);
model4_probs, model4_votes = simulate_election(model4_predict, 1000001, electoral_votes);
model5_probs, model5_votes = simulate_election(model5_predict, 1000001, electoral_votes);
model6_probs, model6_votes = simulate_election(model6_predict, 1000001, electoral_votes);
model7_probs, model7_votes = simulate_election(model7_predict, 1000001, electoral_votes);
model8_probs, model8_votes = simulate_election(model8_predict, 1000001, electoral_votes);
model9_probs, model9_votes = simulate_election(model9_predict, 1000001, electoral_votes);
model10_probs, model10_votes = simulate_election(model10_predict, 1000001, electoral_votes);
model11_probs, model11_votes = simulate_election(model11_predict, 1000001, electoral_votes);
model12_probs, model12_votes = simulate_election(model12_predict, 1000001, electoral_votes);
model13_probs, model13_votes = simulate_election(model13_predict, 1000001, electoral_votes);
model14_probs, model14_votes = simulate_election(model14_predict, 1000001, electoral_votes);
model15_probs, model15_votes = simulate_election(model15_predict, 1000001, electoral_votes);
model16_probs, model16_votes = simulate_election(model16_predict, 1000001, electoral_votes);
model17_probs, model17_votes = simulate_election(model17_predict, 1000001, electoral_votes);
model18_probs, model18_votes = simulate_election(model18_predict, 1000001, electoral_votes);
model19_probs, model19_votes = simulate_election(model19_predict, 1000001, electoral_votes);
model20_probs, model20_votes = simulate_election(model20_predict, 1000001, electoral_votes);
model21_probs, model21_votes = simulate_election(model21_predict, 1000001, electoral_votes);
model22_probs, model22_votes = simulate_election(model22_predict, 1000001, electoral_votes);
model23_probs, model23_votes = simulate_election(model23_predict, 1000001, electoral_votes);
model24_probs, model24_votes = simulate_election(model24_predict, 1000001, electoral_votes);
model25_probs, model25_votes = simulate_election(model25_predict, 1000001, electoral_votes);
model26_probs, model26_votes = simulate_election(model26_predict, 1000001, electoral_votes);
model27_probs, model27_votes = simulate_election(model27_predict, 1000001, electoral_votes);
model28_probs, model28_votes = simulate_election(model28_predict, 1000001, electoral_votes);
model29_probs, model29_votes = simulate_election(model29_predict, 1000001, electoral_votes);
model30_probs, model30_votes = simulate_election(model30_predict, 1000001, electoral_votes);


#--------------------------------------------------------------------
# plotting simulations
# implemented via PyPlot for consistency
using PyPlot

function plot_simulation(vote_totals, n_bins)
  # plot_simulation(vote_totals, n_bins)
  # plot_simulation plots the results of the election simulations
  # for n_bins of the distribution of vote totals
  # use vec() to transpose and turn into 1D array
  win_sum = vec(sum(vote_totals, 1));
  win_prob = sum(ifelse(win_sum .>= 269, 1, 0) / length(win_sum))
  # use vec() function to convert into a column vector
  spread = percentile(vec(win_sum), 95) - percentile(vec(win_sum), 5)
  PyPlot.plt.hist(win_sum, n_bins)
  plt.title(@sprintf "Chance of Obama victory: %0.3f; spread:%d votes; %d bins" win_prob spread n_bins)
  plt.xlabel("Obama Electoral College votes")
  plt.ylabel("Count")
  plt.axvline(269, color = "k", lw = 3)
  plt.axvline(332, color = "r", linestyle = "--", lw = 3)
  plt.legend(["winning threshold", "2012 outcome", "simulation"], loc = "best")
end

plot_simulation(model0_votes, 30)
plot_simulation(model1_votes, 30)
plot_simulation(model2_votes, 30)
plot_simulation(model3_votes, 30)
plot_simulation(model4_votes, 30)
plot_simulation(model5_votes, 30)
plot_simulation(model6_votes, 30)
plot_simulation(model7_votes, 30)
plot_simulation(model8_votes, 30)
plot_simulation(model9_votes, 30)
plot_simulation(model10_votes, 30)

plot_simulation(model11_votes, 30)
plot_simulation(model12_votes, 30)
plot_simulation(model13_votes, 30)
plot_simulation(model14_votes, 30)
plot_simulation(model15_votes, 30)
plot_simulation(model16_votes, 30)
plot_simulation(model17_votes, 30)
plot_simulation(model18_votes, 30)
plot_simulation(model19_votes, 30)
plot_simulation(model20_votes, 30)

plot_simulation(model21_votes, 30)
plot_simulation(model22_votes, 30)
plot_simulation(model23_votes, 30)
plot_simulation(model24_votes, 30)
plot_simulation(model25_votes, 30)
plot_simulation(model26_votes, 30)
plot_simulation(model27_votes, 30)
plot_simulation(model28_votes, 30)
plot_simulation(model29_votes, 30)
plot_simulation(model30_votes, 30)

