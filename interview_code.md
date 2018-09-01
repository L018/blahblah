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
