# 面试编程题

> 前两天面试，前面面的好好的，最后挂在编程上面，主要是没有刷题。原因呢一是用 Python 刷题有一种作弊的感觉，二是短时间内写一道算法题并不能体现对数据结构和算法的理解程度，况且还有很多东西要学。但是没办法，从哪里跌倒从哪里爬起来。

## 1. 列表去重

```
l = ['b', 'b', 'c', 'd', 'b', 'c', 'a', 'a', 'e']

# 1. 集合法
list(set(l))

# 2. 列表推导法
l_1 = []
[l_1.append(i) for i in l if not i in l_1]
```

## 2. 序列计数

```
# 1. 字典法
def get_counts(sequence)
    counts = {}
    for s in sequence:
        if s in counts:
            counts[s] += 1
        else:
            counts[s] = 1
    return counts

# 2. pandas value_counts 方法
import pandas as pd
counts = pd.value_counts(sequence,sort = False)
```

## 3. 交叉链表求交点

主要思想是有交点后面肯定相同。从后开始比较，找到不同的两个前一个即为交点。如果是单向不可回溯的链表，则应该首先长度对其，再逐个比较，找到相同即为交点。

```
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

def node(l1, l2):
    if l1 == None or l2 == None:
        return None
    length1, length2 = 1, 1
    # 求两个链表长度
    head1 = l1
    head2 = l2
    while head1.next:
        head1 = head1.next  # 指向下一节点
        length1 += 1
    while head2.next:
        head2 = head2.next  # 指向下一节点
        length2 += 1
    
    if head1 != head2:  # 最后一个节点不同，肯定不相交
        return None
    
    # 长的链表先走
    if length1 > length2:
        for _ in range(length1 - length2):
            l1 = l1.next
    else:
        for _ in range(length2 - length1):
            l2 = l2.next
    while l1.next != l2.next:
        l1 = l1.next
        l2 = l2.next
    return l1.next
```

## 4. 多叉树求两点路径

该多叉树每一节点只有儿子节点没有父亲节点，和交叉链表求交点有相似之处。

```
"""
这里没有任何新奇之处，只是对多叉树选择了不同的逻辑存储结构，时间换空间。
只需要层次遍历顺序列表和各节点子节点个数列表即可唯一确定一棵树
层次遍历顺序列表形如[A, B, C, D, E, F, G, H, I, J,]
各节点子节点个数列表形如[1, 3, 3, 0, 3, 0, 3, 0, 3,]，最前面 1 是出于计算需要而加的
依据上面两个列表以及一个编号即可推算出父节点编号和该节点是父节点的第几个元素
"""


class Tree(object):
    """树节点"""

    def __init__(self, v, c=None):
        if c is None:
            c = []
        self.child = []
        self.value = v
        self.child.extend(c)


def fatherlist(num, fcnl=None, flist=None):
    """仅传两个参数 num 和 fcnl 即可。通过该节点的编号 num,获取父节点编号列表，并返回"""
    if fcnl is None:  # 如果子节点个数列表为 None 直接返回None
        print("子节点个数列表为空，无法计算")
        return None
    if flist is None:
        flist = []
    flist.insert(0, num)
    if num == 1:
        return
    s = fcnl[0]
    i = 0  # 每个 while 循环结束后 i 的值即为 num 父节点编号
    while s < num:
        i += 1
        s += fcnl[i]
    fatherlist(i, fcnl, flist)  # 递归求取父节点编号
    return flist  # 返回该节点及父节点编号列表

def main(x, y):
    # 对于存在子节点列表的节点树而言，层次遍历是最容易实现的遍历方式，
    # 正常的做法是通过层次遍历来实现上面两个列表，出于方便避免还需要输入一棵树，这里采用直接输入的方式，
    valuelist = ['A','B','C','D','E','F','G','H','I','J','K','L','N','O','P','Q','R','S','T']
    numlist = [1,3,3,0,3,0,3,0,3,0,0,0,0,3,0,0,0,0,0,0]
    # 通过查找获取 x, y 的编号,前提是 x, y 一定在valuelist 中
    i = valuelist.index(x) + 1
    j = valuelist.index(y) + 1
    f1 = fatherlist(i, numlist)  # x 父编号列表
    f2 = fatherlist(j, numlist)  # y 父编号列表
    k = 0
    while f1[k] == f2[k]:
        k += 1
    del f1[:k]
    del f2[:k-1]
    for m in f1:
        f2.insert(0, m)
    # 至此 f2 列表即为从 x 到 y 的路径编号
    print(len(f2))
    path = []
    for n in f2:
        path.append(valuelist[n-1])
    print(path)

if __name__ == '__main__':
    x = input("输入始节点 X 的值：")
    y = input("输入末节点 Y 的值：")
    # 如果 x, y 不是树中的值应该在形成 valuelist 和 numlist 时直接打印错误信息，结束程序
    main(x, y)
```

## 5. 最大子序列和

```
def max_subsequence(sequence):
    """
    返回最大值以及对应的最大子序列索引，如果该序列均为负值，则返回最大负数。该方法是最简单的遍历方式实现的，还有很大的优化空间。
    """
    max = sequence[0]
    subseq = [(0,0),]
    i = 0
    length = len(sequence)
    while i < length:
        max_t = sequence[i]
        sum = sequence[i]
        subseq_t = [(i,i),]
        j = i + 1
        while j < length:
            sum += sequence[j]
            if max_t < sum:
                max_t = sum
                subseq_t = [(i,j),]
            if max = sum:
                subseq_t.append((i,j))
            j += 1
        if max < max_t:
            max = max_t
            subseq = subseq_t
        if max == max_t:
            subseq += subseq_t
        i += 1
    return (max, subseq)
```

以上的遍历方式有很多工作是重复的，没有必要逐个遍历，也不是必须要循环到序列结束位置。
当上一个最大子序列和首尾位置确定的时候，下一个遍历的开始和结束位置也就可以确定了。
下面是优化版：

```
def max_subsequence(sequence):
    """
    返回最大值以及对应的最大子序列索引。
    i=0这个最大子序列是在遍历的基础上完成的，索引j 以后，自 j+1 开始的任意序列和一定是负值，之后的外循环求和的时候，后面的也就不用再循环相加了。
    j 之前开头的子序列不可能包含后半段，此时最大子序列要么在前半段，要么在后半段 (释义中的j指代子序列末尾索引)
    这个相比之前遍历的方式，依据之前做过的工作省去了许多没必要的遍历过程。
    """
    max = sequence[0]
    subseq = [(0,0),]
    i = 0
    length = len(sequence)
    end_index = length - 1
    while i < length:
        max_t = sequence[i]
        sum = sequence[i]
        subseq_t = [(i,i),]
        j = i + 1
        while j <= end_index:
            sum += sequence[j]
            if max_t < sum:
                max_t = sum
                subseq_t = [(i,j),]
            if max_t = sum:
                subseq_t.append((i,j))
            j += 1
        end_index = subseq_t[-1][1] 了
        if max < max_t:
            max = max_t
            subseq = subseq_t
        if max == max_t:
            subseq += subseq_t
        while i <= end_index and sequence[i] >= 0:  # 先找到第一个负值
            i += 1
        while i <= end_index and sequence[i] < 0:  # 再找到第一个正值
            i += 1
        if i > end_index:
            end_index = length - 1
            while i <= end_index and sequence[i] < 0:  # 直接找到另一部分的正值位置
                i += 1
    if max < 0:  # 因为是通过遍历正负值来优化的，未能求出最大负值位置
        return (0, None)
    return (max, subseq)
```
