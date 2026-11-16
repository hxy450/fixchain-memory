# 超出 2^53 的 long 常量

agent 会看到什么：读到 Java 源码把 Long.MAX_VALUE 或别的超出 2^53 的 long 常量拼进 SQL 等字符串（如 CASE … ELSE " + Long.MAX_VALUE + " END 作哨兵）；产物里把它声明成 number 常量 9223372036854775807 再拼接

## 规矩

- rule-cf86fb053a86｜源码把 Long.MAX_VALUE 这类 long 常量拼进 SQL 时，目标用字符串字面量拼｜读到：Java 源码用字符串拼接把 Long.MAX_VALUE（或别的超出 2^53 的 long 常量）拼进 SQL，例如 CASE … ELSE " + Long.MAX_VALUE + " END 作哨兵；写错：目标声明成 number 常量 9223372036854775807 再拼进 SQL 字符串，实际拼出的是 9223372036854776000
