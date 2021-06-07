import sys
import time
sys.stdin = open("input_origin.txt")
sys.setrecursionlimit(100000)

################## solution 1 #####################
# solution one을 위한 함수
# 전위 순회를 통해 필요한 data 얻어오기
# 재귀로 전위 순회 했는데 충돌이 일어나서 중간에 코드가 중단된다..
# 출제자의 의도
# 노드 십만개 질문 만개 기준 약 2초
def getTable(node, count):
    global num

    table[node].append(count)
    count += 1
    # print(count)

    for child in tree[node]:
        count = getTable(child, count)
    
    table[node].append(count)

    return count

# 재귀 충돌로 인해 재귀 중단돼서 while문으로 전위 순회 구현
def getTableTwo():
    stack = [[0, 0]]
    num = 0
    while stack:
        current, child_idx = stack[-1]
 
        if child_idx == 0:
            table[current].append(num)
            num += 1

        if child_idx == len(tree[current]):
            table[current].append(num)
            stack.pop()
        else:
            stack[-1][1] += 1
            stack.append([tree[current][child_idx], 0])

    

def solution_one(question):
    getTableTwo()

    for idx, q in enumerate(question):
        parent, child = q
        # print(table[parent], table[child])
        if (table[parent][0] < table[child][0]) and (table[parent][1] >= table[child][1]):
            print('#{} {}'.format(idx+1, 'T'))
        else:
            print('#{} {}'.format(idx+1, 'F'))
        
        if idx == 100000:
            return

################## solution 2 #####################
# 자식으로 부터 쭉 올라가서 직계인지 확인한다.
# 함정 코드.. 사람들이 이렇게 풀 확률이 높음..
# 이렇게 풀면 효율 안좋음
# 노드 십만개 질문 만개 기준 약 23초
def isTrue(parent, child):
    current_parent = my_parent[child]
    if current_parent == -1:
        return False

    while True:
        if current_parent == parent:
            return True
        if current_parent == 0:
            return False
        current_parent = my_parent[current_parent]

def solution_two(question):
    for idx, q in enumerate(question):
        parent, child = q

        result = 'T' if isTrue(parent, child) else 'F'
        print('#{} {}'.format(idx+1, result))
        if idx == 100000:
            return


# 노드 개수, 간선의 개수, 질문의 개수
start = time.time()
N, V, Q = map(int, input().split())
tree_info = list(map(int, input().split()))
question = []
for _ in range(Q):
    q = list(map(int, input().split()))
    question.append(q)

tree = [[] for _ in range(N+1)]

# solution two를 위한 부모 정보
my_parent = [-1 for _ in range(N+1)]

# 트리 만들기
for i in range(0, 2*V, 2):
    tree[tree_info[i]].append(tree_info[i+1])
    
    # solution two의 부모 정보 갱신
    my_parent[tree_info[i+1]] = tree_info[i]

# solution one을 위한 table
table = [[] for _ in range(N+1)]
# solution one을 위한 글로벌 변수 num
num = 0

# print(sys.getrecursionlimit())

# 출제자의 의도 코드
# solution_one(question)

# 흔히 푸는 방법 (함정 코드)
solution_two(question)

# 시간 확인
# print('total time :', time.time()-start)