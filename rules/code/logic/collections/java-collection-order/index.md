# Java 集合的遍历顺序和入队语义

agent 会看到什么：读过的 Java 源码用 HashSet / HashMap 遍历决定输出顺序，或用 List.addAll 整批入队、不去重不设上限；交回的代码改成 Set / Map 的插入序，或加了去重、截断

## 规矩

- rule-5ddf92e8bb63｜源端按 HashSet/HashMap 遍历顺序产出结果时，目标用 Java 桶序复刻，不用插入序｜读到：Java 源码 `HashSet<String>` / `HashSet<Integer>` / HashMap 收集后经 keySet()、toArray()、new ArrayList<>(set) 遍历，决定写入、尝试或输出顺序；写错：ArkTS 用 new Set / new Map / Array.from(set) / indexOf 去重保持插入序，注释写「HashSet 无序 → 确定性输出」
- rule-b1b123831a23｜源端 addAll 整批入队、不去重不设上限时，目标照样整批入队，不加去重和截断｜读到：源端单例窗口的队列用 List.addAll(list) 整批入队、get(0) 后 remove(0) 逐个播放，没有按 id 去重，也没有 size() 上限；响应里的列表用 JSON.parseArray 整批解析后交给它；写错：目标队列多了按 id 去重的 Set、超过常量条数就丢弃的截断，或解析时用 Math.min(数组.length, 常数) 只取前若干条
- rule-4c7e4ddd04ce｜多选导出时按源集合的勾选顺序导出，不用展示列表 filter 代替｜读到：源码用 mutableStateListOf 维护选中集合，勾选时 add、取消时 remove，导出时 selected.forEach 依次 put；写错：目标导出用 this.list.filter(item => isSelected(item.id)) 取选中项，导出顺序变成列表顺序
- rule-eaee696b93ea｜List.remove(Object) 移植成 indexOf 加 splice 原地删第一个，不用 filter｜读到：源码 list.remove(obj)（List.remove(Object)），元素类没有覆写 equals；写错：目标写 this.list = this.list.filter(item => item !== obj)：新建数组并删掉全部相同对象
- rule-52fdc325eb16｜HashMap 遍历后再排序时，目标模拟 HashMap 迭代序和 compareToIgnoreCase｜读到：源码用 HashMap<String, Integer> / HashSet 聚合后遍历 entrySet / keySet，再 Collections.sort(…, compareToIgnoreCase) 一类排序；写错：目标用 JS Map 插入序聚合，排序用整串 toLowerCase() 比较，注释写「compareToIgnoreCase 等价」
