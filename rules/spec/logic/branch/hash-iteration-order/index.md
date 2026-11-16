# HashSet / HashMap 遍历决定的输出顺序

agent 会看到什么：读到 Java 源码用 HashSet / HashMap 收集后经 keySet()、toArray()、new ArrayList<>(set) 遍历，结果决定输出内容或尝试、写入顺序；AC 只写「去重」，或写成插入序、以「本来无序」略过

## 规矩

- rule-30797d3e65e5｜源端用 HashSet/HashMap 遍历结果决定顺序时，AC 写明按 Java 迭代序｜读到：Java 源码用 HashSet / HashMap 收集后经 keySet()、toArray()、new ArrayList<>(set) 遍历，结果决定输出文件内容、尝试顺序、写入顺序或问题清单顺序；写错：AC 只写「去重」「HashSet 语义」，没写顺序；或写成按插入序；或以「HashMap 本来无序」略过
