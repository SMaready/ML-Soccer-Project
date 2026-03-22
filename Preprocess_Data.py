import csv
import random


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
	altered_data = [['Home_L3_Pts', 'Home_L3_Goals', 'Home_L3_EnemyGoals', 'Home_L3_Wins', 'Home_L3_Losses', 'Home_L3_HomeWins', 'Home_L5_Pts', 'Home_L5_Goals', 'Home_L5_EnemyGoals', 'Home_L5_Wins', 'Home_L5_Losses', 'Home_L5_HomeWins', 'Home_L10_Pts', 'Home_L10_Goals', 'Home_L10_EnemyGoals', 'Home_L10_Wins', 'Home_L10_Losses', 'Home_L10_HomeWins', 'Away_L3_Pts', 'Away_L3_Goals', 'Away_L3_EnemyGoals', 'Away_L3_Wins', 'Away_L3_Losses', 'Away_L3_HomeWins', 'Away_L5_Pts', 'Away_L5_Goals', 'Away_L5_EnemyGoals', 'Away_L5_Wins', 'Away_L5_Losses', 'Away_L5_HomeWins', 'Away_L10_Pts', 'Away_L10_Goals', 'Away_L10_EnemyGoals', 'Away_L10_Wins', 'Away_L10_Losses', 'Away_L10_HomeWins', 'Target_Did_Home_Win']]
	
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

			altered_data.append(last3_team1 + last5_team1 + last10_team1 + last3_team2 + last5_team2 + last10_team2 + [target])

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
	
	#This function changes the dataset: It should contain 
	better_soccer_data = last_ten_features(soccer_data)

	print("======================\n*Feature Engineering Check: ", len(better_soccer_data), "data samples,", (len(better_soccer_data[0])-1), "features\n", better_soccer_data[0], "\n", better_soccer_data[1], "\n======================\n")




	




		



	
	

if __name__ == "__main__":
	main()