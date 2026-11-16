# Java float 运算和截断

agent 会看到什么：读过的 Java 源表达式有 (float) 强转、60000.0f 这类 f 后缀字面量或 float 返回值，结果再 (int) 截断；交回的代码按 double 算再 Math.trunc，没有 Math.fround

## 规矩

- rule-59feaf4437cc｜源式按 Java float 运算时，目标每个操作数和每步结果包 Math.fround 再收窄｜读到：Java 源表达式有 `(float)` 强转、`60000.0f` 这类 f 后缀字面量或 float 返回类型，结果再 `(int)` 截断；写错：目标写成 double 表达式再截断，如 Math.trunc(a * (60000.0 / b))，没有 Math.fround；同一公式在几个方法里各写一遍
- rule-1f48a38dfe40｜源式里有 (int) 截断时，目标用 Math.trunc 原样保留，不留浮点｜读到：Java 源式里有 `(int)` 强转或 `Math.floor` 等取整，如 `(int) ((descent() + ascent()) / 2)`；写错：目标写成不取整的浮点表达式，没有 `Math.trunc(` 或对应的取整
- rule-93a24c6c6baa｜Kotlin 的 Float.toInt() 迁成 Math.trunc，不写成 Math.round｜读到：Kotlin 里 fontSize = state.toInt() 或标题文本里 slider 值 .toInt()；写错：目标标题和落库都写成 Math.round(…)
- rule-495b49d4f378｜Math.round((float) a / b) 一类移植时逐步 Math.fround 再舍入，NaN 得 0｜读到：源码 Math.round((float) completed / items * 100) 一类 float 运算后取整；写错：目标用 double 直接 Math.round(a / b * 100)，只处理了 NaN
