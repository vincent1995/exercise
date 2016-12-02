import math
import random
from sys import getsizeof
# 超大范围的不重复随机数生成
def rand_uint(letterCount,numberCount):
    numberRange = 26**letterCount
    eSet = set()
    while(len(eSet)<numberCount):
        n = random.randint(0,numberRange-1)
        if n not in eSet:
            eSet.add(n)
    return list(eSet)

# 生成字典
def create_dic(wordCount=10**6):
    minLetterCount = 5
    reqLetterCount = math.ceil(math.log(wordCount*2,26))
    letterCount = max(minLetterCount,reqLetterCount)
    numDict = rand_uint(letterCount,wordCount)
    wordDict = []
    while(len(numDict)>0):
        n = numDict.pop()
        word = []
        while(n != 0):
            c = chr(n % 26 + ord('a'))
            n = n//26
            word.append(c)
        wordDict.append(''.join(word))
    return wordDict


# 1.1 仅给定单词和地点
def sort_word(word):
    count = [0] * 26
    for c in list(word):
        count[ord(c) - ord('a')] += 1
    sorted_word = []
    for i in range(26):
        for j in range(count[i]):
            sorted_word.append(chr(i + ord('a')))
    sorted_word = str(sorted_word)
    return sorted_word
def test_1_1():
    given_word = "given"
    dic = create_dic()# 大小8Mb
    given_sig = sort_word(given_word)
    ans = []
    for word in dic:
        sig = sort_word(word)
        if(sig == given_sig):
            ans.append(word)
    print(ans[:10],len(ans))
# 1.2 预处理
def test_1_2():
    given_word = "given"
    words = create_dic()# 大小8Mb
    given_sig = sort_word(given_word)
    dic = {}
    while(len(words)>0):
        word = words.pop()
        sig = sort_word(word)
        if dic.get(sig) == None:
            dic[sig] = [word]
        else:
            dic[sig].append(word)
    ans = dic[given_sig]
    print(ans[:10],len(ans))

# 2 重复整数
# 32位整数一共有不到43亿个，因此43亿个数中一定存在重复的数。使用二分法。
def test_2():
    def create_data(r):
        n = list(range(0,r))
        rand = random.randrange(0,r)
        n.append(rand)
        random.shuffle(n)
        return n,rand
    rng = 10**5
    num,rand = create_data(rng)
    l = 0
    r = rng
    def count_num(l,r,num):
        c = 0;
        for i in num:
            if i>=l and i<r:
                c+=1
        return c
    while(r-l>1):
        m = (r+l)//2
        if count_num(l,m,num)>m-l:
            r = m
            continue
        elif count_num(m,r,num)>r-m:
            l = m
            continue
        else:
            raise Exception("input error")
    print(l,rand)
# 3.1 循环位移，单个移动
def move_juggle(word,step):
    l = len(word)
    si = 0 # 一轮的起始位置
    c = 0 # 移动次数
    while(1):
        tmp = word[si]
        i = si # 一轮中，数组空位下标
        while(1):
            ni = (i+step)%l # 待移动元素下标
            if ni == si:
                word[i] = tmp
                c+=1
                break
            word[i] = word[ni]
            i = ni
            c+=1
        if c < l: # 当移动次数和数组长度相同时终止
            si+=1
            continue
        else:
            break
    return "".join(word)
# 3.2 循环位移，迭代实现
def move_recursive(word,step):
    def move_word(word,strt,step):
        l = len(word)-strt
        if l > 2*step:
            tmp = word[strt:strt+step]
            word[strt:strt+step]=word[strt+step:strt+step*2]
            word[strt + step:strt + step * 2] = tmp
            return move_word(word,strt+step,step)
        else:
            tmp = word[strt:strt+step]
            left = word[strt+step:]
            word[strt:strt+len(left)] = left
            word[strt+len(left):strt+len(left)+step] = tmp
            return word
    ans = move_word(word,0,step)
    return "".join(ans)
# 4.1 循环位移，求逆算法
def move_reverse(word,step):
    def reverse(word):
        start = 0
        end = len(word)-1
        while(start<end):
            tmp = word[start]
            word[start] = word[end]
            word[end] = tmp
            start += 1
            end -= 1
        return word
    ans = reverse(reverse(word[:step])+reverse(word[step:]))
    return "".join(ans)
# 4.2 三种方法速度比较
# 没有得到书中所写的结果。书中强调高速缓存的性能问题。
# 可能和python的运行原理有关，或者和我的机器性能有关？
def test_4_2():
    from time import clock
    from matplotlib import pyplot as plt
    ans = {"juggle":[],"recur":[],"reverse":[]}
    whole_word = "abcdefghij"*100
    x = list(range(5,100))
    for step in x:
        word = list(whole_word)
        s = clock()
        move_juggle(word,step)
        e = clock()
        ans["juggle"].append(e-s)

        s = clock()
        move_recursive(word,step)
        e = clock()
        ans["recur"].append(e-s)

        s = clock()
        move_reverse(word,step)
        e = clock()
        ans["reverse"].append(e-s)
    plt.plot(x,ans["juggle"],label="juggle")
    plt.plot(x, ans["recur"],label="recursive")
    plt.plot(x, ans["reverse"],label="reverse")
    plt.legend()
    plt.show()
test_4_2()
# 5 (aTbTcT)T =cba

# 6 电话号码簿
# 和变位词同样的思路，使用拼写姓名按下的按键序列作为名字的标识
def test_6():
    def cal_num(word):
        num = []
        for c in word:
            asc = ord(c)-ord('a')
            n = asc//3+2
            if n>9:
                n = 0
            num.append(str(n))
        return ''.join(num)
    nameCount = 10**5
    name_list = create_dic(nameCount)
    dic = {}
    while(len(name_list)>0):
        name = name_list.pop()
        num = cal_num(name)

        if dic.get(num) == None:
            dic[num] = [name]
        else:
            dic[num].append(name)
    # 重复率
    sameCount = 0
    for i in dic.values():
        sameCount+=len(i)-1
    print(sameCount/nameCount)
    # 查询
    given_name = "vince"
    ans = dic.get(cal_num(given_name))
    print(ans)

# 8 O(nlogn):排序，取最小n个
#   O(nlogk):扫描一遍数据，过程中存储k个已经遇到元素中最小的元素。
# 实现第二种方法
def test_8():
    # 大顶堆
    def swap(a, i, j):
        temp = a[i]
        a[i] = a[j]
        a[j] = temp
    def insert_full_heap(a,n):
        def sort_heap(a,ind):
            l = ind*2+1
            r = ind*2+2
            if l>=len(a) or (a[ind]>=a[l] and (r>=len(a) or a[ind]>=a[r])):
                return
            elif r>=len(a) or a[l] >a[r]:
                swap(a, l, ind)
                sort_heap(a, l)
            else:
                swap(a, r, ind)
                sort_heap(a, r)
        if n>a[0]:
            return
        a[0] = n
        sort_heap(a,0)
    def insert_empty_heap(a,n):
        def up(a,ind):
            if ind==0:
                return
            p = (ind-1)//2
            if a[p] < a[ind]:
                swap(a,p,ind)
                up(a,p)
        ind = len(a)
        a.append(n)
        up(a,ind)
    num = rand_uint(2,100)
    k = 5
    t = 200
    s = []
    for n in num:
        if len(s) < k:
            insert_empty_heap(s,n)
        else:
            insert_full_heap(s,n)
    print(sum(s)<t,s)


# 9 k> nlogn/(n - logn)

