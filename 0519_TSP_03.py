### 潘老師ㄉ幫忙後新code
import random

import numpy as np

distanceMatrix = np.array([[0, 60, 80, 90, 45, 20],
                           [60, 0, 30, 60, 90, 80],
                           [80, 30, 0, 15, 60, 90],
                           [90, 60, 15, 0, 40, 70],
                           [45, 90, 60, 40, 0, 25],
                           [20, 80, 90, 70, 25, 0]])

gasMatrix = np.array([[5, 70, 80],
                      [50, 30, 25],
                      [80, 95, 95],
                      [15, 20, 5],
                      [36, 89, 15],
                      [11, 22, 33]])


class TestSolution():
    def __init__(self, array, printArray):
        self.array = array
        self.printArray = printArray
        self.fitness = fitnessFunction(testMatrix, self.array, self.printArray)


def findGasStation(current_city, next_city, gasMatrix):
    distance = 0
    current_city_to_min_gas = np.min(gasMatrix[current_city])
    min_gas_index = np.argmin(gasMatrix[current_city])
    gas_Station_num = min_gas_index + 1
    gas_to_next_city = gasMatrix[next_city][min_gas_index]
    distance += current_city_to_min_gas
    distance += gas_to_next_city
    return distance, gas_Station_num


def fitnessFunction(distanceMatrix, solutionArray, printArray):  # 計算fitness的method
    total_distance = 0
    waylist = [x - 1 for x in solutionArray]
    for i in range(len(waylist)):
        current_city = waylist[i]
        if i == len(solutionArray) - 1:  # 若跑到最後一個點了
            break
        next_city = waylist[i + 1]
        if total_distance >= 20:  # 先判斷前一個distance是不是超過 gas distance
            gas_distance, gasStationNum = findGasStation(current_city, next_city, gasMatrix)
            total_distance += gas_distance
            total_distance == 0
            printArray.insert(i + 1, f"gas station_{gasStationNum}")
            break
        total_distance += distanceMatrix[current_city][next_city]
    return total_distance


def getNewArray(distanceMatrix):  # 找到一個新的解
    distanceMatrixRowNum = distanceMatrix.shape[0]
    #     line70~line74 : 下次遇到同樣使用情境時 可以嘗試下面兩種寫法
    #     array = [i for i in range(distanceMatrixRowNum)][1:] # 1
    #     array = list(range(distanceMatrixRowNum))[1:] # 2
    array = []
    for i in range(distanceMatrixRowNum):  # 若這個matrix是3*3 num==3, range(3)= [0,1,2]
        array.append(i)  # [0,1,2]依序插入到array內
    array = array[1:]  # 把第一個值，也就是0刪掉 #因為我們的頭尾規定都是 0，所以先把第一位數拿掉
    random.shuffle(array)  # 打亂這個array #打亂這裡面的排列
    array.insert(0, 0)  # 在第0位，插入數字 0
    array.append(0)  # 在最後一位插入數字 0
    array = [x + 1 for x in array]  # 把array中的值都加一 if array=[0,1,2] ---> 變成 [1,2,3]
    # printArray = array.copy()
    # printArray = [x + 1 for x in printArray]
    # return TestSolution( ,array, printArray)
    return array

def getNeighborArray(array):
    newArray = array.copy()
    newArray = [x - 1 for x in newArray]  # 把這個array的值都-1
    newArray = newArray[1:]  # 刪掉第一位的0
    newArray = newArray[:-1]  # 刪掉最後一位的0
    pos1 = random.randint(0, len(newArray) - 1)  # 隨機取一位
    pos2 = random.randint(0, len(newArray) - 1)  # 隨機取一位
    if pos1 == pos2:  # 若這麼碰巧的pos1 == pos2 ((會變成新的newArray沒有更新))，所以重新執行這個method
        return getNeighborArray(array)  # 重新執行

    #     這邊不一定要用遞迴的方式,有時候遞迴如果每次都碰巧的pos1 == pos2 那效能就會變差了QQ
    #     試試下面的寫法
    #     打亂newArray的index陣列, 取前兩個, 可以做到只做一次並且不重複
    #     random.shuffle(list(range(len(newArray))))
    #     pos1 = newArray[0]
    #     pos2 = newArray[1]

    newArray[pos1], newArray[pos2] = newArray[pos2], newArray[pos1]  # 把這兩個位置交換
    newArray.insert(0, 0)  # 在第一位插入0
    newArray.append(0)  # 最後一位插入0
    newArray = [x + 1 for x in newArray]  # 最後把這個array的值都+1
    newPrintArray = newArray.copy()
    return TestSolution(newArray,newPrintArray)


testMatrix = np.array([[0, 5, 10, 12],
                       [5, 0, 8, 15],
                       [10, 8, 0, 18],
                       [12, 15, 18, 0]])

# ==============================================================================================

testMatrix = np.array([[0, 5, 10, 12],
                       [5, 0, 8, 15],
                       [10, 8, 0, 18],
                       [12, 15, 18, 0]])

testArray = [1, 3, 2, 4, 1]
TestArray = TestSolution([1, 3, 2, 4, 1], [1, 3, 2, 4, 1])


initArray = getNewArray(testMatrix)
# print(initArray)
InitTestArray = TestSolution(initArray, initArray)
print(f"initArray= {initArray}")
print(f"initArray.printArray= {InitTestArray.printArray}, initArray.fitness= {InitTestArray.fitness}")
print()
print()
print(f"testArray={testArray}")
print(f"TestArray.printArray= {TestArray.printArray}, TestArray.fitness= {TestArray.fitness}")


ABCArray = getNewArray(testMatrix)
ABCArrayPrint = ABCArray.copy()
print(ABCArray)
ObjABCArray = TestSolution(ABCArray,ABCArrayPrint)
print(ABCArray)
print(f"ObjABCArray.array= {ObjABCArray.array}\t, ObjABCArray.printArray= {ObjABCArray.printArray}\t, ObjABCArray.fitness= {ObjABCArray.fitness}")

BCDArray = getNeighborArray(ObjABCArray.array)
print(f"BCDArray.array= {BCDArray.array}\t, BCDArray.printArray= {BCDArray.printArray}\t, BCDArray.fitness= {BCDArray.fitness}")