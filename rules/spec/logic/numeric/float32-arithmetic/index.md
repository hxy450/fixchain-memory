# Java 源表达式里的 float 运算和 (int) 截断

agent 会看到什么：读到 Java 源表达式有 (float) 强转、f 后缀字面量或 float 返回值，结果随后 (int) 截断或比较；验收样例按实数或 double 心算，没有一个 float 与 double 结果不同的样例

## 规矩

- rule-2f2daaf18ccb｜源式按 float 运算时，验收样例按 float32 逐步算，并给一个与 double 不同的样例｜读到：Java 源表达式有 (float) 强转、f 后缀字面量或 float 返回值，结果随后 (int) 截断或比较；写错：验收样例按实数或 double 心算得出（如把 255×(1/3) 记成 85），没有一个 float 与 double 截断结果不同的样例；样例值落在整数或 .5 边界附近也没按 float32 复核
- rule-96fac647faab｜源式有 (float) 强转或 f 字面量再截断时，规格映射把 float 运算和收窄分两行｜读到：Java 源表达式出现 (float) 强转、60000.0f 这类 f 后缀字面量或 float 字段、返回值，结果随后 (int) 截断或参与比较；写错：规格的实现映射只写「(int) float→int 收窄 → Math.trunc + 显式饱和」或「正常值 Math.trunc 等价」，公式去掉了 f，没写每步按 float32 舍入
