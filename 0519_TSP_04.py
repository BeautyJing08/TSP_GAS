### 要把溫度&降溫&退火演算寫出來
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

### 創建解Class
class TestSolution():
    def __init__(self, array, printArray):
        self.array = array
        self.printArray = printArray
        self.fitness = fitnessFunction(testMatrix, self.array, self.printArray)


## 創建溫度Class
class Temperature():
    def __init__(self, initialtemp, tempMin): #創建溫度的時候，要丟入原始溫度 & 終止計算的最小溫度
        self.initialtemp = initialtemp
        self.temp = initialtemp #溫度會 == 初始溫度
        self.tempMin = tempMin

## 設定降溫method
def SlowCooling(temperature, iterationNum):  # 降溫方法
    FireReductionRadio = 0.9  # 溫度下降的比例
    temperature.temp = temperature.initialtemp * (FireReductionRadio ** iterationNum)
    return temperature

## 設定 如何找到gas station method
def findGasStation(current_city, next_city, gasMatrix):
    distance = 0
    current_city_to_min_gas = np.min(gasMatrix[current_city])
    min_gas_index = np.argmin(gasMatrix[current_city])
    gas_Station_num = min_gas_index + 1
    gas_to_next_city = gasMatrix[next_city][min_gas_index]
    distance += current_city_to_min_gas
    distance += gas_to_next_city
    return distance, gas_Station_num

## 計算fitness method
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

## 找到新的解
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
    return array
## 找到隔壁的解
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
    newPrintArray = newArray.copy()
    return TestSolution(newArray,newPrintArray)

######## ## 創建 退火演算法的 method

def SimulatedAnnealing(distanceMatrix, temperature): #要把 workMatrix & 溫度丟進去
    iterationNum = 0  # 從第0代開始
    testArrayList = []
    gBestList = []  # 有更好的gBest時，就存進來
    gBestChangeIndexList = []  # 這是索引gBest更動時的位置 ((後續可以丟到陣列中拿到fitness值
    #### 初代解 ####
    initArray = getNewArray(testMatrix)
    initPrintArray = initArray.copy()
    # print(initArray)
    testArray = TestSolution(initArray, initPrintArray)
    print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")
    gBestArray = testArray  # 同時創造一個新的gBestArray來記錄

    testArrayList.append(testArray)
    gBestList.append(gBestArray)
    #### 執行後續演算 ####
    while temperature.temp > temperature.tempMin: ##在溫度沒有低到"低溫標準"，都繼續執行計算
        iterationNum += 1
        tmpTestArray = getNeighborArray(testArray.array) ##創建一個tmpTestArray ((從獲得鄰近解method創建
        ### 第一個情況，新的解比舊的解好 ###

        if tmpTestArray.fitness > testArray.fitness:
            testArray = tmpTestArray

            # if iterationNum % 3 == 0:
            temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
            print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

            ### 若tmpTest > gBest 就要把索引值存到 gBestChangeIndexList









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






# #===============================================================================
# # 創建溫度

print("M11105102")
print("Jing's SA_assignment")
initialtemp = 3000
tempMin = 0
temperature = Temperature(initialtemp, tempMin) ### 創建溫度
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}") ### 印出 溫度設定
print()
#
# ####### STEP 03 執行退火演算法 SimulatedAnnealing  #####################
#
testArrayList, gBestList, gBestChangeIndexList, iterationNum = SimulatedAnnealing(testMatrix, temperature)