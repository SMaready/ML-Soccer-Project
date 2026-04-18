import csv
import random
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, roc_auc_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt



def main():
	
	better_soccer_data = []
	with open('Preprocessed-Soccer-Dataset.csv', newline='', encoding='utf-8') as data:
		read = csv.reader(data)
		for x in read:
			better_soccer_data.append(x)

	print('Rows loaded (including header):', len(better_soccer_data))
	print('Columns:', len(better_soccer_data[0]))
	print('Headers:', better_soccer_data[0])





	data = better_soccer_data[1:]  # skip header row

	eighty = int((len(data)) * 0.8)
	training_set = data[:eighty]
	testing_set  = data[eighty:]

	training_labels = []
	for r in training_set: training_labels.append(r.pop())
	testing_labels = []
	for r in testing_set: testing_labels.append(r.pop())

	# Convert to numbers (float)
	for i in range(len(training_set)):
		for j in range(len(training_set[i])):
			training_set[i][j] = float(training_set[i][j])

	for i in range(len(testing_set)):
		for j in range(len(testing_set[i])):
			testing_set[i][j] = float(testing_set[i][j])

	print('Training rows:', len(training_set))
	print('Testing rows: ', len(testing_set))
	print('Features per row:', len(training_set[0]))



	model = LogisticRegression()
	model.fit(training_set, training_labels)

	pickle.dump(model, open('finalized_model_M1.sav', 'wb'))
	print('Model 1 saved: finalized_model_M1.sav')
	print('Trained on', model.n_features_in_, 'features')





	# Indices of the top features by Pearson correlation (L5 and L10 windows only)
	INDEX4reduced = [6, 7, 8, 9, 10, 11,    # Home L5
					12, 13, 14, 15, 16, 17, # Home L10
					24, 25, 26, 27, 28, 29, # Away L5
					30, 31, 32, 33, 34, 35] # Away L10

	# Build reduced training and testing sets
	training_setR = []
	for r in training_set:
		rowR = []
		for i in INDEX4reduced:
			rowR.append(r[i])
		training_setR.append(rowR)

	testing_setR = []
	for r in testing_set:
		rowR = []
		for i in INDEX4reduced:
			rowR.append(r[i])
		testing_setR.append(rowR)





	model2 = LogisticRegression()
	model2.fit(training_setR, training_labels)

	pickle.dump(model2, open('finalized_model_M2.sav', 'wb'))
	print('Model 2 saved: finalized_model_M2.sav')
	print('Trained on', model2.n_features_in_, 'features')



	knn_full = KNeighborsClassifier(n_neighbors=15)
	knn_full.fit(training_set, training_labels)
	knn_score = knn_full.score(testing_set, testing_labels)
	print(f'KNN(k=15): {round(knn_score * 100, 2)}%')

	pickle.dump(knn_full, open('knn_full.sav', 'wb'))
	print('KNN Model on Full Feature Set saved: knn_full.sav')
	print('Trained on', knn_full.n_features_in_, 'features')




	naive_full = GaussianNB()
	naive_full.fit(training_set, training_labels)
	gb_score = naive_full.score(testing_set, testing_labels)
	print(f'Gaussian Naive Bayes: {round(gb_score * 100, 2)}%')

	pickle.dump(naive_full, open('naive_bayes_full.sav', 'wb'))
	print('Gaussian Naive Bayes Model on Full Feature Set saved: naive_bayes_full.sav')
	print('Trained on', naive_full.n_features_in_, 'features')



	randomTrees = RandomForestClassifier(n_estimators=300,max_depth=10,min_samples_split=5,random_state=101)
	randomTrees.fit(training_set, training_labels)

	resultTrees = randomTrees.score(testing_set, testing_labels)

	pickle.dump(randomTrees, open('randomTrees.sav', 'wb'))
	print("Random Forest (Full features) score: " + str(round(resultTrees * 100, 2)) + "%")
	print(randomTrees.feature_importances_)


	load1 = pickle.load(open('finalized_model_M1.sav', 'rb'))
	load2 = pickle.load(open('finalized_model_M2.sav', 'rb'))

	result1 = load1.score(testing_set, testing_labels)
	result2 = load2.score(testing_setR, testing_labels)

	print('Model 1 (Full features) score:    ' + str(round(result1 * 100, 2)) + '%')
	print('Model 2 (Reduced features) score: ' + str(round(result2 * 100, 2)) + '%')
		# Looks like we get about 60% accuracy for both
		# This means it's learning something from the data, just not much XD




	dtree = DecisionTreeClassifier(max_depth=5, min_samples_split=5, random_state=101)
	dtree.fit(training_set, training_labels)

	dtree_score = dtree.score(testing_set, testing_labels)
	print(f'Decision Tree: {round(dtree_score * 100, 2)}%')

	pickle.dump(dtree, open('decision_tree.sav', 'wb'))
	print('Decision Tree saved: decision_tree.sav')
	print('Trained on', dtree.n_features_in_, 'features')



	# The score for each of the ML techniques were calculated in cells above

	print('Logistic Regression score: ' + str(round(result1 * 100, 2)) + '%')
	print(f'KNN score (k=15): {round(knn_score * 100, 2)}%')
	print(f'Gaussian Naive Bayes: {round(gb_score * 100, 2)}%')
	print("Random Forest score: " + str(round(resultTrees * 100, 2)) + "%")
	print(f'Decision Tree: {round(dtree_score * 100, 2)}%')

	models = ['Logistic Regression', 'KNN', 'Gaussian Naive Bayes', 'Random Forest', 'Decision Tree']
	scores = [result1, knn_score, gb_score, resultTrees, dtree_score]

	scores = [s * 100 for s in scores]

	plt.figure(figsize=(10,6))
	plt.bar(models, scores)

	plt.xlabel('Model')
	plt.ylabel('Score')
	plt.title('Model Score Comparison')
	plt.ylim(0, 100)
	plt.yticks(range(0, 101, 10))

	plt.show()




	# Logistic Regression
	y_pred_lr = model.predict(testing_set)
	confusion_matrix_lr = confusion_matrix(testing_labels, y_pred_lr)

	# KNN
	y_pred_knn = knn_full.predict(testing_set)
	confusion_matrix_knn = confusion_matrix(testing_labels, y_pred_knn)

	# Gaussian Naive Bayes
	y_pred_gnb = naive_full.predict(testing_set)
	confusion_matrix_gnb = confusion_matrix(testing_labels, y_pred_gnb)

	# Random Forest
	y_pred_rf = randomTrees.predict(testing_set)
	confusion_matrix_rf = confusion_matrix(testing_labels, y_pred_rf)

	# Decision Tree
	y_pred_dtree = dtree.predict(testing_set)
	confusion_matrix_dtree = confusion_matrix(testing_labels, y_pred_dtree)



	fig, ax = plt.subplots()
	# fig.savefig() if we want to use in our paper.

	ConfusionMatrixDisplay(confusion_matrix_lr).plot(ax=ax)
	ax.set_title('Logistic Regression Confusion Matrix')
	plt.show()




	fig, ax = plt.subplots()
	# fig.savefig() if we want to use in our paper.

	ConfusionMatrixDisplay(confusion_matrix_knn).plot(ax=ax)
	ax.set_title('K-Nearest Neighbor Confusion Matrix')
	plt.show()


	fig, ax = plt.subplots()
	# fig.savefig() if we want to use in our paper.

	ConfusionMatrixDisplay(confusion_matrix_gnb).plot(ax=ax)
	ax.set_title('Gaussian Naive Bayes Confusion Matrix')
	plt.show()\
	


	fig, ax = plt.subplots()
	# fig.savefig() if we want to use in our paper.

	ConfusionMatrixDisplay(confusion_matrix_rf).plot(ax=ax)
	ax.set_title('Random Forest Confusion Matrix')
	plt.show()


	fig, ax = plt.subplots()
	# fig.savefig() if we want to use in our paper.

	ConfusionMatrixDisplay(confusion_matrix_dtree).plot(ax=ax)
	ax.set_title('Decision Tree Confusion Matrix')
	plt.show()


	
	# combined_guy.set_xticks(xP)
	# combined_guy.set_xticklabels(model_list)



if __name__ == "__main__":
	main()