# 资源里保留 @string/ 引用数组时，代码级映射表为每个消费方登记解析义务

审的是：计划与派工
触发（任一种）：
- 读到：转换规则写明 @string/name → $string:name，资源产物的 strarray 条目仍是 '@string/…'；写错的样子：资源映射的「代码级映射」表只给 @drawable 图标数组登记了消费方义务，保留 '@string/…' 的 strarray 数组没有登记
适用范围：资源转换阶段确需把 @string/ 引用原样留在 strarray 里、交给代码侧处理时
做法：
- 在代码级映射表里逐个列出保留 '@string/…' 的数组名，写明所有消费方读出后对 '@string/' 前缀逐项调 resourceManager.getStringByNameSync(name) 解析
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringByNameSync(resName: string): string：按资源名取字符串，登记里写的解析方法（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringByNameSync）
来源：1 张卡，1 个应用
- case-a0ce76f2b62e29f7e625（opencamera-hmos）：做法第 1 步 ← 建议 1
