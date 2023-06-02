import numpy as np
import itertools
import matplotlib.pyplot as plt

def getAllPermutations(array):
    permutations = list(itertools.permutations(array))
    result = []
    for perm in permutations:
        perm_list = list(perm)
        perm_list.insert(0, 1)
        perm_list.append(1)
        result.append(perm_list)

    return result


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

gasMatrix = np.array([[25,11,32],
                      [21,9,31],
                      [19,3,26],
                      [31,18,28],
                      [53,35,16],
                      [24,17,40],
                      [5,23,47],
                      [44,34,15],
                      [21,41,37],
                      [53,32,20]])

# distanceMatrix = np.array([[0, 4, 13, 8, 40],
#                            [4, 0, 11, 11, 39],
#                            [13, 11, 0, 20, 37],
#                            [8, 11, 20, 0, 36],
#                            [40, 39, 37, 36, 0], ])
#
# gasMatrix = np.array([[25, 11, 32],
#                       [21, 9, 31],
#                       [19, 3, 26],
#                       [31, 18, 28],
#                       [53, 35, 16]])


array = [2, 3, 4, 5, 6, 7, 8, 9, 10]
resultList = getAllPermutations(array)
print(resultList)


class TestSolution():  # 建立一個class來包住array, printarray, fitness
    def __init__(self, array, printArray):
        self.array = array.copy()
        self.printArray = printArray.copy()
        self.fitness = fitnessFunction(distanceMatrix, self.array, self.printArray)  # 計算fitness


def findGasStation(current_city, next_city, gasMatrix):  # 計算gasStation在哪兒
    distance = 0  # 初始從目前城市->加油站->下個城市的總距離 =0
    print(f"current_city= {current_city}, next_city= {next_city}")
    current_city_to_min_gas = np.min(
        gasMatrix[current_city])  # 這個變數是要裝【從目前的城市-->找到最近的加油站距離】  #假設目前城市是【城市0】，那到gasMatrix找第0排(row)，找最小值
    print(f"current_city_to_min_gas= {current_city_to_min_gas}")
    min_gas_index = np.argmin(gasMatrix[current_city])  # 假設目前城市是【城市0】，那到gasMatrix找第0排(row)，若第0個element是最小值，那index = 0
    print(f"min_gas_index= {min_gas_index}")
    gas_Station_num = min_gas_index + 1  # 假設是【城市0】，我們在printarray是寫【城市1】，所以要再 +1
    print(f"gas_Station_num= {gas_Station_num}")
    gas_to_next_city = gasMatrix[next_city][min_gas_index]
    print(f"gas_to_next_city= {gas_to_next_city}")
    distance += current_city_to_min_gas
    distance += gas_to_next_city
    return distance, gas_Station_num, gas_to_next_city


def fitnessFunction(distanceMatrix, solutionArray, printArray):  # 計算fitness的method
    print(f"solutionArray= {solutionArray}")
    total_distance = 0
    fillUp_distance = 0
    waylist = [x - 1 for x in solutionArray]
    print(f"solutionArray= {waylist}")
    for i in range(len(waylist)):
        current_city = waylist[i]
        if i == len(waylist) - 1:  # 若跑到最後一個點了
            break
        next_city = waylist[i + 1]
        if fillUp_distance >= 159:  # 先判斷前一個distance是不是超過 gas distance
            gas_distance, gasStationNum, gas_to_next_city = findGasStation(current_city, next_city, gasMatrix)
            total_distance += gas_distance  # 總距離會==
            fillUp_distance = gas_to_next_city
            printArray.insert(i + 1, f"gas station_{gasStationNum}")
            continue  # 直接跳到下一個迴圈
        total_distance += distanceMatrix[current_city][next_city]  # 里程總距離，也就是fitness
        fillUp_distance += distanceMatrix[current_city][next_city]  # 加油距離，
    return total_distance



k = 0
resultPrintList = resultList.copy()
fitnessList = []
while k < len(resultPrintList):
    print(f"k= {k}")
    testArray = TestSolution(resultList[k], resultPrintList[k])
    print(f"testArray.array= {testArray.array}, testArray.printArray= {testArray.printArray}, testArray.fitness= {testArray.fitness}")
    k += 1
    fitnessList.append(testArray.fitness)

print(fitnessList)
min_value = min(fitnessList)
min_index = fitnessList.index(min_value)
print(f"min_index= {min_index}, min_value= {min_value}")
mintestArray = TestSolution(resultList[min_index], resultPrintList[min_index])
print(f"mintestArray.array= {mintestArray.array}, mintestArray.printArray= {mintestArray.printArray}, mintestArray.fitness= {mintestArray.fitness}")
#==================================================================#

# newArray = [1, 4, 5, 3, 2, 1]
# newPrintArray = newArray.copy()
# print(f"newArray= {newArray}, newPrintArray= {newPrintArray}")
# tmpArray = TestSolution(newArray, newPrintArray)
# print(
#     f"tmpArray.array= {tmpArray.array}, tmpArray.printArray= {tmpArray.printArray}, tmpArray.fitness= {tmpArray.fitness}")

################## STEP 04 繪圖 #############################

plt.title("Jing_final")
iteration_ = np.arange(0, len(fitnessList), 1)
plt.xlabel("Generation")
plt.ylabel("Fitness,f Maximum")
plt.plot(iteration_, fitnessList, label="Test Array")  # 這是每一個iteration的fitness走勢

# plt.plot(iteration_, gBestListFitness, c="black", alpha=0.3, label="gBest Array")  # 這是gBest的fitness走勢

# 這是把點位置的x軸==gBestChangeIndexList y軸==gBestChange_index_fitness 的文字描述((寫出座標位置))
# for i in range(len(gBestChangeIndexList)):
#     x = gBestChangeIndexList[i]
#     y = gBestChange_index_fitness[i]
#     plt.text(x, y + 3, f"({x}, {y})", fontsize=7, ha='center', va='bottom', alpha=0.5)

# plt.scatter(gBestChangeIndexList, gBestChange_index_fitness, alpha=0.3, c="r",
#             label="gBestChangePoint")  # 這是把gBestChange的點標示出來
# plt.legend(loc='upper right')  # 顯示圖例 #放在圖的右下角

# text = f'initialtemp={temperature.initialtemp}, tempMin={temperature.tempMin}'
# text2 = f'coolingRate= {FireReductionRadio}'
# text3 = f'iterationNum= {iterationNum}'
# plt.text(0.98, 0.75, text, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
# plt.text(0.98, 0.7, text2, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
# plt.text(0.98, 0.65, text3, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
plt.show()
