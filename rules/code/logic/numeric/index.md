# 数值运算

源端有 (float) 强转和 f 后缀字面量、Float 相等比较、算式里的倍率和偏移、超出 2^53 的 long 常量、模型字段的时间单位，目标端有 TS 的算式和数值常量时

## 触发族

- [源端 Float 相等比较和比值钳制](float-compare-ratio/index.md)（2 条）：读到源端 Kotlin 里用 == 比较 Float（toFloat() == value）、算比值时带零分母分支和 coerceIn(0f, 1f)，产物里是 TS 的比较表达式和进度计算
- [Java float 运算和截断](java-float-arith/index.md)（4 条）：读过的 Java 源表达式有 (float) 强转、60000.0f 这类 f 后缀字面量或 float 返回值，结果再 (int) 截断；交回的代码按 double 算再 Math.trunc，没有 Math.fround
- [源端算式里的倍率和偏移项](formula-offset-multiplier/index.md)（2 条）：读到源端算式在调用点或数据流里带倍率、偏移（实参写成进度 × 倍率、derivedStateOf，图表上下界写 max + 2 / min - 2）；产物里内联或重写的算式只照被调组件内部公式或数据极值写，少了这一项
- [两端模型同名数值字段的单位](model-field-unit/index.md)（1 条）：读到源端 Builder().setDuration(x) 一类链式构造逐字段直传数值，目标端来源模型和目标模型对同名数值字段注明不同单位（ms / 秒）；产物里 new 目标模型(…, src.字段, …) 原样传值，没有 / 1000 或 * 1000 换算
- [超出 2^53 的 long 常量](long-beyond-safe-integer/index.md)（1 条）：读到 Java 源码把 Long.MAX_VALUE 或别的超出 2^53 的 long 常量拼进 SQL 等字符串（如 CASE … ELSE " + Long.MAX_VALUE + " END 作哨兵）；产物里把它声明成 number 常量 9223372036854775807 再拼接
- [与源端或 Base 层同名的常量和哨兵值](sentinel-const-value/index.md)（2 条）：读到源端 const val 常量（实体字段默认值、companion object 里的哨兵）、Base 模型层 export const 的同名常量，而规格表给了另一个默认数值；产物里 export const 的数值照抄哪一边、偏好缺省和列表行 id 用的是哪一层的常量
- [调用实参里的字面数值](literal-call-args/index.md)（1 条）：读到源端调用的实参里直接写字面数值或换算式（如 角度 * 0.01745329252f）；产物里 seam 接口删了这些参数、只在注释里留参数名，或绑定处传了来源不明的数值（Math.PI / 18.0 一类）
