# 源端按 HashSet/HashMap 遍历顺序产出结果时，目标用 Java 桶序复刻，不用插入序

审的是：代码
触发（任一种）：
- 读到：Java 源码 `HashSet<String>` / `HashSet<Integer>` / HashMap 收集后经 keySet()、toArray()、new ArrayList<>(set) 遍历，决定写入、尝试或输出顺序；写错的样子：ArkTS 用 new Set / new Map / Array.from(set) / indexOf 去重保持插入序，注释写「HashSet 无序 → 确定性输出」
适用范围：源端哈希集合的遍历顺序会落到文件内容、写入顺序、尝试顺序或清单顺序上时
做法：
- 按 Java 规则算序：hash = h ^ (h >>> 16)，h 是 String.hashCode（31 进制累加、32 位 int 回绕，可写 h = (Math.imul(31, h) + s.charCodeAt(i)) | 0）或 Integer.hashCode（值本身）；桶下标 (n - 1) & hash
- 容量 n 从 16 起，元素数超过 n × 0.75 时翻倍重排；遍历按桶下标从小到大、同桶按放入先后，用这个顺序替代 Set/Map 插入序
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hash(key) = (h = key.hashCode()) ^ (h >>> 16)，null 键为 0：扰动后的哈希（出处：java.util.HashMap#hash）
- tab[i = (n - 1) & hash]：桶下标，n 是当前容量（出处：java.util.HashMap#putVal）
- DEFAULT_INITIAL_CAPACITY = 1 << 4（16），DEFAULT_LOAD_FACTOR = 0.75f，++size > threshold 时 resize：默认容量、负载因子和扩容时机（出处：java.util.HashMap#DEFAULT_INITIAL_CAPACITY、HashMap#putVal）
- new HashSet() 背后是默认容量 16、负载因子 0.75 的 HashMap：HashSet 的顺序按 HashMap 算（出处：java.util.HashSet#HashSet()）
- String.hashCode = s[0]*31^(n-1) + s[1]*31^(n-2) + … + s[n-1]，int 运算：字符串键的哈希，按 32 位 int 溢出回绕（出处：java.lang.String#hashCode）
- Integer.hashCode(int value) 返回 value：整数键的哈希就是值本身（出处：java.lang.Integer#hashCode）
- do {} while (index < t.length && (next = t[index++]) == null)：迭代器按 table 下标从小到大找下一个非空桶（出处：java.util.HashMap.HashIterator）
未核实：卡里没给桶序工具的具体实现，计算步骤按框架源码写；同桶元素达到 TREEIFY_THRESHOLD（8）转成树后的遍历序未核实
来源：1 张卡，1 个应用
- case-119e8f2945fd9ff1c0c4（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2
