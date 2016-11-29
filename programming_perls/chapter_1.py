import numpy as np
import random
import math

# 1 调用库
def test_1():
    a = [3,4,5,2,6,7,5,6,7,89,4,5,6]
    a = sorted(a)
    print(a)

# 2 位图的实现
BITS_PER_WORD = 32
MASK = 0x1f
SHIFT = 5
def set(i, bitMap):
    bitMap[i >> SHIFT] |= 1 << (i & MASK)
def clr(i, bitMap):
    bitMap[i >> SHIFT] &= ~(1 << (i & MASK))
def test(i, bitMap):
    return (bitMap[i >> SHIFT] & (1 << (i & MASK))) != 0
def create_bitmap(numberSize):
    return  np.zeros(math.ceil(numberSize/BITS_PER_WORD),dtype=np.uint32)
def test_2():
    numberSize = 10**6
    bitMap = create_bitmap(numberSize)
    set(1,bitMap)
    set(2,bitMap)
    print(test(1,bitMap))
    clr(1,bitMap)
    print(test(1,bitMap))
    print(test(2,bitMap))


# 3 位图排序
def test_3():
    numberRange = 10**6
    a = list(range(0,numberRange))
    random.shuffle(a)
    bitMap = create_bitmap(numberRange)
    for i in a:
        set(i,bitMap)
    b = []
    for i in range(0,numberRange):
        if test(i,bitMap):
            b.append(i)
    print(b[:10])

# 4 随机数
# python中
def shuffle_rand(numberRange,numberCount):
    a = list(range(0, numberRange))
    random.shuffle(a)
    a = a[:numberCount]
    return a
def test_4():
    numberRange = 10**6
    numberCount = 7*10**5
    a = shuffle_rand(numberRange,numberCount)
    print(a[:10])

# 5 1MB严格边界   使用两趟算法
def test_5():
    # 推广到n趟算法
    runTime = 2
    numberCount = 8*10**5
    numberRange = 10**6
    a = shuffle_rand(numberRange,numberCount)
    b = []
    for n in range(0,runTime):
        r = [int(numberRange*n/runTime),int(numberRange*(n+1)/runTime)] # 左闭右开
        bitMap = create_bitmap(r[1]-r[0])
        for i in a:
            if i >=r[0] and i < r[1]:
                set(i-r[0],bitMap)
        for i in range(0,r[1]-r[0]):
            if test(i,bitMap):
                b.append(i+r[0])
    print(b[:10],b[-10:],len(b))
# 6 最多出现10次， 位图中4个bit保存一个数
# 1MB 可以保存 2^21次方个数，一共10^7次方个数，所以至少需要运行 (10^7)/(2^21) 大约5趟算法
def test_6():
    NUM_PER_WORD = 8
    MASK = 0x7
    SHIFT = 3
    def create_bitmap(numberRange):
        return np.zeros(math.ceil(numberRange/NUM_PER_WORD),dtype=np.uint32)
    def set(i,bitMap):
        bitMap[i>>SHIFT] += 1<<((i&MASK)*4)
    def test(i,bitMap):
        return ( bitMap[i>>SHIFT]>>(i&MASK)*4 )&0xf
    def multi_shuffle_rand(multi,numberRange,numberCount):
        a = []
        for i in range(0,multi):
            a += list(range(0,numberRange))
        random.shuffle(a)
        return a[:numberCount]
    numberRange = 10**6
    numberCount = 8*10**5
    runTime = 5
    a = multi_shuffle_rand(10,numberRange,numberCount)
    b = []
    for n in range(0,runTime):
        r = [int(numberRange*n/runTime),int(numberRange*(n+1)/runTime)] # 左闭右开
        bitMap = create_bitmap(r[1]-r[0])
        for i in a:
            if i >=r[0] and i < r[1]:
                set(i-r[0],bitMap)
        for i in range(0,r[1]-r[0]):
            if test(i,bitMap) > 0:
                c = test(i,bitMap)
                for j in range(0,c):
                    b.append(i + r[0])
    print(b[:10],b[-10:],len(b))
# 7 错误检查
# 输入可能的错误：
# 1、小于0，大于n
# 2、输入重复
# 3、输入数据类型错误，比如为float，或者是字符串
# 推广到n趟算法
def test_7():
    def check_num(i,r):
        if isinstance(i,int) and i<r and i>=0:
            pass
        else:
            raise Exception("input error")
    runTime = 2
    numberCount = 8*10**5
    numberRange = 10**6
    a = shuffle_rand(numberRange,numberCount)
    b=[]
    a.append(1)
    a.append(1)
    for n in range(0,runTime):
        r = [int(numberRange*n/runTime),int(numberRange*(n+1)/runTime)] # 左闭右开
        bitMap = create_bitmap(r[1]-r[0])
        for i in a:
            check_num(i,numberRange)# 判断输入类型范围是否正常
            if i >=r[0] and i < r[1]:
                if test(i-r[0],bitMap):
                    raise Exception("input error")
                set(i-r[0],bitMap)
        for i in range(0,r[1]-r[0]):
            if test(i,bitMap):
                b.append(i+r[0])
    print(b[:10],b[-10:],len(b))
# 8
#########
# 1、增加区号
# 不同区号号码分别排序。多趟算法，每个区号需要两趟
# 2、快速查找
# 将生成的每个位图保存，根据查询号码范围查找对应位图。
def test_8_1():
    def rand_with_area_code(numberRange,numberCount,areaCode):
        a = list(range(0, numberRange))
        random.shuffle(a)
        a= a[:numberCount]
        acSize = len(areaCode)
        for i in range(0,len(a)):
            ac = str(areaCode[random.randint(0,acSize-1)])
            a[i] = ac + "-"+str(a[i])
        return a
    areaCode = [800,888,887]
    runTime = 2
    numberCount = 8 * 10 ** 5
    numberRange = 10 ** 6
    a = rand_with_area_code(numberRange,numberCount,areaCode)
    b = []
    sorted(areaCode)
    for ac in areaCode:
        for n in range(0, runTime):
            r = [int(numberRange * n / runTime), int(numberRange * (n + 1) / runTime)]  # 左闭右开
            bitMap = create_bitmap(r[1] - r[0])
            for i in a:
                curNumber = int(i.split('-')[1])
                curAreaCode = int(i.split('-')[0])
                if curNumber >= r[0] and curNumber < r[1] \
                        and curAreaCode == ac:
                    set(curNumber - r[0], bitMap)
            for i in range(0, r[1] - r[0]):
                if test(i, bitMap):
                    b.append(str(ac) + "-"+str(i + r[0]))
    print(b[:10], b[-10:], len(b))

