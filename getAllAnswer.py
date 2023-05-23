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



array = [2,3,4,5,6]
resultList = getAllPermutations(array)
print(resultList)

class TestSolution():
    def __init__(self, array, printArray):
        self.array = array.copy()
        self.printArray = printArray.copy()

        self.fitness = fitnessFunction(distanceMatrix, self.array, self.printArray)


def findGasStation(current_city, next_city, gasMatrix):
    distance = 0
    current_city_to_min_gas = np.min(gasMatrix[current_city])
    min_gas_index = np.argmin(gasMatrix[current_city])
    gas_Station_num = min_gas_index + 1
    gas_to_next_city = gasMatrix[next_city][min_gas_index]
    distance += current_city_to_min_gas
    distance += gas_to_next_city
    return distance, gas_Station_num , gas_to_next_city



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
        if fillUp_distance >= 20:  # 先判斷前一個distance是不是超過 gas distance
            gas_distance, gasStationNum, gas_to_next_city = findGasStation(current_city, next_city, gasMatrix)
            total_distance += gas_distance
            fillUp_distance = 0
            printArray.insert(i + 1, f"gas station_{gasStationNum}")
            continue
        total_distance += distanceMatrix[current_city][next_city]
        fillUp_distance += distanceMatrix[current_city][next_city]
    return total_distance



k = 0
resultPrintList = resultList.copy()
fitnessList = []
while k < len(resultPrintList):
    print(f"k= {k}")
    testArray = TestSolution(resultList[k],resultPrintList[k])
    print(f"testArray.array= {testArray.array}, testArray.printArray= {testArray.printArray}, testArray.fitness= {testArray.fitness}")
    k += 1
    fitnessList.append(testArray.fitness)
print(fitnessList)
min_value = min(fitnessList)
min_index = fitnessList.index(min_value)
print(f"min_index= {min_index}, min_value= {min_value}")
mintestArray = TestSolution(resultList[min_index],resultPrintList[min_index])
print(f"mintestArray.array= {mintestArray.array}, mintestArray.printArray= {mintestArray.printArray}, mintestArray.fitness= {mintestArray.fitness}")

# a = [1,2,3,4,5]
# print(f"a= {a}")
# b = a.copy()
# print(f"b= {b}")
# # a[0]=0
# # print(f"a= {a}, b= {b}")
# print("=======================================================")
# print(resultList[k])
#
# testArray = TestSolution(resultList[k],resultPrintList[k])
# print( f"testArray.array= {testArray.array}, testArray.printArray= {testArray.printArray}, testArray.fitness= {testArray.fitness}")