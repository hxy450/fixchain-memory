# 数据源只是对本地静态集合做 shuffled/filter/sort 时，在组件初始化处直接复现，不登记前向占位

审的是：代码
触发（任一种）：
- 读到：源端 ViewModel 的数据源方法只是对本地静态种子做 shuffled() / filter / sort（如 exampleLists.shuffled().toMutableList()）；写错的样子：目标把种子照录成固定顺序的常量数组，写一个 `FWD-REF` 标记，理由是「ViewModel 等价体未建」
适用范围：页面 UI 转换阶段迁移列表数据源，而对应 ViewModel 的鸿蒙等价体还没建时
不适用的情形：数据源依赖网络、跨页状态等本切片确实拿不到的工件时才延后
做法：
- 在组件 aboutToAppear 里对种子副本复现同样的变换：shuffled() 写成对副本做 Fisher-Yates 洗牌后赋给列表状态，filter / sort 用数组的 filter / sort；不登记前向占位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- aboutToAppear?(): void：自定义组件创建后、build() 执行前调用，可在这里改状态变量，下一次 build 生效（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToAppear）
- 模块级 Fisher-Yates 洗牌函数，aboutToAppear 里洗牌种子副本后注入列表：修好后每次进入顺序随机，与源端 shuffled() 一致（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-77e4e8b4e16c3fc8e030（DeepAI全能PPT）：做法第 1 步 ← 建议 2、诊断；例外 1 ← 建议 2；取值 2 ← 诊断
