# List.remove(Object) 移植成 indexOf 加 splice 原地删第一个，不用 filter

审的是：代码
触发（任一种）：
- 读到：源码 list.remove(obj)（List.remove(Object)），元素类没有覆写 equals；写错的样子：目标写 this.list = this.list.filter(item => item !== obj)：新建数组并删掉全部相同对象
适用范围：把 Java List.remove(Object) 翻译成 ArkTS 数组操作时
做法：
- const i = list.indexOf(obj); if (i >= 0) { list.splice(i, 1) }：原地删除第一个相同元素
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- List.remove(Object) 删除第一次出现的指定元素：只删一个，原地改列表（出处：java.util.List#remove(Object)）
- splice(start: number, deleteCount?: number): T[]，原地删除并返回被删元素：原地删的写法（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，Array.splice）
- filter 返回满足条件的元素组成的新数组：会新建数组、删掉全部匹配项（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，Array.filter）
- 修好后改为 indexOf + splice：修好后的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-e9189514e875ef00f96f（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
