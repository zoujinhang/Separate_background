# Separate_background （背景分离算法）

## 背景分离算法的介绍

该算法主要是针对Fermi卫星的GBM探测器的TTE数据。在数据处理的过程中我们往往需要先估算信号背景，如果使用TTE数据进行背景的估算首先要对TTE数据进行切片统计（TTE数据记录了探测器测量到的光子的能道和光子的到达时间）。然而这样的计算往往要考虑切片的大小，因为不同的切片大小会影响信噪比。我们发现，通过光子与光子之间的等待时间可以统计出一段时域内的的计数比率。为了估计一个光子对应的计数比率，我们需要通过这个光子于周围的其他光子的时间间隔来获得该光子处的计数比率的概率，通过统计推导我们发现该光子的平均等待时间的倒数对应计数比率的概率最大值处。也就是说，平均等待时间的的倒数可以代表计数比率。为了得到每个光子处的计数比率，我们通过一种特别的高斯卷积，来获得每个光子对应的平均等待时间，这样就可以得到每个光子对应的计数比率了。

针对背景的计算，我们使用的是R语言中的baseline算法。我们对该算法python化并对其进行了相关的优化使其可以更好的适应时域分析。在评估背景时我们需要TTE数据进行切片统计，对于背景的估算而言，切片长度对计算结果基本没有影响。因此我们采用1s的切片长度，并将其作为一个恒定的内部参数。之后通过插值法获得每个光子对应的背景计数比。

我们在得到一个光子的计数比率和背景计数比率到底有何用途？通过这两个比率我们可以得到一个光子来自背景的概率。如果说计数比率代表光子出现概率，那么背景比率则代表光子来自背景的概率。这样我们就可以根据这两个概率来区分光子从而达到区分光子的目的。而区分的方法我们可以参考马尔科夫过程。首先在光子计数的数值范围内生成一个均匀随机的随机数，然后让昌盛的随机数与背景比率进行比较，随机数小于背景比率，光子将判定为背景光子。这个过程并不改变样本总体的统计特性。

最终我们的到的结果如下面三幅图：

1). 下面这幅图展示的是原始的TTE数据，图中每一个黑色点代表一个光子。

![figure 1](https://github.com/zoujinhang/Separate_background/tree/master/picture/A_original.png)

2). 下面这幅图展示的是算法分离处理的背景光子。

![figure 2](https://github.com/zoujinhang/Separate_background/tree/master/picture/A_b.png)

3). 下面这幅图展示的扣除背景光子的GRB事件。

![figure 3](https://github.com/zoujinhang/Separate_background/tree/master/picture/A_s.png)





