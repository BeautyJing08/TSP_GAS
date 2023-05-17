### now use TS 來寫一個試著解決 TSP 問題 的 code
import random

import numpy as np

distanceMartix = np.array([[0, 60, 80, 90, 45, 20],
                           [60, 0, 30, 60, 90, 80],
                           [80, 30, 0, 15, 60, 90],
                           [45, 90, 60, 40, 0, 25],
                           [20, 80, 90, 70, 25, 0]])

gasMartix = np.array([[5, 70, 80],
                      [50, 30, 25],
                      [80, 95, 95],
                      [15, 20, 5],
                      [36, 89, 15],
                      [11, 22, 33]])

class TestSolution():
    def __init__(self,array):
        self.array = array
        self.fitness = fitnessFunction(testMatrix,self.array)
        self.printArray = array



def fitnessFunction(distanceMatrix, solutionArray):  # 計算fitness的method
    total_distance = 0
    waylist = [x - 1 for x in solutionArray]
    for i in range(len(waylist)):
        current_city = waylist[i]
        if i == len(solutionArray) - 1:  # 若跑到最後一個點了
            break
        next_city = waylist[i + 1]
        total_distance += distanceMatrix[current_city][next_city]
    return total_distance


def findGasStation(current_city, next_city):
    return 0


def getNewArray(distanceMatrix):  # 找到一個新的解
    distanceMatrixRowNum = distanceMatrix.shape[0]
    array = []
    for i in range(distanceMatrixRowNum):  # 若這個matrix是3*3 num==3, range(3)= [0,1,2]
        array.append(i)  # [0,1,2]依序插入到array內
    array = array[1:]  # 把第一個值，也就是0刪掉 #因為我們的頭尾規定都是 0，所以先把第一位數拿掉
    random.shuffle(array)  # 打亂這個array #打亂這裡面的排列
    array.insert(0, 0)  # 在第0位，插入數字 0
    array.append(0)  # 在最後一位插入數字 0
    array = [x + 1 for x in array]  # 把array中的值都加一 if array=[0,1,2] ---> 變成 [1,2,3]
    return TestSolution(array)


def getNeighborArray(array):
    newArray = array.copy()
    newArray = [x - 1 for x in newArray]  # 把這個array的值都-1
    newArray = newArray[1:]  # 刪掉第一位的0
    newArray = newArray[:-1]  # 刪掉最後一位的0
    pos1 = random.randint(0, len(newArray) - 1)  # 隨機取一位
    pos2 = random.randint(0, len(newArray) - 1)  # 隨機取一位
    if pos1 == pos2:  # 若這麼碰巧的pos1 == pos2 ((會變成新的newArray沒有更新))，所以重新執行這個method
        return getNeighborArray(array)  # 重新執行
    newArray[pos1], newArray[pos2] = newArray[pos2], newArray[pos1]  # 把這兩個位置交換
    newArray.insert(0, 0)  # 在第一位插入0
    newArray.append(0)  # 最後一位插入0
    newArray = [x + 1 for x in newArray]  # 最後把這個array的值都+1
    return TestSolution(newArray)




# ==============================================================================================

testMatrix = np.array([[0, 5, 10, 12],
                       [5, 0, 8, 15],
                       [10, 8, 0, 18],
                       [12, 15, 18, 0]])

testArray = [1, 3, 2, 4, 1]
TestArray = TestSolution([1,3,2,4,1])
print(TestArray.array)
print(TestArray.fitness)


# testMatrixFitness = fitnessFunction(testMatrix, testArray)
# print(f"testArray= {testArray} , testMatrixFitness= {testMatrixFitness}")
#
# newarray = getNewArray(testMatrix)
# # print(newarray)
#
# newarrayFitness = fitnessFunction(testMatrix, newarray)
# # print(newarrayFitness)
# print(f"newarray= {newarray} , newarrayFitness= {newarrayFitness}")
#
# AAarray = getNeighborArray(newarray)
# AAarrayFitness = fitnessFunction(testMatrix, AAarray)
#
# # print(f"AAarray= {AAarray}")
#
#
# print(f"AAarray= {AAarray} , AAarrayFitness= {AAarrayFitness}")
