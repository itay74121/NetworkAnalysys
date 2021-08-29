import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import zeros_like
import math 
import pandas as pd
from sklearn.linear_model import LogisticRegression as LG



class LogisticRegression:
    def __init__(self,x:np.array,y:np.array,learning = 0.01) -> None:
        #initial data
        self.x = x
        self.y = y
        self.n = x.shape[0]
        self.m = x.shape[1]
        self.learning = learning

        # what im learning
        self.weight = np.random.random_sample(size=x.shape[1])
        self.b = np.random.randint(0,10)

    def h(self,xi:np.array) -> float:
        return 1 / (1+ math.e ** (-np.dot(self.weight,xi)+self.b))
    def update_weight(self):
        #print(self.weight)
        res = np.zeros(self.x.shape[1])
        for i in range(len(self.x)):
            v = self.x[i]*(self.h(self.x[i]) - self.y[i][0])
            res = v+res
        #print(res)
        res = self.learning*(1/self.m) * res
        self.weight = self.weight - res
        #print(self.weight)
       
    def update_b(self):
        #print(self.weight)
        res =0
        for i in range(len(self.x)):
            v = self.h(self.x[i]) - self.y[i][0]
            res = v+res
        #print(res)
        res = self.learning*(1/self.m) * res
        self.b = self.b - res

    def fit(self):
        for i in range(5):
            #self.update_weight()
            self.update_b()
        for i in range(5):
            self.update_weight()
    def predict(self,x:np.array)->bool:
        return self.h(x) > 0.5
    def score(self):
        c = 0
        for i in range(len(self.x)):
            p = self.predict(self.x[i])
            if p == self.y[i]:
                c+=1
        return c/self.n
    
# class GradientDescent:
#     """
#     predict is a function that takes x1 and x2. 
#     and multiply them.
#     """
#     def __init__(self,x:np.array,y:np.array,predict:function) -> None:
#         self.weights = np.random.random(size=x.shape[1])
#         self.intercept = np.random.randint(0,10)
#         self.x = x
#         self.y = y
#         self.prediction_func = predict
#     def predict(self,x)

def main():
    df = pd.read_csv("titanic.csv")
    df['male'] = df['Sex'] == 'male' 
    x = df[['Pclass','male','Age','Siblings/Spouses','Parents/Children','Fare']].values
    y = df[['Survived']].values
    for i in x:
        i[1] = 1 if i[1] == True else 0
    model = LG()
    Y = [i[0] for i in y]
    model.fit(x,Y)
    for i in model.predict(x):
        print(i)
    # lg = LogisticRegression(x,y)
    # lg.fit()
    # print(lg.weight,lg.b)
    # print("my score:" , lg.score())
    # print("model score:",model.score(x,y))
if __name__ == "__main__":
    main()