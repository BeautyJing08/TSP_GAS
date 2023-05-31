### 0521 把圖畫出來，但是低溫要是0.5 整體趨勢看起來才是對的 ##
import random
import math
import numpy as np
import matplotlib.pyplot as plt

distanceMatrix = np.array([[0, 4, 13, 8, 40, 27, 30, 39, 61, 26],
                           [4, 0, 11, 11, 39, 23, 26, 40, 43, 30],
                           [13, 11, 0, 20, 37, 16, 23, 30, 39, 35],
                           [8, 11, 20, 0, 36, 31, 35, 35, 57, 22],
                           [40, 39, 37, 36, 0, 51, 63, 33, 55, 29],
                           [27, 23, 16, 31, 51, 0, 29, 28, 37, 49],
                           [30, 26, 23, 35, 63, 29, 0, 47, 23, 57],
                           [39, 40, 30, 35, 33, 28, 47, 0, 26, 37],
                           [61, 43, 39, 57, 55, 37, 23, 26, 0, 58],
                           [26, 30, 35, 22, 29, 49, 57, 37, 58, 0]])

gasMatrix = np.array([[25, 11, 32],
                      [21, 9, 31],
                      [19, 3, 26],
                      [31, 18, 28],
                      [53, 35, 16],
                      [24, 17, 40],
                      [5, 23, 47],
                      [44, 34, 15],
                      [21, 41, 37],
                      [53, 32, 20]])


### create solution Class
class TestSolution():
    def __init__(self, array, printArray):
        self.array = array.copy()
        self.printArray = printArray.copy()
        self.fitness = fitnessFunction(distanceMatrix, self.array, self.printArray)


## create temperature Class
class Temperature():
    def __init__(self, initialtemp, tempMin):  # 創建溫度的時候，要丟入原始溫度 & 終止計算的最小溫度
        self.initialtemp = initialtemp
        self.temp = initialtemp  # 溫度會 == 初始溫度
        self.tempMin = tempMin


FireReductionRadio = 0.99


## setting slow cooling method
def SlowCooling(temperature, iterationNum):  # 降溫方法
    # FireReductionRadio = 0.999 # 溫度下降的比例
    temperature.temp = temperature.initialtemp * (FireReductionRadio ** iterationNum)
    return temperature


## 設定 如何找到gas station method
def findGasStation(current_city, next_city, gasMatrix):
    distance = 0  # this distnace is to record current_city to gas station and to next_city
    current_city_to_min_gas = np.min(gasMatrix[current_city])  # find closest distance in gasMatrix [current_city] row
    min_gas_index = np.argmin(gasMatrix[current_city])  # find the index
    gas_Station_num = min_gas_index + 1
    gas_to_next_city = gasMatrix[next_city][min_gas_index]  # next_city row * closest index
    distance += current_city_to_min_gas
    distance += gas_to_next_city
    return distance, gas_Station_num, gas_to_next_city


## 計算fitness method
def fitnessFunction(distanceMatrix, solutionArray, printArray):  # 計算fitness的method
    total_distance = 0
    fillUp_distance = 0
    waylist = [x - 1 for x in solutionArray]
    for i in range(len(waylist)):
        current_city = waylist[i]
        if i == len(waylist) - 1:  # if run to last one
            break  # break the for loop
        next_city = waylist[i + 1]
        if fillUp_distance >= 159:  # if fillUP_distance greater than 159 , doing findGasStation method
            gas_distance, gasStationNum, gas_to_next_city = findGasStation(current_city, next_city, gasMatrix)
            total_distance += gas_distance
            fillUp_distance = gas_to_next_city  # fillUP_distnace will equal gas station to next_city
            printArray.insert(i + 1, f"gas station_{gasStationNum}")  # insert gas station num to printArray
            continue  # forced into next loop
        total_distance += distanceMatrix[current_city][next_city]
        fillUp_distance += distanceMatrix[current_city][next_city]
    return total_distance


## 找到新的解
def getNewArray(distanceMatrix):  # get an initial solution array method
    distanceMatrixRowNum = distanceMatrix.shape[0]  # read distanceMatrix to get row num
    array = []
    for i in range(
            distanceMatrixRowNum):  # if this matrix is 3*3, num==3, range(3)=[0,1,2] # 若這個matrix是3*3 num==3, range(3)= [0,1,2,3]
        array.append(i)  # [0,1,2,3]insert to array one by one
    array = array[1:]  # delete array[0]===> [0,1,2,3]--->[1,2,3]
    random.shuffle(array)  # shuffle array ===> [1,2,3]--->[3,2,1]
    array.insert(0, 0)  # insert 0 to array [0] ====> [3,2,1]--->[0,3,2,1]
    array.append(0)  # append 0 to array =========> [0,3,2,1]--->[0,3,2,1,0]
    array = [x + 1 for x in array]  # make array every element add one ===> if array=[0,1,2] ---> [1,2,3]
    return array


## 找到隔壁的解
def getNeighborArray(array):  # get neighbor array method
    newArray = array.copy()
    newArray = [x - 1 for x in newArray]  # make new array every element subtract one ===> if [1,2,3]--->[0,1,2]
    newArray = newArray[1:]  # delete array[0]
    newArray = newArray[:-1]  # delete array last element
    pos1 = random.randint(0, len(newArray) - 1)  # random select one element
    pos2 = random.randint(0, len(newArray) - 1)  # random select one element
    if pos1 == pos2:  # if pos1 == pos2, then newArray will not update, so redo getNeighborArray method
        return getNeighborArray(array)  # redo
    newArray[pos1], newArray[pos2] = newArray[pos2], newArray[pos1]  # change these two elements
    newArray.insert(0, 0)  # insert 0 to array [0]
    newArray.append(0)  # append 0 to array
    newArray = [x + 1 for x in newArray]  # make array every element add one ===> if array=[0,1,2] ---> [1,2,3]
    newPrintArray = newArray.copy()
    return TestSolution(newArray, newPrintArray)


######## ## 創建 退火演算法的 method

def SimulatedAnnealing(distanceMatrix, temperature):  # 要把 workMatrix & 溫度丟進去
    iterationNum = 0  # from 0 iteration
    testArrayList = []
    gBestList = []  # if have better gBest, record it
    gBestChangeIndexList = []  # it's the index for searching gBest iteration num -> can put it to array get fitness

    #### 初代解 #### #initial solution
    initArray = getNewArray(distanceMatrix)  # get initial array
    initPrintArray = initArray.copy()  # copy it to PrintArray
    # print(initArray)
    testArray = TestSolution(initArray, initPrintArray) # to create a testArray Class element
    print(f"initArray= {initArray}, initPrintArray= {initPrintArray}")
    print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")
    gBestArray = testArray

    testArrayList.append(testArray)
    gBestList.append(gBestArray)
    #### 執行後續演算 ####
    while temperature.temp > temperature.tempMin: # when temperature reach teapMin > stop loop
        print(temperature.temp)
        iterationNum += 1
        tmpTestArray = getNeighborArray(testArray.array) # create new tmpTestArray from neighbor
        ### first situation
        ### 第一個情況，新的解比舊的解好 ### ((要找到比較小的答案))
        if tmpTestArray.fitness < testArray.fitness:
            testArray = tmpTestArray  # tmp replace test
            # if iterationNum % 3 == 0:
            temperature = SlowCooling(temperature, iterationNum)  # every iteration doing slow cooling
            print(
                f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")
            ### 若tmpTest > gBest 就要把索引值存到 gBestChangeIndexList
            if tmpTestArray.fitness < gBestArray.fitness:
                gBestArray = tmpTestArray
                gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好

        ### 第二個情況，新的解沒有比舊的解好 # 就要計算 delta & movePossibility & 隨機生成 r
        elif tmpTestArray.fitness > testArray.fitness:  # (找最小值，所以比較大的就是比較不好的)
            r = np.random.rand()  # 隨機創造0~1之間的數
            delta = tmpTestArray.fitness - testArray.fitness  # 參照公式
            # print(f"r= {r}, delta= {delta}")
            movePossibility = math.exp(-delta / temperature.temp)  # 參照公式
            # print(f"r= {r}, delta= {delta}, movePossibility= {movePossibility}")
            ## 若 r < movePossibility
            if r < movePossibility:  # 若隨機變數r < 移動機率 movePossibility
                testArray = tmpTestArray  # 就move粒子，讓新的取代舊的
                # if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
                print(
                    f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

                ### 若tmpTest > gBest 就要把索引值存到 gBestChangeIndexList
                if tmpTestArray.fitness < gBestArray.fitness:
                    gBestArray = tmpTestArray
                    gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好
            ## 若 r > movePossibility: #就降溫而已
            else:
                # if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
                print(
                    f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

        else:  # 不移動粒子，就只做改變溫度
            # if iterationNum % 3 == 0:
            temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
            print(
                f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

        testArrayList.append(testArray)
        gBestList.append(gBestArray)

    print()
    return testArrayList, gBestList, gBestChangeIndexList, iterationNum

# #===============================================================================
# # 創建溫度

print("M11105102 王菁 | M11101013 何欣穎")
print("Group07 _ TSP_GAS")
initialtemp = 100000
tempMin = 0.01
temperature = Temperature(initialtemp, tempMin)  ### 創建溫度
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}")  ### 印出 溫度設定
print()
#
# ####### STEP 03 執行退火演算法 SimulatedAnnealing  #####################
#
testArrayList, gBestList, gBestChangeIndexList, iterationNum = SimulatedAnnealing(distanceMatrix, temperature)

########################################################################

######## 創建 testArrayListFitness #把每一代的fitness裝進去
testArrayListFitness = []
for i in testArrayList:
    testArrayListFitness.append(i.fitness)
# print(testArrayListFitness)
# print(len(testArrayListFitness))
# print(iterationNum + 1)

######## 把 gBestChangeIndexList 丟到 testArrayListFitness找到轉折點
######## 這是要拿來畫得到更好的gBest圖點圖

gBestChange_index_fitness = []
# print(gBestChangeIndexList)
for i in gBestChangeIndexList:
    gBestChange_index_fitness.append(testArrayListFitness[i])

# print(gBestChange_index_fitness)

gBestListFitness = []
for i in gBestList:
    gBestListFitness.append(i.fitness)
# print(gBestListFitness)
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}")  ### 印出 溫度設定Z
print(f"總共執行了 {iterationNum} 代")
print(
    f"final_出現在第 {gBestChangeIndexList[-1]} 代, final_gBest = {gBestList[-1].printArray}, final_gBest_fitness= {gBestListFitness[-1]}")

### 把答案轉型成中文 ###
mapping = {1: "台科", 2: "中正紀念堂", 3: "故宮博物院", 4: "木柵動物園", 5: "九份老街", 6: "陽明山擎天崗",
           7: "淡水漁人碼頭", 8: "野柳女王頭", 9: "富貴角燈塔", 10: "平溪天燈", "gas station_1": "G台灣中油淡水站",
           "gas station_2": "G台灣中油大直站", "gas station_3": "G台灣中油成功一路(基隆)"}
newarray = [mapping[element] for element in gBestList[-1].printArray]
print(newarray)


################## STEP 04 繪圖 #############################

plt.title("Jing_final")
iteration_ = np.arange(0, len(testArrayListFitness), 1)
plt.xlabel("Generation")
plt.ylabel("Fitness,f Maximum")
plt.plot(iteration_, testArrayListFitness, label="Test Array")  # 這是每一個iteration的fitness走勢

plt.plot(iteration_, gBestListFitness, c="black", alpha=0.3, label="gBest Array")  # 這是gBest的fitness走勢

# 這是把點位置的x軸==gBestChangeIndexList y軸==gBestChange_index_fitness 的文字描述((寫出座標位置))
for i in range(len(gBestChangeIndexList)):
    x = gBestChangeIndexList[i]
    y = gBestChange_index_fitness[i]
    plt.text(x, y + 3, f"({x}, {y})", fontsize=7, ha='center', va='bottom', alpha=0.5)

plt.scatter(gBestChangeIndexList, gBestChange_index_fitness, alpha=0.3, c="r",
            label="gBestChangePoint")  # 這是把gBestChange的點標示出來
plt.legend(loc='upper right')  # 顯示圖例 #放在圖的右下角

text = f'initialtemp={temperature.initialtemp}, tempMin={temperature.tempMin}'
text2 = f'coolingRate= {FireReductionRadio}'
text3 = f'iterationNum= {iterationNum}'
plt.text(0.98, 0.75, text, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
plt.text(0.98, 0.7, text2, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
plt.text(0.98, 0.65, text3, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
plt.show()
