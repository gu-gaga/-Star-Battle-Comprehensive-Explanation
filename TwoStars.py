from collections import deque
from math import inf
import copy
import image_input

matrix=image_input.get_matrix("a.jpg")
copy_matrix=copy.deepcopy(matrix)
n=len(matrix)
num=[0]*n       # 统计每个区域未被处理的块数
begin=[[] for _ in range(n)]
rowNum=[0]*n
colNum=[0]*n
areaNum=[0]*n

# 标记为星
def star(row,col):
    area_order=matrix[row][col]
    matrix[row][col]=-1
    num[area_order]-=1
    areaNum[area_order]+=1
    if not isAreaFull(area_order):
        return False
    rowNum[row]+=1
    if not isRowFull(row):
        return False
    colNum[col]+=1
    if not isColFull(col):
        return False
    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
        nr,nc=row+dr,col+dc
        if 0<=nr<n and 0<=nc<n and matrix[nr][nc] not in (-1,-2):
            neighbor=matrix[nr][nc]
            num[neighbor]-=1
            matrix[nr][nc]=-2
            if num[neighbor]<2-areaNum[neighbor]:
                return False
    return True

# 检查行是否满
def isRowFull(row):
    if rowNum[row]==2:
        for i in range(n):
            if matrix[row][i] not in (-1,-2):
                neighbor=matrix[row][i]
                num[neighbor]-=1
                matrix[row][i]=-2
                if num[neighbor] < 2 - areaNum[neighbor]:
                    return False
        return True
    else:
        rest=0
        for i in range(n):
            if matrix[row][i] not in (-1,-2):
                rest += 1
                if rowNum[row]==rest:
                    return True
        return False

# 检查列是否满
def isColFull(col):
    if colNum[col]==2:
        for i in range(n):
            if matrix[i][col] not in (-1,-2):
                neighbor=matrix[i][col]
                num[neighbor]-=1
                matrix[i][col]=-2
                if num[neighbor] < 2 - areaNum[neighbor]:
                    return False
        return True
    else:
        rest=0
        for i in range(n):
            if matrix[i][col] not in (-1,-2):
                rest+=1
                if colNum[col]==rest:
                    return True
        return False

# 检查区域是否满
def isAreaFull(name):
    if areaNum[name]==2:
        for row in range(n):
            for col in range(n):
                if copy_matrix[row][col]==name and matrix[row][col]==name:
                    neighbor=matrix[row][col]
                    num[neighbor]-=1
                    matrix[row][col]=-2
                    if num[neighbor] < 2 - areaNum[neighbor]:
                        return False
        return True
    else:
        rest=0
        for row in range(n):
            for col in range(n):
                if copy_matrix[row][col] == name and matrix[row][col] == name:
                    rest+=1
                    if areaNum[name]==rest:
                        return True
        return False

# 主函数
for i in range(n):
    for j in range(n):
        order=matrix[i][j]
        num[order]+=1
        if num[order]==1:
            begin[order].append(i)
            begin[order].append(j)

# 固定格式处理
three=deque()
for i in range(n):
    if num[i]==3:
        three.append((begin[i][0],begin[i][1],i))
while three:
    r,c,a=three.popleft()
    if matrix[r+1][c] and matrix[r+1][c]==a:
        star(r+2,c)
    else:
        star(r,c+2)
    star(r,c)

# 遍历逻辑：回溯
def backtrace():
    global matrix,num,rowNum,colNum,areaNum
    if all(area==2 for area in areaNum):
        return True
    possible_list=[]
    possible_name=-1
    min_cells=inf
    for ind in range(n):
        if areaNum[ind]<2:
            if num[ind]>0:
                if num[ind]<min_cells:
                    min_cell=num[ind]
                    possible_name=ind

    for row in range(n):
        for col in range(n):
            if copy_matrix[row][col] == possible_name and matrix[row][col] == possible_name:
                possible_list.append([row,col])
    for place in possible_list:
        row,col=place[0],place[1]
        old_matrix=copy.deepcopy(matrix)
        old_num=num.copy()
        old_rowNum=rowNum.copy()
        old_colNum=colNum.copy()
        old_areaNum=areaNum.copy()
        if star(row,col):
            if backtrace():
                return True
        matrix=old_matrix
        num=old_num
        rowNum=old_rowNum
        colNum=old_colNum
        areaNum=old_areaNum
    return False

def print_solution(result_matrix):
    for row in result_matrix:
        line = ""
        for cell in row:
            if cell == -1:
                line += "★ "  # 星星
            else:
                line += "· "  # 空位
        print(line)

if backtrace():
    print("解题成功！")
    print_solution(matrix)
else:
    print("此题无解，请检查图像识别是否准确。")