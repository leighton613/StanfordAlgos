
# coding: utf-8

"""

GOAL: 2-SUM algorithm, compute the number of **target values t** in the interval [-10000,10000] (inclusive),
such that there are distinct numbers x,y in the input file that satisfy x+y=t
 
FILE: contains integers, both positive and negative, with the ith row of the file specifying the ith entry of the array.

"""

def numTarget2(filename, rg):
    fh = open(filename)
    mapping = {}
    cnt = 0
    for line in fh:
        num = int(line.strip())
        if mapping.get(num) == None:
        	cnt += 1
            mapping[num] = cnt
    fh.close()
    print "Loaded distinct {0} numbers".format(cnt)
    
    CNT = 0
    for t in rg:
        for num in mapping:
            if t-num != num and t-num in mapping:
                print "Found at t = %d: (%d, %d)" %(t, num, t-num)
                CNT += 1
                break
    print "Valid Pairs: {0}".format(CNT)



def Solution():
    numTarget2("algo1-programming_prob-2sum.txt", range(-10000,10001))



if __name__ == "__main__":
    Solution()
