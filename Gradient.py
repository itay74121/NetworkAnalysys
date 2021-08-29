import numpy as np
from numpy.core.fromnumeric import size
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


# from matplotlib import pyplot as plt
# from numpy.linalg.linalg import 

class GD:
    def __init__(self,X:np.array,Y:np.array,lr = 0.001,slr= 0.001) -> None:
        self.X = X
        self.Y = Y
        self.lr = lr
        self.slr =  slr
        self.weights = np.random.random(size = X.shape[1])
        self.b = np.random.random()
    def j1(self):
        s = 0
        for i in range(len(self.X)):
            s += (np.dot(self.weights,self.X[i]) +self.b - self.Y[i][0])*self.X[i]
        s = s*(1/float(self.X.shape[1]))
        return s
    def j2(self):
        s = 0
        for i in range(len(self.X)):
            s += (np.dot(self.weights,self.X[i]) + self.b- self.Y[i][0])
        s = s*(1/float(self.X.shape[1]))
        return s

    def fit(self):
        a = np.array([1]*self.X.shape[1])
        b = 1
        for i in range(1000):
            a,b = self.j1(),self.j2()
            if i %1000 == 0:
                print(a,b)
            self.weights = self.weights - self.lr * a
            self.b = self.b - self.lr*b
        print(self.weights,self.b)

    def predict(self,xi:np.array):
        return np.dot(self.weights,xi)+self.b

    def score(self):
        c = 0
        for i in range(len(self.X)):
            # if (self.predict(self.X[i]) > 0.5 and self.Y[i] == 1) or (self.predict(self.X[i]) < 0.5 and self.Y[i] == 0):
            #     c+=1
            print(self.predict(self.X[i]), self.Y[i])
        #print(c/self.X.shape[0])
        print(self.j1(),self.j2())



def main():
    df = pd.read_csv("titanic.csv")
    df['male'] = df['Sex'] == 'male' 
    x = df[['Pclass','male','Age','Siblings/Spouses','Parents/Children','Fare']].values
    y = df[['Survived']].values
    for i in x:
        i[1] = 1 if i[1] == True else 0

    for i in range(6):
        m = np.max(x[:,i])
        for j in range(len(x)):
            x[j][i] = x[j][i]/m
    # for i in range(len(y)):
    #     if i%5 == 0:
    #         y[i][0]= 5
    lm = RandomForestClassifier()
    lm.fit(x,[i[0] for i in y])
    print(lm.score(x,[i[0] for i in y]))
    y1 = lm.predict(x)
    # gd = GD(x,y)
    # gd.fit()
    # gd.score()
if __name__ == "__main__":
    main()

import sklearn
