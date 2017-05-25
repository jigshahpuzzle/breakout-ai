# breakout-ai

## Dependencies 
Install dependencies via 'pip install -r requirements.txt'. Installing dependencies in a virtual environment is recommended.   

## Running the Code 
'python main.py 0' - Runs Breakout with a decision function based AI created using domain knolwedge of the game.   
'python main.py 1' - Runs Breakout with a machine learning based AI trained from a dataset generated by observing the prior AI.  
'python main.py 2' - Runs Breakout for single player human play.   
'python ai.py' - Runs cross validation tests on the training dataset provided across a variety of machine learning models.   

## Files 
main.py - contains an executable to startup the game, and classes for all of the key objects that are present in the game    
ai.py - contains the code to train and run both the domain-knowledge and machine learning AI agents     
