# Stack 的内容对齐用 Stack({ alignContent })，不写即居中，不用 justifyContent

审的是：代码
触发（任一种）：
- 读到：Compose `Box(contentAlignment = Alignment.Center)` 一类的居中叠放布局，迁成 ArkUI `Stack`；写错的样子：`Stack() {…}` 后面写了 `.justifyContent(FlexAlign.Center)`，编译报 Property 'justifyContent' does not exist on type 'StackAttribute'
适用范围：把叠放布局（Compose Box 等）迁成 ArkUI Stack 并设置内容对齐时
做法：
- 写成 `Stack({ alignContent: Alignment.<位置> }) { … }`，按源端 contentAlignment 的位置选 Alignment 的对应值；居中时可以不写（默认 Alignment.Center）
- 不在 Stack 上套用 Column/Row/Flex 的 `.justifyContent(...)`、`.alignItems(...)`
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (options?: StackOptions): StackAttribute：Stack 的构造，对齐写在 StackOptions 里（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackInterface）
- alignContent?: Alignment，@default Alignment.Center：子组件在容器内的对齐，不写时居中（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- alignContent(value: Alignment): FolderStackAttribute：同族接口：FolderStack 的内容对齐（出处：鸿蒙 SDK 的 ets/component/folder_stack.d.ts，FolderStackAttribute.alignContent）
- Stack 上写 justifyContent 编译报 Property 'justifyContent' does not exist on type 'StackAttribute'；删掉后按默认居中编译通过：Stack 不支持 justifyContent（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c839a6e432779939bf8b（青商城）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
