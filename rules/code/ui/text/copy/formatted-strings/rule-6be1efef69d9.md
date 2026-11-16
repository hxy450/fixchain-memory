# 克隆回调取编辑草稿和重排后的子项，名称用带占位符的字符串资源格式化原名

审的是：代码
触发（任一种）：
- 读到：源端克隆：copy(id = 0, name = getString(R.string.…, 原名))，子项 mapIndexed 重排并清 id；确认克隆时传入草稿的 name、description 等字段；写错的样子：目标 clone(id) 按 id 读已持久化的记录，以 { ...record, id: 0 } 原名插入，没有后缀，也丢了未保存的编辑
适用范围：编辑页的克隆回调迁到目标端数据层和接线时
做法：
- 克隆入参改成编辑草稿的字段和当前顺序的子项；插入时主记录 id = 0，子项 id = 0、序号 = 下标
- 名称仍取持久化原名，用源端同一个带占位符的字符串资源格式化（迁到 string.json 时保留 %1$s），不用草稿名、不省略后缀
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringSync(resId: number, ...args: Array<string | number>): string：非 UI 代码里取格式化字符串，args 依次替换占位符（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- $r('app.string.label', 'aaa', 444)：UI 里取带 %1$s、%2$d 占位符的字符串资源，后面的参数依次替换（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
- public final String getString(@StringRes int resId, Object... formatArgs)：源端 getString 的第二个起的参数是格式化参数，对应目标 args（出处：android.content.Context#getString）
- getStringByNameSync(resName: string, ...args: Array<string | number>): string：同族接口：按资源名取格式化字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringByNameSync）
- 克隆用草稿字段和有序子项（id = 0、序号 = 下标）插入，名称按持久化名加后缀：两轮判别后的修复（出处：卡里修好并验证过）
针对本应用要查的：
- 克隆名用的字符串资源和它的占位符：源工程 res/values*/strings.xml 里，克隆回调 getString 引用的那个 name；把各语言的 value 照搬到目标 resources/<限定词>/element/string.json 的同名条目，保留 %1$s
未核实：卡里的环境是 HarmonyOS 6.0.1(21)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-ef4b9ae3acaea9323135（Cofi）：做法第 1 步 ← 诊断、建议 2；做法第 2 步 ← 诊断、建议 2；取值 5 ← 诊断
