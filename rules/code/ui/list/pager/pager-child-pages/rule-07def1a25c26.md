# @Builder 槽位要显示异步加载或 @Trace 会变的数据时，不作位置值参，槽体内直读 this 上的状态

审的是：代码
触发（任一种）：
- 读到：源端宿主 Fragment 用 Tab / ViewPager 嵌子 Fragment，子 Fragment 显示异步加载的列表和选中位置；写错的样子：@Builder 槽位声明成多个位置值参（数组、选中索引、回调），调用处传入 @ObservedV2 / @Trace 状态对象上的属性值（如 this.state.list、this.state.selectedIndex）；槽体只有 FWD-REF 占位时也是这个签名
适用范围：@ComponentV2 页面里用 @Builder 槽位嵌入子组件，包括槽体只有 FWD-REF 占位的空槽和后续填充槽体时
做法：
- 槽位写成无参 @Builder，在槽体内直接读 this 上的被观测状态（如 this.state.list、this.state.selectedIndex），调用处无参调用；只有静态值和回调适合作参数
- 或把数据交给子组件，子组件用 @Param 接入；后续填充槽体时不沿用占位签名，先确认异步更新后槽内能刷新
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 调用 @Builder 装饰的函数默认按值传递，参数为状态变量时，状态变量的改变不会引起 @Builder 函数内的 UI 刷新：取出的属性值作参数，只定格调用时刻的快照（出处：arkts-builder.md，按值传递参数）
- @Builder 传入两个或两个以上参数且未用按回调传递时，不会触发动态渲染 UI：多参数槽位不随数据更新（出处：arkts-builder.md，限制条件）
- 无参槽位、槽体直读 this 上的状态后，分类异步到达时 Tab 正常显示：修好的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a927e303e0cae68a913a（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 3；取值 3 ← 诊断
