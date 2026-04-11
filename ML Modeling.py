import csv
import random
from sklearn.linear_model import LogisticRegression
import pickle


from sklearn.ensemble import RandomForestClassifier


def main():
	#Import
	better_soccer_data = []
	with open('Preprocessed-Soccer-Dataset.csv', newline='', encoding='utf-8') as data:
		read = csv.reader(data)
		for x in read:
			better_soccer_data.append(x)
	
	#Data Shuffle
	shuffled_data = better_soccer_data[1:]  # skip header
	random.shuffle(shuffled_data)


	#Train on regular data set
	training_set = []
	testing_set = []

	eighty = int((len(shuffled_data)) * 0.8)
	training_set = shuffled_data[:eighty]
	testing_set  = shuffled_data[eighty:]

	training_labels = []
	for r in training_set: training_labels.append(r.pop())
	testing_labels = []
	for r in testing_set: testing_labels.append(r.pop())

	for i in range(len(training_set)):
		for j in range(len(training_set[i])):
			training_set[i][j] = float(training_set[i][j])

	for i in range(len(testing_set)):
		for j in range(len(testing_set[i])):
			testing_set[i][j] = float(testing_set[i][j])

	#Logistic Regression
	model = LogisticRegression()
	model.fit(training_set, training_labels)
	pickle.dump(model, open('finalized_model_M1.sav', 'wb'))

	# Selecting the best features only, in this case Home L5, L10, Away L5, l10
	INDEX4reduced = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

	#Train on the reduced set of data
	training_setR = []
	testing_setR = []

	for r in training_set:
		rowR = []
		for i in INDEX4reduced:
			rowR.append(r[i])
		training_setR.append(rowR)

	for r in testing_set:
		rowR = []
		for i in INDEX4reduced:
			rowR.append(r[i])
		testing_setR.append(rowR)

	#Logistic Regression2
	model2 = LogisticRegression()
	model2.fit(training_setR, training_labels)
	pickle.dump(model2, open('finalized_model_M2.sav', 'wb'))


	# Random Forest
	randomTrees = RandomForestClassifier(n_estimators=300,max_depth=10,min_samples_split=5,random_state=101)
	randomTrees.fit(training_set, training_labels)


	# Load Models from disk & print()
	load1 = pickle.load(open('finalized_model_M1.sav', 'rb'))
	load2 = pickle.load(open('finalized_model_M2.sav', 'rb'))

	result1 = load1.score(testing_set, testing_labels)
	result2 = load2.score(testing_setR, testing_labels)
	resultTrees = randomTrees.score(testing_set, testing_labels)

	print("Model 1 (Full features) score:    " + str(round(result1 * 100, 2)) + "%")
	print("Model 2 (Reduced features) score: " + str(round(result2 * 100, 2)) + "%")
	# Looks like we get about 60% accuracy for both
	# This means it's learning something from the data, just not much XD

	print("Random Forest (Full features) score: " + str(round(resultTrees * 100, 2)) + "%")
	print(randomTrees.feature_importances_)

if __name__ == "__main__":
	main()