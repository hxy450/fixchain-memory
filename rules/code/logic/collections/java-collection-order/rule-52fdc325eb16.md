# HashMap 遍历后再排序时，目标模拟 HashMap 迭代序和 compareToIgnoreCase

审的是：代码
触发（任一种）：
- 读到：源码用 HashMap<String, Integer> / HashSet 聚合后遍历 entrySet / keySet，再 Collections.sort(…, compareToIgnoreCase) 一类排序；写错的样子：目标用 JS Map 插入序聚合，排序用整串 toLowerCase() 比较，注释写「compareToIgnoreCase 等价」
适用范围：源端结果顺序依赖 HashMap / HashSet 迭代序（含排序后比较相等的项）时
做法：
- 排序前的顺序照 HashMap 迭代序模拟：键的 hashCode 做 h ^ (h >>> 16)，按 (容量 - 1) & hash 分桶，默认容量 16、负载因子 0.75 时扩容，桶内按插入序
- compareToIgnoreCase 逐字符先 toUpperCase 再 toLowerCase 后比较；Collections.sort 是稳定排序，比较相等的项保持迭代序
- 写「等价」注释前用大小写变体的键（如 Tag / tag）自测
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- HashMap 不保证顺序，也不保证顺序随时间不变：JS Map 的插入序和它不同（出处：java.util.HashMap（类注释））
- hash(key) = (h = key.hashCode()) ^ (h >>> 16)；桶下标 (n - 1) & hash：模拟迭代序用的散列和分桶（出处：java.util.HashMap#hash、java.util.HashMap#putVal）
- DEFAULT_INITIAL_CAPACITY = 16，DEFAULT_LOAD_FACTOR = 0.75f：默认容量和扩容阈值（出处：java.util.HashMap#DEFAULT_INITIAL_CAPACITY、java.util.HashMap#DEFAULT_LOAD_FACTOR）
- String.hashCode = s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]（int 溢出）：字符串键的 hashCode（出处：java.lang.String#hashCode）
- compareToIgnoreCase 对每个字符做 Character.toLowerCase(Character.toUpperCase(c)) 后比较：不是整串 toLowerCase（出处：java.lang.String#compareToIgnoreCase）
- List.sort 默认实现是稳定的归并排序：相等项保留原顺序（出处：java.util.List#sort）
- 修好后按 HashMap 迭代序模拟键顺序（旧实现在构造用例上错 2156 例）：修好后的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-e9189514e875ef00f96f（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 7 ← 诊断
