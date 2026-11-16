# LazyColumn 无 key 的项按位置标识，目标常驻组件要按位置相关键重建或保存后复位

审的是：代码
触发（任一种）：
- 读到：LazyColumn / LazyList 里无 key 的 `item { }`（如列表尾部的新增卡），内部状态只 remember(…)，保存回调不自清；写错的样子：目标把它放进常驻的条件 ListItem，状态只在 aboutToAppear 初始化，保存后只追加不复位，上一条输入留在卡里
适用范围：把 Compose 惰性列表的项迁成 ArkUI List + ForEach / Repeat 时
做法：
- 逐项核对源端有无 key：无 key 的项位置一变 remember 状态就丢；目标用位置相关键重建，如 ForEach([this.steps.length], () => { … }, (n: number) => `${n}`)，或保存后显式复位输入状态
- 推断出「源保存后仍保留旧输入」这类反常行为时，先回查框架的身份语义再定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的签名（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 键值变化时框架视为数组项已被替换，按新键值创建新组件：用随步数变化的键可让尾卡重建、状态复位（出处：arkts-rendering-control-foreach.md，键值生成规则）
- 尾卡改为 ForEach([steps.length]) 按步数为键重建后，保存一条后尾卡回到空白：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-36f0b5f441f81e98f6c6（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 3 ← 诊断
