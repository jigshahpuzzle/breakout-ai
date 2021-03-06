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

    # Get Decision Function on Initialization
    # Train Machine Learning Model on Initialization
    def __init__(self):
        self.td = TrainingData()
        self.random_forest = RandomForestClassifier(n_estimators=20,
								max_depth=None, min_samples_split=2, random_state=0)
        df = pd.read_csv("data/training.csv")
        y = np.array(df["target"])
        X = np.array(df.drop(["target"], axis=1))
        self.random_forest.fit(X, y)

    # Get AI Prediction for Next Move
    def generate_move(self, ball, paddle, bricks, game_mode):
        brick_bucket = [[], [], [], [], []]
        for brick in bricks:
            brick_bucket[brick.xpos // 80].append(brick)
        b1_len = len(brick_bucket[0])
        b2_len = len(brick_bucket[1])
        b3_len = len(brick_bucket[2])
        b4_len = len(brick_bucket[3])
        b5_len = len(brick_bucket[4])
        if game_mode == 0:
            return self.td.decision_function(paddle.xpos,
                            ball.xpos, ball.ypos,
                            ball.v_x, ball.v_y,
                            b1_len, b2_len, b3_len,
                            b4_len, b5_len)
        if game_mode == 1:
            input_matrix = [[paddle.xpos,
                                ball.xpos, ball.ypos,
                                ball.v_x, ball.v_y,
                                b1_len, b2_len, b3_len,
                                b4_len, b5_len]]
            input_matrix = np.array(input_matrix)
            return self.random_forest.predict(input_matrix)

'''
Class responsible for generating the training data
according to the decision function
'''
class TrainingData(object):

    def __init__(self):
        pass

    # Generate Training Data for ML Model
    def generate_data(self):
        data = [["paddle_x",
					"ball_x", "ball_y",
                    "ball_vx", "ball_vy",
					"br_1", "br_2","br_3",
                    "br_4", "br_5",
					"target"]]
        for x in range(10000):
            # Generate Randomized Inputs
            paddle_x = np.random.randint(0, 400)
            ball_x = np.random.randint(0, 400)
            ball_y = np.random.randint(30, 400)
            ball_vx = 1 - np.random.rand(1)[0] * 2
            ball_vy = 1 - np.random.rand(1)[0] * 2
            br_1 = np.random.randint(0, 10)
            br_2 = np.random.randint(0, 10)
            br_3 = np.random.randint(0, 10)
            br_4 = np.random.randint(0, 10)
            br_5 = np.random.randint(0, 10)
            target = self.decision_function(paddle_x,
                                            ball_x, ball_y,
                                            ball_vx, ball_vy,
                                            br_1, br_2, br_3,
                                            br_4, br_5)
            # Update dataset
            data.append([paddle_x,
							ball_x, ball_y,
                            ball_vx, ball_vy,
						    br_1, br_2, br_3,
                            br_4, br_5,
							target])
        # Write Training Data to File
        with open('data/training.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile)
            for row in data:
                spamwriter.writerow(row)

    # Theoretical Decision Model
    def decision_function(self, paddle_x, ball_x, ball_y,
                          ball_vx, ball_vy, br_1, br_2, br_3,
                          br_4, br_5):
        # Find Ball Goal
        ball_goal = 0 # Destination for the ball
        if ball_vy < 0:
            ball_goal = ball_x
        else:
            time = (ball_y - 370) / ball_vy
            ball_goal = ball_x + time * ball_vx * -1
            if ball_goal <= 0 or ball_goal >= 400:
                ball_goal = ball_x
        # Find Paddle Goal
        paddle_goal = 0 # Destination for the paddle
        brs = [br_1, br_2, br_3, br_4, br_5]
        max_value = max(brs)
        max_index = brs.index(max_value)
        x_targets = [40, 120, 200, 280, 360]
        x_target = x_targets[max_index]
        diff = x_target - ball_goal
        offset = diff / 400
        paddle_goal = ball_goal - 25 - offset*21
        # Set Prediction Target
        target = 0
        if paddle_x > paddle_goal:
            target = 1
        elif paddle_x < paddle_goal:
            target = 2
        return target

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
					alpha=1e-5, hidden_layer_sizes=(10, 4, 2), random_state=1)
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
