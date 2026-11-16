# 深链或路由的 query 解析写成可导出的工具函数，不写成 @Entry 页面的私有方法

审的是：代码
触发（任一种）：
- 写错的样子：query 取值函数写成 @Entry 页面里的 private 方法，多个深链或路由分支各自调用它或复制一份
适用范围：目标端解析深链、want.uri 或路由 query 参数的代码
做法：
- 放到 utils 下导出的 getQueryValue(query, key)，各路由分支 import 共用同一实现，删掉页面里的私有副本
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 新建工具模块导出 getQueryValue，删除页面私有取值函数并替换全部调用点：修复后的结构（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9fe714b7ae5de2097fcf（Countdate）：做法第 1 步 ← 建议 3、诊断；取值 1 ← 诊断
