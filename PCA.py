import numpy as np
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import shape
from numpy.linalg import norm
from sklearn.linear_model import LinearRegression 


class model_:
    def __init__(self,dots:np.array) -> None:
        self.m = np.random.random()
        self.b = np.random.random()
        self.dots = dots 
        self.step = 0.001
    def calc_loss(self):
        s = 0
        for i in self.dots:
            #d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
            # x1,x2 = i[0]-2,i[0]+2
            # y1,y2 = self.m*x1+self.b,self.m*x2+self.b
            # p3 = i
            # p2 = np.array([x2,y2])
            # p1 = np.array([x1,y1])
            # s += norm(np.cross(p2-p1, p1-p3))/norm(p2-p1) # abs(i[1] -1*self.m*i[0] -self.b) / np.math.sqrt(i[1]**2 + self.m**2)
            s += (i[1]-(self.m*i[0]+self.b))**2
        return s 

    def estimate_b(self):
        lower = True
        start_est = self.calc_loss()
        x = np.linspace(0,1,100)
        for i in range(10**4):
            old_b = self.b
            self.b = self.b - self.step if lower else self.b + self.step
            res = self.calc_loss()
            if res > start_est:
                lower = not lower
                self.b = old_b
            else:
                start_est = res
            # if i%10**4 == 0:
            #     plt.clf()
            #     plt.scatter(self.dots[:,0],self.dots[:,1])
            #     y = self.m*x + self.b
            #     plt.plot(x,y)
            #     plt.title(f"f(x) = {self.m}x + {self.b}")
            #     plt.show()
            
    def estimate_m(self):
        lower = True
        start_est = self.calc_loss()
        #x = np.linspace(0,1,100)
        for i in range(10**4):
            old_m = self.m
            self.m = self.m - self.step if lower else self.m + self.step
            res = self.calc_loss()
            if res > start_est:
                lower = not lower
                self.m = old_m
            else:
                start_est = res
            # if i%10**4 == 0:
            #     plt.clf()
        
    def show(self):
            plt.figure(2)
            x = np.linspace(0,1,100)
            plt.scatter(self.dots[:,0],self.dots[:,1])
            y = self.m*x + self.b
            plt.plot(x,y)
            plt.title(f"f(x) = {self.m}x + {self.b}")
            plt.show()

def main():
    dots = np.random.rand(10,2)
    model = LinearRegression()
    
    model.fit(dots[:,0].reshape(-1,1),dots[:,1])
    model.score(dots[:,0].reshape(-1,1),dots[:,1])
    y = model.predict(dots[:,0].reshape(-1,1))
    plt.figure(1)
    #plt.plot()
    plt.plot(dots[:,0],y)
    plt.show()
    m = model_(dots)
    m.estimate_b()
    m.estimate_m()
    m.show()
if __name__ == "__main__":
    main()











