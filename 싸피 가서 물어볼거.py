class Trie:
    head = {}
    
    def add(self, word):
        cur = self.head
        
        for ch in word:
            if ch not in cur:
                cur[ch] = {}
            cur = cur[ch]
        
        cur[ch] = True # 다 끝나고 마지막 ch를 True라고 설정
    
    def search(self, word):
        cur = self.head
        
        for ch in word:
            if ch not in cur:
                return False
            cur = cur[ch]

        if cur[ch] == True: # 마지막 ch에서 True라면 단어가 있음
            return True
        else:
            return False # 마지막 ch의 값이 True가 아니라면 해당 단어는 없는거임(더 길거나 짧음)
    
    def remove(self, word):
        cur = self.head
        
        for ch in word:
            cur = cur[ch]
        cur[ch] = False
    
diction = Trie()

diction.add("hi")
diction.add('hello')
print(diction.search('hi'))
print(diction.search('hell'))



# 세그먼트 부분

from math import ceil, log

arr = [1, 6, 2, 4, 8, 3, 7]

class segment():
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.tree = [0] * (len(arr) * 4)
        # 어떤 사람은 값을 받을 때 [0] * (2**ceil(log(len(arr), 2)+1))로 받던데 트리의 남는 공간을 최소화 하려는건가?

    def build(self, left, right, i=1):  # 왼쪽 끝, 오른쪽 끝, I
        if left == right:
            self.tree[i] = self.arr[left]
            return self.tree[i]

        mid = (left + right) // 2
        self.tree[i] = self.build(left, mid, i * 2) + self.build(mid + 1, right, i * 2 + 1)
        return self.tree[i]

    '''start = 구간의 왼쪽 end = 구간의 오른쪽, left = 찾는 범위 왼쪽, right = 찾는 범위 오른쪽
    만약 인덱스 3~5까지를 찾으려면 search(0, 6, 3, 5) 하면 될 듯

    얼추 이해는 되고 있는데 start랑 end를 그냥 0, len(arr)-1로 고정해도 되는거 아닌가?
    search에서도 그렇고 update도 그렇고 계속 고정값으로 받고 있는데?
    만약 start랑 end값을 다르게 받으면 어떤 식으로 범위가 새로 설정되는지 이해가 안됨'''

    def search(self, start, end, left, right, i=1):
        if end < left or start > right: # 찾으려는 범위가 전체 구간의 안쪽인지 확인
            return 0

        if left <= start and end <= right: # 여기가 좀 이해가 안됨. 아마 덩어리 부분 찾는거 같은데..
            return self.tree[i]

        mid = (start + end) // 2 # 해당 범위에 있는게 맞다면 반씩 가르면서 찾는 범위가 어디있나 확인
        return self.search(start, mid, left, right, i * 2) + self.search(mid + 1, end, left, right, i * 2 + 1)

    def update(self, start, end, target, diff, i=1):  # 근데 이러면 해당되는 리프노드는 안바뀌는거 아닌가??
        if target < start or target > end:  # 바꾸려는 위치가 구간의 안쪽이어야 한다(현재 구간에 해당되어야 한다)
            return
        self.tree[i] += diff  # 리프노드까지 들어가면서 차이를 다 더해줌
        if start != end:  # 리프노드가 아니라면 아래의 재귀 시작
            mid = (start + end) // 2
            # 아래 과정에서 재귀를 들어갔을 때 둘 중 하나에서 현재 함수의 첫 줄에 걸러지게 됨
            self.update(start, mid, target, diff, i * 2)  # 0~6이던 구간을 0~3으로 바꿈
            self.update(mid + 1, end, target, diff, i * 2 + 1)  # 구간을 4~6으로 바꿈


seg = segment(arr)
seg.build(0, len(arr) - 1, 1)
print(seg.search(0, 6, 2, 4), seg.tree)
seg.update(0, 6, 3, 1)  # 이거 왜 2번째 레벨까지는 바뀌는데 왜 3번째부터 안바뀌지??
print(seg.search(0, 6, 2, 4), seg.tree)