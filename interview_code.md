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
