import csv
import random

def getmean(soccer_data_here): #I adapted this from my Assignment 1, pls don't shoot XD
	meanfirst = True
	mean = []
	missing = []
	for j in range(len(soccer_data_here[0])):
		mean.append(0)
		missing.append(0)

	for i in range(len(soccer_data_here)):
		if meanfirst == True:
			meanfirst = False
			continue
		for j in range(len(soccer_data_here[i])):
			if soccer_data_here[i][j] != '': mean[j] += float(soccer_data_here[i][j])
			else: missing[j] += 1
			
	for j in range(len(mean)):
		mean[j] = mean[j]/((len(soccer_data_here)-1)-missing[j])
		if j != len(mean)-1:
			mean [j] = round(mean[j], 4)
		#print(mean[j])
	#now I have the means XD
	return mean

def pearson(feature, featuremean, target, targetmean):
	dividend = sum((float(feature[i]) - featuremean) * (float(target[i]) - targetmean) for i in range(len(feature)))
	featuredivisor = sum((float(feature[i]) - featuremean) ** 2 for i in range(len(feature)))
	targetdivisor = sum((float(target[i]) - targetmean) ** 2 for i in range(len(feature)))
	
	return dividend / (featuredivisor * targetdivisor) ** 0.5


def get_stats(history, n):
	last_few = history[-n:]
	points = 0
	goals = 0
	enemygoals = 0
	win = 0
	loss = 0
	homewin = 0
	for iterate_guy in last_few:
		points += iterate_guy['points']
		goals += iterate_guy['goals']
		enemygoals += iterate_guy['enemygoals']
		if iterate_guy['points']== 3: win += 1
		if iterate_guy['points']== 0: loss += 1
		if iterate_guy['points']== 3 and iterate_guy['hometeam'] == 1: homewin += 1
	
	return [points, goals, enemygoals, win, loss, homewin]


def last_ten_features(soccer_data_here):
	team_history = {}
	altered_data = [['Home_L3_Pts', 'Home_L3_Goals', 'Home_L3_EnemyGoals', 'Home_L3_Wins', 'Home_L3_Losses', 'Home_L3_HomeWins', 'Home_L5_Pts', 'Home_L5_Goals', 'Home_L5_EnemyGoals', 'Home_L5_Wins', 'Home_L5_Losses', 'Home_L5_HomeWins', 'Home_L10_Pts', 'Home_L10_Goals', 'Home_L10_EnemyGoals', 'Home_L10_Wins', 'Home_L10_Losses', 'Home_L10_HomeWins', 'Away_L3_Pts', 'Away_L3_Goals', 'Away_L3_EnemyGoals', 'Away_L3_Wins', 'Away_L3_Losses', 'Away_L3_HomeWins', 'Away_L5_Pts', 'Away_L5_Goals', 'Away_L5_EnemyGoals', 'Away_L5_Wins', 'Away_L5_Losses', 'Away_L5_HomeWins', 'Away_L10_Pts', 'Away_L10_Goals', 'Away_L10_EnemyGoals', 'Away_L10_Wins', 'Away_L10_Losses', 'Away_L10_HomeWins', 'Outlier?', 'Target_Did_Home_Win']]
	
	for i in range(1, len(soccer_data_here)):
		team1 = soccer_data_here[i][2]
		team2 = soccer_data_here[i][5]

		if team1 not in team_history: team_history[team1] = []
		if team2 not in team_history: team_history[team2] = []

		if len(team_history[team1]) >= 10 and len(team_history[team2]) >= 10:
			last3_team1 = get_stats(team_history[team1], 3)
			last5_team1 = get_stats(team_history[team1], 5)
			last10_team1 = get_stats(team_history[team1], 10)
			last3_team2 = get_stats(team_history[team2], 3)
			last5_team2 = get_stats(team_history[team2], 5)
			last10_team2 = get_stats(team_history[team2], 10)

			target = 0
			if int(soccer_data_here[i][13]) == 3: target = 1

			outlier = 0
			if int(soccer_data_here[i][8]) + int(soccer_data_here[i][9]) >= 8: outlier = 1

			altered_data.append(last3_team1 + last5_team1 + last10_team1 + last3_team2 + last5_team2 + last10_team2 + [outlier]  + [target])

		team_history[team1].append({'points': int(soccer_data_here[i][13]), 'goals': int(soccer_data_here[i][8]), 'enemygoals': int(soccer_data_here[i][9]), 'hometeam': 1})
		team_history[team2].append({'points': int(soccer_data_here[i][14]), 'goals': int(soccer_data_here[i][9]), 'enemygoals': int(soccer_data_here[i][8]), 'hometeam': 0})

	return altered_data



def main():
	soccer_data = [] #Our data as a list of lists (like Assignment 1)
	#I will modify it's contents later

	#This code opens the odd-not csv and turns it into ^list of list^
	headers = []
	first = True
	with open('Soccer-Dataset', 'r') as rawdata:
		atdata = False
		for eachline in rawdata:
			eachline = eachline.strip()
			if eachline.startswith('@ATTRIBUTE'): headers.append(eachline.split()[1])
			if eachline == '@DATA': atdata = True; continue
			if atdata == True:
				if first == True: first = False; soccer_data.append(headers)
				soccer_data.append(eachline.split(','))

	print("======================\n*Data Parse Check:\n", soccer_data[0], "\n", soccer_data[1], "\n======================\n")

	number_of_samples = (len(soccer_data)-1)
	winlosscount = [0, 0, 0]	#Contains the number of wins, draws, and losses: in that order
	winlosspercent = [0, 0, 0]	#Same as ^above^ but percents in decimal (i.e. 0.624354)
	for i in range(len(soccer_data)):
		if soccer_data[i][13] == "3": winlosscount[0] += 1
		if soccer_data[i][13] == "1": winlosscount[1] += 1
		if soccer_data[i][13] == "0": winlosscount[2] += 1
	winlosspercent[0] = winlosscount[0]/number_of_samples
	winlosspercent[1] = winlosscount[1]/number_of_samples
	winlosspercent[2] = winlosscount[2]/number_of_samples
	
	print("======================\n*Home Team Win?:\nWin:", str((round(winlosspercent[0] * 100, 2))) + "%", "\nDraw:", str((round(winlosspercent[1] * 100, 2))) + "%", "\nLoss:", str((round(winlosspercent[2] * 100, 2))) + "%", "\n======================\n")


	#Here I check for missing values. This dataset has no missing values, so no extra preprocessing is needed here!
	emptyvarcount = 0
	for i in range(1, len(soccer_data)):
		for j in range(len(soccer_data[i])):
			if soccer_data[i][j] == '': emptyvarcount += 1
	print("======================\nCheck For Missing Values:\n#+The number of missing/empty values is " + str(emptyvarcount) + "\n======================\n")
	
	dupecount = 0
	sofar = set()
	for i in range(1, len(soccer_data)):
		check = (soccer_data[i][1], soccer_data[i][2], soccer_data[i][5])
		if check in sofar: dupecount += 1
		else: sofar.add(check)
	print("======================\nClean Data:\n#+The number of duplicate entries is " + str(dupecount) + "\n======================\n")
	


	#This function changes the dataset: It should contain data about the
	# last 3/5/10 games and home team win metric
	better_soccer_data = last_ten_features(soccer_data)

	print("======================\n*Feature Engineering Check: ", len(better_soccer_data), "data samples,", (len(better_soccer_data[0])-1), "features\n", better_soccer_data[0], "\n", better_soccer_data[1], "\n======================\n")



	# Pearson Correlation code adapted from my Assignment 1 (Kurtis Volker)
	mean = getmean(better_soccer_data)
	columns = []

	for j in range(len(better_soccer_data[0])):
		columns.append([])
		
	for i in range(len(better_soccer_data)):
		if i == 0: continue
		for j in range(len(better_soccer_data[i])):
			columns[j].append(better_soccer_data[i][j])

	Pcorrelations = []
	for i in range(len(columns)):
		Pcorrelations.append(pearson(columns[i], mean[i], columns[-1], mean[-1]))

	print("======================\n*Pearson Correlations: ",  Pcorrelations,  "\n======================\n")



	threshold = 0.05
	feature_indices = list(range(len(better_soccer_data[0]) - 1))  # exclude target column

	kept_indices   = [i for i in feature_indices if abs(Pcorrelations[i]) >= threshold]
	dropped_indices = [i for i in feature_indices if abs(Pcorrelations[i]) <  threshold]

	# Build the new dataset: kept feature columns + target column (always last)
	target_col_idx = len(better_soccer_data[0]) - 1
	selected_cols  = kept_indices + [target_col_idx]

	selected_data = []
	for i, row in enumerate(better_soccer_data):
		selected_data.append([row[j] for j in selected_cols])

	print("======================")
	print("*Feature Selection:")
	print(f"  Threshold: |r| >= {threshold}")
	print(f"  Features dropped ({len(dropped_indices)}):")
	for idx in dropped_indices:
		print(f"    Feature {idx} ({better_soccer_data[0][idx]}): r = {Pcorrelations[idx]:.4f}")
	print(f"  Features kept: {len(kept_indices)}")
	print(f"  New dataset shape: {len(selected_data)-1} samples x {len(selected_data[0])-1} features")
	print("\n  New headers:", selected_data[0])
	print("======================")


	n_features = len(selected_data[0]) - 1  # exclude target

	# Compute per-feature min and max (skip header row)
	col_min = [float('inf')]  * n_features
	col_max = [float('-inf')] * n_features

	for i in range(1, len(selected_data)):
		for j in range(n_features):
			val = float(selected_data[i][j])
			if val < col_min[j]: col_min[j] = val
			if val > col_max[j]: col_max[j] = val

	# Build normalized dataset (header row stays as strings)
	normalized_data = [selected_data[0][:]]  # copy header

	for i in range(1, len(selected_data)):
		norm_row = []
		for j in range(n_features):
			val   = float(selected_data[i][j])
			denom = col_max[j] - col_min[j]
			norm_row.append(round((val - col_min[j]) / denom, 6) if denom != 0 else 0.0)
		norm_row.append(selected_data[i][-1])  # preserve original target
		normalized_data.append(norm_row)

	print("======================")
	print("*Range Normalization (Min-Max [0, 1]):")
	print(f"  Features normalized: {n_features}  |  Target column preserved")
	print(f"  Sample normalized row [0]: {normalized_data[1]}")
	print("\n  Per-feature ranges (min → max):")
	for j in range(n_features):
		print(f"    {selected_data[0][j]:30s}  min={col_min[j]:.1f}  max={col_max[j]:.1f}")
	print("======================")

	
	with open('soccer_preprocessed.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		for row in normalized_data:
			writer.writerow(row)

	print("Saved soccer_preprocessed.csv!")
	print("Rows:", len(normalized_data) - 1, "| Features:", len(normalized_data[0]) - 1, "| Target: last column")



		



	
	

if __name__ == "__main__":
	main()