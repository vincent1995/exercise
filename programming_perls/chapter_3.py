# 1
# 两个数组，存储税收起点和税率
def test_1():
    tax_strt = [2000,3000,4000,6000,float('inf')]
    tax_rate = [0.14,0.17,0.24,0.40]
    income = 20000
    tax = 0
    for i in range(len(tax_strt)-1):
        if income < tax_strt[i]:
            break
        tax += (min(income-tax_strt[i],tax_strt[i+1]-tax_strt[i]))*tax_rate[i]
    print(tax)

# 2
# 计算k阶常系数
# 递归计算计算量非常大
# //TODO 递归计算的时间复杂度？
# 计算方法：
# k+1大小数组存储c，k大小数组存储最近的k个数。
def test_2():
    k = 5
    m = 6
    c = list(range(1,k+2))
    a = list(range(1,k+1))
    curIndex = k
    cur = 0
    while(curIndex<m):
        cur = 0
        for i in range(0,k):
            cur += c[i]*a[(curIndex+i)%k]
        cur += c[-1]
        a[curIndex%k] = cur
        curIndex +=1
    print(cur)

# 3
# 命令行图形化表示字母
# 自定义图形描述语言，编写解释器
# 描述语言：一行最多九个字符
# r+行重复次数；字符+该字符重复次数,s表示空格,忽略空格
# eg：'r3 s1#7s1 r3 s3#3s3 r3 s1#7s1' 是I
def InterpretLetter(dsc):
    cur = 0
    pic = []
    while(cur<len(dsc)):
        cur+=1
        r = int(dsc[cur])
        cur+=1
        line = []
        while(cur<len(dsc) and dsc[cur]!='l'):
            char = dsc[cur]
            if char ==' ':
                cur+=1
                continue
            elif char =='s':
                char = ' '
            cur +=1
            time = int(dsc[cur])
            line += [char]*time
            cur +=1
        for i in range(r):
            pic.append(line)
    return pic
def test_3():
    dic ={
        'C': "l2#6 l4#2 l2#6",
        'E':"l2#7 l2#2 l2#7 l2#2 l2#7",
        'H':"l4#2s3#2 l2#7 l4#2s3#2",
        "I":"l2#6 l4s2#2s2 l2#6"
    }
    letter = "C"
    pic = InterpretLetter(dic[letter])
    for l in pic:
        print("".join(l))
# 4 日期计算
# 日期表示：2016/08/08 可去掉0。
def InterpDate(ds):# 解释日期字符串
    date = [0,0,0] # 年月日
    dInd = 0
    sInd = 0
    while(sInd<len(ds)):
        v = ds[sInd]
        sInd += 1
        if v == '/':
            dInd +=1
            if dInd >= len(date):
                raise Exception("date error")
        else:
            v = int(v)
            date[dInd] = date[dInd]*10 + v
    return date
def test_4():
    MONTH_DAY = [31,0,31,30,31,30,31,31,30,31,30,31]
    WEEKS = ['Sun','Mon','Tue','Wen','Thu','Fri','Sat']
    STD_DS = "2016/12/03"
    STD_WEEK = 6
    def GetFebDay(year):
        if year%4 ==0 and year % 100 != 0 or year%400 ==0:
            return 29
        else:
            return 28
    def DaysInYear(year):# 计算一年几天
        return sum(MONTH_DAY)+GetFebDay(year)
    def DaysPassInYear(date):# 计算当年过去几天
        day = 0
        day += sum(MONTH_DAY[:(date[1]-1)]) # 过去的月
        if date[1]>2:
            day += GetFebDay(date[0]) # 本月过去的日
        day += date[2]
        return day
    def CmpDate(d1,d2): # 比较d1 d2 两个日期
        if d1[0] * 10 ** 4 + d1[1] * 10 ** 2 + d1[2] < d2[0] * 10 ** 4 + d2[1] * 10 ** 2 + d2[2]:
            return -1
        if d1[0] * 10 ** 4 + d1[1] * 10 ** 2 + d1[2] > d2[0] * 10 ** 4 + d2[1] * 10 ** 2 + d2[2]:
            return 1
        else:
            return 0
    def CalDay(ds1,ds2): # 计算两日期间的天数差。输入字符串
        d1,d2 = InterpDate(ds1),InterpDate(ds2)
        if CmpDate(d1,d2) < 0: #保证 d1更大
            tmp = d1
            d1 = d2
            d2 = tmp
        day1 = DaysPassInYear(d1)
        day2 = DaysPassInYear(d2)
        dayYear = 0
        for y in range(d2[0],d1[0]):
            dayYear+=DaysInYear(y)
        return dayYear+day1-day2
    def GetWeek(ds): # 给定日期，计算星期。输入字符串
        day = CalDay(ds,STD_DS)
        if CmpDate(InterpDate(ds),InterpDate(STD_DS)) < 0:
            day = day*-1
        return (day+STD_WEEK)%7
    def GetCalend(year,month): # 给年月，输出日历
        cal =[]
        cal.append("Year: "+str(year) +"  Month: " + str(month))
        line = []
        for w in WEEKS:
            line.append(w)
            line.append("\t")
        cal.append(line)

        line =[]
        wk = GetWeek(''.join([str(year),'/',str(month),'/1']))
        line += ["\t"]*wk
        day = 1
        md = MONTH_DAY[month-1]
        if month ==2:
            md = GetFebDay(year)
        while(day <= md):
            line+= [str(day)]+["\t"]
            day+=1
            wk = (wk+1)%7
            if wk == 0:
                cal.append(line)
                line = []
        if len(line)>0:
            cal.append(line)
        return cal
    cal = GetCalend(2016,11)
    for l in cal:
        print("".join(l))

# 5 后缀匹配
def test_5():
    SUFFIXS = ['et-ic','al-is-tic','s-tic','p-tic']
    word = "ppap-tic"
    s = None
    for suf in SUFFIXS:
        strt = len(word)-len(suf)
        find = True
        for i in range(len(suf)):
            if word[strt+i] != suf[i]:
                find = False
                break
        if find:
            s = suf
            break
    print(word,s)

# 6 格式生成器
# 格式： $后接数字n代表第n个参数，\用作转义。
def InterpretText(ts,args):
    t = []
    cur = 0
    getArg = False
    argNum = 0
    escape = False
    while(cur<len(ts)):
        c = ts[cur]
        if getArg:
            if ord(c) in range(ord('0'),ord('9')+1):
                argNum = argNum*10 + ord(c)-ord('0')
            else:
                t.append(args[argNum])
                t.append(c)
                argNum = 0
                getArg = False
        elif escape:
            t.append(c)
            escape = False
        elif c == '\\':
            escape = True
        elif c == "$":
            getArg = True
        else:
            t.append(c)
        cur+=1
    return ''.join(t)
def test_6():
    ts = r"Hello \$ $0 \\ !"
    text = InterpretText(ts,["World"])
    print(text)
