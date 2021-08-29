from typing import Type
import numpy as np
import pandas as pd


class DescionTree_:
    def __init__(self,x:np.array,y:np.array) -> None:
        self.x = x
        self.y = y
        if self.x.shape[1] == 1:
            if type(self.x[0]) in (int,float):
                matrix = np.array([[self.x[i],self.y[i]] for i in range(len(x))])
                np.sort(matrix,axis=0)
                
            
            else:
                pass
        else:
            pass
        self.trees = []
        for i in range(self.x.shape[1]):
            newdata = np.delete(self.x,i,axis=1)
            tree = DescionTree_(newdata,y)
    


        

class Node:
    def __init__(self,data:np.array,values:np.array,col:int) -> None:
        self.data = data
        self.values = values
        self.col = col
        self.column = self.data[:,col]
        self.weight = np.random.choice(self.column)
        self.true = []
        self.false = []







def main():
    df =pd.read_csv("titanic.csv")
    x = df[['Pclass','Sex','Age','Siblings/Spouses','Parents/Children','Fare']].values
    y = df[['Survived']].values


if __name__ == "__main__":
    main()