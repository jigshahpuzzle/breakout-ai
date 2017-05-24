import os
import numpy as np
import pandas as pd
import csv
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn import tree

'''
Run in main method
'''
def executable():
    td = TrainingData()
    td.generate_data()
    df = pd.read_csv("data/training.csv")
    y = df["target"]
    X = df.drop(["target"], axis=1)
    cf = Classifiers(X, y)

'''
Class that holds the AIPlayer and communicates
moves to the game
'''
class AIPlayer(object):

    def __init__(self):
        self.random_forest = RandomForestClassifier(n_estimators=20,
								max_depth=None, min_samples_split=2, random_state=0)
        df = pd.read_csv("data/training.csv")
        y = np.array(df["target"])
        X = np.array(df.drop(["target"], axis=1))
        self.random_forest.fit(X, y)

    def generate_move(self, ball, paddle):
        input_matrix = [[paddle.xpos, ball.xpos, ball.ypos]]
        input_matrix = np.array(input_matrix)
        return self.random_forest.predict(input_matrix)

'''
Class responsible for generating the training data
according to the decision function
'''
class TrainingData(object):

    def __init__(self):
        pass

    def generate_data(self):
        data = [["paddle_x",
					"ball_x",
					"ball_y",
					"br_1", "br_2",
					"br_3", "br_4",
					"br_5",
					"target"]]
        for x in range(1000):
            paddle_x = np.random.randint(0, 400)
            ball_x = np.random.randint(0, 400)
            ball_y = np.random.randint(30, 400)
            br_1 = np.random.randint(0, 5)
            br_2 = np.random.randint(0, 5)
            br_3 = np.random.randint(0, 5)
            br_4 = np.random.randint(0, 5)
            br_5 = np.random.randint(0, 5)
            target = 0
            if paddle_x > ball_x:
                target = 1
            elif paddle_x < ball_x:
                target = 2
            data.append([paddle_x,
							ball_x,
							ball_y,
							br_1, br_2,
							br_3, br_4,
							br_5,
							target])
        with open('data/training.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile)
            for row in data:
                spamwriter.writerow(row)

'''
Wrapper to hold the dataset and run classifiers comparing feature selection and
non-selection based classification methods.
'''
class Classifiers(object):

	def __init__(self, X, y):
		print "***** Creating Classifier Object *****"
		self.X_selected = np.array(X)
		self.y = np.array(y)
		self.naiveBayes()
		self.sGradientDescent()
		self.decisionTree()
		self.neuralNetwork()
		self.randomForestClassifier(20)

	def naiveBayes(self):
		print "***** Testing Naive Bayes *****"
		gnb = GaussianNB()
		scores = cross_val_score(gnb, self.X_selected, self.y, cv=5)
		print scores, scores.mean()

	def sGradientDescent(self):
		print "***** Testing Gradient Descent *****"
		clf = SGDClassifier(loss="hinge", penalty="l2")
		scores = cross_val_score(clf, self.X_selected, self.y, cv=5)
		print scores, scores.mean()

	def decisionTree(self):
		print "***** Testing Decision Tree *****"
		clf = tree.DecisionTreeClassifier()
		scores = cross_val_score(clf, self.X_selected, self.y, cv=5)
		print scores, scores.mean()

	def neuralNetwork(self):
		print "***** Testing Neural Net *****"
		clf =  MLPClassifier(solver='lbfgs',
					alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
		scores = cross_val_score(clf, self.X_selected, self.y, cv=5)
		print scores, scores.mean()

	def randomForestClassifier(self, est):
		print "***** Testing Random Forest Classifier *****"
		clf = RandomForestClassifier(n_estimators=est,
				max_depth=None, min_samples_split=2, random_state=0)
		scores = cross_val_score(clf, self.X_selected, self.y, cv=5)
		print scores, scores.mean()

if __name__ == "__main__":
    executable()
