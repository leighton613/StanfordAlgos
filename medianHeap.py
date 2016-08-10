
# coding: utf-8
"""
GOAL: 
1. Median Maintenance algorithm; 
2. you should treat this as a stream of numbers, arriving one by one;
3. Compute the last 4 digits of summation of all medians.
"""

class Heap:
    ## -------- Nonpublic Behavior
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left(self, i):
        return 2 * i + 1
    
    def _right(self, i):
        return 2 * i + 2
    
    def _has_left(self, i):
        return len(self._data) > self._left(i)
    
    def _has_right(self, i):
        return len(self._data) > self._right(i)
    
    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
        
        
    def _bubble_up(self, val):
        raise NotImplementedError('must be implemented by subclass')
        
    def _bubble_down(self, val):
        raise NotImplementedError('must be implemented by subclass')

    def _is_empty(self):
        return self.__len__() == 0
    
    ## -------- Public Behavior
    def __init__(self):
        self._data = []
        
    def __len__(self):
        return len(self._data)
    
    def add(self, val):
        self._data.append(val)
        self._bubble_up(len(self._data)-1)
    
    def pop(self):
        if self._is_empty():
            raise ValueError("Empty heap")
        self._swap(0, len(self._data)-1)
        val = self._data.pop()
        self._bubble_down(0)
        return val
    



class minHeap(Heap):    
    def min(self):
        if self._is_empty():
            raise ValueError('empty heap')
        return self._data[0]
    
    def _bubble_up(self, i):
        parent_idx = self._parent(i)
        if i > 0 and self._data[i] < self._data[parent_idx]:
            self._swap(i, parent_idx)
            self._bubble_up(parent_idx)
            
    def _bubble_down(self, i):
        if self._has_left(i):
            left = self._left(i)
            small_one = left
            if self._has_right(i):
                right = self._right(i)
                if self._data[right] < self._data[left]:
                    small_one = right
            
            # has the smaller one
            if self._data[i] > self._data[small_one]:
                self._swap(i, small_one)
                self._bubble_down(small_one)

class maxHeap(Heap):
    def max(self):
        if self._is_empty():
            raise ValueError('empty heap')
        return self._data[0]
    
    def _bubble_up(self, i):
        parent_idx = self._parent(i)
        if i > 0 and self._data[i] > self._data[parent_idx]:
            self._swap(i, parent_idx)
            self._bubble_up(parent_idx)

    def _bubble_down(self, i):
        if self._has_left(i):
            left = self._left(i)
            large_one = left
            if self._has_right(i):
                right = self._right(i)
                if self._data[right] > self._data[left]:
                    large_one = right
            
            # has the larger one
            if self._data[i] < self._data[large_one]:
                self._swap(i, large_one)
                self._bubble_down(large_one)



class medianHeap(object):
    def __init__(self):
        self.minH = minHeap()
        self.maxH = maxHeap()
    
    def showBoth(self):
        print "minHeap:", self.minH._data
        print "maxHeap:", self.maxH._data
        
    def sumMedian(self, filename):
        fh = open(filename)
        cnt = 0
        sumMed = 0
        for line in fh:
            cnt += 1
            num = int(line.strip())
            if cnt == 1:
                first = num
                sumMed += first
            elif cnt == 2:
                self.minH.add(max([first, num]))
                self.maxH.add(min([first, num]))
                sumMed += self.maxH.max()
            else:
                if num <= self.maxH.max():
                    self.maxH.add(num)
                else:
                    self.minH.add(num)
                
                ## balance
                if abs(len(self.minH) - len(self.maxH)) > 1:
                    if len(self.minH) > len(self.maxH):
                        while len(self.minH) - len(self.maxH) > 1:
                            self.maxH.add(self.minH.pop())
                    else:
                        while len(self.maxH) - len(self.minH) > 1:
                            self.minH.add(self.maxH.pop())
                            
                assert(abs(len(self.minH) - len(self.maxH)) <= 1)
                
                ## find median
                if len(self.minH) > len(self.maxH):
                    sumMed += self.minH.min()
                else:
                    # as the def its k/2 th element 
                    sumMed += self.maxH.max()
        
        fh.close()
        return sumMed%10000



def Solution():
    medHeap = medianHeap()
    print medHeap.sumMedian("Median.txt")



if __name__ == "__main__":
    Solution()
