# 新增 import 并让本文件类 extends 它前，先查对方是否间接导入回本文件，是则先移到叶子模块

审的是：代码
触发（任一种）：
- 写错的样子：新加 `import { X } from M` 并写 `class … extends X`（或在模块顶层、类静态初始化里用 X），而 M 直接或间接 import 回本文件；运行时报 `ReferenceError: X is not initialized`
适用范围：接线或结构修补时，让本文件的类继承另一模块导出的类，或在模块顶层、类静态块里使用它时
做法：
- 写之前查 M 的 import 行，以及 M 导入的各模块（尤其页面）的 import 行，看是否直接或间接引回本文件
- 成环时先把 X 移到不导入页面的叶子模块再继承，或改用不需要继承的满足方式
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- extends 是模块求值期依赖：环里路由模块先加载时，子类模块求值读到尚未初始化的基类，HAP 启动即 ReferenceError：崩溃的成因；编译门和结构检查都不检测运行期模块初始化顺序（出处：卡里修好并验证过）
- const i = A.a; // 报错信息：Error message:A is not initialized：官方示例：模块间循环依赖时，在模块顶层访问对方导出类的静态属性或实例化它即报未初始化（出处：faqs-arkts-module.md，模块间循环依赖 - class）
- B 文件导入的 A 变量没有在全局或类静态中被使用时正常执行，反之报未初始化：只在函数体里用到对方导出不会崩，在求值期用到才会（出处：arkts-module-faq.md，Object is not initialized）
来源：1 张卡，1 个应用
- case-a5951acfc4d0e4117f1d（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断；取值 1 ← 诊断
