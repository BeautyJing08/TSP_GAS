import numpy as np
import itertools
def getAllPermutations(array):
    permutations = list(itertools.permutations(array))
    result = []
    for perm in permutations:
        perm_list = list(perm)
        perm_list.insert(0,1)
        perm_list.append(1)
        result.append(perm_list)

    return result


array = [2,3,4,5,6]
resultArray = getAllPermutations(array)
print(resultArray)

########################################################

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
########################################################
### 創建解Class
class TestSolution():
    def __init__(self, array, printArray):
        self.array = array
        self.printArray = printArray
        self.fitness = fitnessFunction(distanceMatrix, self.array, self.printArray)


## 創建溫度Class
class Temperature():
    def __init__(self, initialtemp, tempMin):  # 創建溫度的時候，要丟入原始溫度 & 終止計算的最小溫度
        self.initialtemp = initialtemp
        self.temp = initialtemp  # 溫度會 == 初始溫度
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
    return distance, gas_Station_num , gas_to_next_city


## 計算fitness method
def fitnessFunction(distanceMatrix, solutionArray, printArray):  # 計算fitness的method
    total_distance = 0
    fillUp_distance = 0
    waylist = [x - 1 for x in solutionArray]
    for i in range(len(waylist)):
        current_city = waylist[i]
        if i == len(solutionArray) - 1:  # 若跑到最後一個點了
            break
        next_city = waylist[i + 1]
        if fillUp_distance >= 20:  # 先判斷前一個distance是不是超過 gas distance
            gas_distance, gasStationNum, gas_to_next_city = findGasStation(current_city, next_city, gasMatrix)
            total_distance += gas_distance
            fillUp_distance = 0
            printArray.insert(i + 1, f"gas station_{gasStationNum}")
            continue
        total_distance += distanceMatrix[current_city][next_city]
        fillUp_distance += distanceMatrix[current_city][next_city]
    return total_distance

########################################################
######## ## 創建 退火演算法的 method

def SimulatedAnnealing(distanceMatrix, temperature,resultArrayList):  # 要把 workMatrix & 溫度丟進去
    iterationNum = 0  # 從第0代開始
    testArrayList = []
    resultArrayListNum = len(resultArrayList)
    resultArrayPrintList = resultArrayList.copy()
    gBestList = []  # 有更好的gBest時，就存進來
    gBestChangeIndexList = []  # 這是索引gBest更動時的位置 ((後續可以丟到陣列中拿到fitness值

    #### 初代解 ####
    initArray = TestSolution(resultArrayList[iterationNum],resultArrayPrintList[iterationNum])
    initPrintArray = initArray.copy()
    # print(initArray)
    testArray = TestSolution(resultArrayList[iterationNum],resultArrayPrintList[iterationNum])
    print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")
    gBestArray = testArray  # 同時創造一個新的gBestArray來記錄

    testArrayList.append(testArray)
    gBestList.append(gBestArray)
    #### 執行後續演算 ####
    while iterationNum < resultArrayListNum - 1:  ##在溫度沒有低到"低溫標準"，都繼續執行計算
        iterationNum += 1
        tmpTestArray = TestSolution(resultArrayList[iterationNum],resultArrayPrintList[iterationNum]) ##創建一個tmpTestArray ((從獲得鄰近解method創建

        ### 第一個情況，新的解比舊的解好 ### ((要找到比較小的答案))
        if tmpTestArray.fitness < testArray.fitness:
            testArray = tmpTestArray  # 讓tmp取代test

            temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
            print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")
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
            if r < movePossibility: # 若隨機變數r < 移動機率 movePossibility
                testArray = tmpTestArray # 就move粒子，讓新的取代舊的
                temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
                print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

                ### 若tmpTest > gBest 就要把索引值存到 gBestChangeIndexList
                if tmpTestArray.fitness < gBestArray.fitness:
                    gBestArray = tmpTestArray
                    gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好
            ## 若 r > movePossibility: #就降溫而已
            else:
                temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
                print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

        else: #不移動粒子，就只做改變溫度
            temperature = SlowCooling(temperature, iterationNum)  # 每個iteration就降溫一次
            print(f"第{iterationNum}代，array= {testArray.array},PrintArray= {testArray.printArray}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

        testArrayList.append(testArray)
        gBestList.append(gBestArray)

    print()
    return testArrayList, gBestList, gBestChangeIndexList, iterationNum


# #===============================================================================
# # 創建溫度

print("M11105102")
print("Jing's SA_assignment")
initialtemp = 300
tempMin = 0.5
temperature = Temperature(initialtemp, tempMin)  ### 創建溫度
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}")  ### 印出 溫度設定
print()
#
# ####### STEP 03 執行退火演算法 SimulatedAnnealing  #####################
#
testArrayList, gBestList, gBestChangeIndexList, iterationNum = SimulatedAnnealing(distanceMatrix, temperature, resultArray)

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
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}") ### 印出 溫度設定Z
print(f"總共執行了 {iterationNum} 代")
print(f"final_出現在第 {gBestChangeIndexList[-1]} 代, final_gBest = {gBestList[-1].printArray}, final_gBest_fitness= {gBestListFitness[-1]}")

# end = time.process_time()

# print(f"找到所有解的執行時間: ", (end - start))
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

plt.scatter(gBestChangeIndexList, gBestChange_index_fitness, alpha=0.3, c="r" , label = "gBestChangePoint") #這是把gBestChange的點標示出來
plt.legend(loc='upper right')  # 顯示圖例 #放在圖的右下角

text = f'initialtemp={temperature.initialtemp}, tempMin={temperature.tempMin}'
plt.text(0.98, 0.75, text, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
plt.show()
