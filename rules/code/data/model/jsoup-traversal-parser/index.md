# Jsoup 节点遍历改写成的自研解析器

agent 会看到什么：读到 Jsoup 的 Element / TextNode 遍历（wholeText 计数、pre / table 分支、pushId(element.id())、按元素 ids 建锚点下标）；产物里自研解析器的 appendText / pushElement 计数和上限检查的位置、线性元素有没有 ids 字段

## 规矩

- rule-50cafb889ee2｜自研解析器替代 Jsoup 遍历时，计数和截断检查放在源码相同位置、所有上限一起查｜读到：源端遍历 Jsoup 节点时对每个 `TextNode` 先累加 wholeText 的长度、再按块样式（pre、table）分支；追加元素时同一处同时判断元素数上限和字符数上限；写错：目标 appendText 在 pre / table 分支 return 之后才累加字符数；pushElement 只查元素数上限，不查字符数上限
- rule-199865db7074｜源端线性元素带 ids、按元素 ids 建锚点下标时，目标模型保留 ids，不用比例映射｜读到：源端遍历时对每个元素 pushId(element.id())，线性元素构造时带 ids；锚点表按 elements.mapIndexed 取每个元素的 ids() 映射到它的真实下标；写错：目标的线性元素类型没有 `ids` 字段；下游另写函数把 HTML 里的 id 按出现顺序、按比例映射到元素下标，差异清单里也没记
