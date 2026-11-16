# ForEach 的键里拼了请求序号、加载状态等易变字段时，键只用数据的查询键

审的是：代码
触发（任一种）：
- 写错的样子：ForEach(arr, itemGenerator, keyGenerator) 的 keyGenerator 返回值里拼了请求序号、加载状态、事件列表这类每次请求都会变的字段，翻页或切换时页面反复销毁重建、抖动
适用范围：ArkUI 用 ForEach 生成翻页页面或列表项、数据由异步查询填充时的 keyGenerator
做法：
- keyGenerator 只返回标识这一项数据身份的查询键（例如由模式和日期范围拼成的查询键），不拼请求序号、加载状态和查询结果内容
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的调用签名，第三个参数是键值生成函数（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 键值变化时，框架视为该数组元素已被替换，按新键值创建新组件：键里任何字段一变，这一项的组件就销毁重建（出处：arkts-rendering-control-foreach.md，键值生成规则）
- 键值生成函数里用与 UI 相关的数据属性；对象数据用唯一 id 作键：键只放数据身份，不放过程状态（出处：arkts-rendering-control-foreach.md，键值生成规则、使用建议）
- 键只用查询键后，翻页时页面不再反复销毁重建：修好后的行为（出处：卡里修好并验证过）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的调用签名，键值规则相同（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
- key(keyGenerator: (item: T, index: number) => string): RepeatAttribute<T>：同族接口：Repeat 的键值生成（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.key）
来源：1 张卡，1 个应用
- case-e5d42507c82fd492f62b（记得日历）：做法第 1 步 ← 诊断；取值 4 ← 诊断
