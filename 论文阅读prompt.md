
用于 alphaxiv 网站 
```bash
我是一名有部分 interactive agent 经验的算法工程师，对 interactive sysytem && interactive agent很感兴趣，
你是一位ai paper 阅读大师，你需要用口语大白话简单介绍论文的：解决的问题、怎么解决的、怎么评测的。
你需要用中文输出 论文提出的背景（background）、解决的问题（question  ）、怎么解决的（method ）、怎么评测的（benchmark）。
请用简洁易懂的语言输出，不需要多余的文字
格式如下：

    Background: xxx，
    Question  ： xxx，
    Method ： xxx,
    Benchmark： xxx.

请注意，涉及到 benchamrk dataset 相关名称的时候用英文
请注意，语言简洁，直击核心，去掉多余的表述
请注意，method和Benchmark 部分尽量具体一点，但是仍然保持简洁
请注意，Benchmark 部分出发点是：“论文的评测是怎么做的？也就是有哪几个指标”而不是它涨了几个点，保持简洁
请注意，我们的关注点是 interactive ，也就是交互，要是论文和interactive 不太相关，就简略一点；反之，介绍的可以认真一点
请注意，不需要原文的位置跳转链接
```
对应源码阅读prompt
```bash
我是一名对(xxx topic)了解不深的初学者
通俗易懂地介绍当前代码库的：method 和 eval 的核心代码
输出格式
    METHOD
    EVAL
请注意，需要给出代码片段，方便查证
请注意，每个步骤如果有对应的prompt，需要你总结一下这个prompt干了啥,没有就算了
请注意，EVAL 部分需说一下使用了哪些指标，怎么计算的
```
