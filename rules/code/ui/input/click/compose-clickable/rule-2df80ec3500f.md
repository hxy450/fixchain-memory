# 新建页内对话框的可见性状态时，每个状态都要有置 true 的触发点或登记 FWD-REF

审的是：代码
触发（任一种）：
- 读到：规格导航关系表里有「卡片 → 对话框」这类触发行；源端 Compose 在状态为真时渲染对话框，触发组件带 Modifier.clickable(onClick = onClick)；写错的样子：页面声明了 @Local 可见性状态和 @Builder overlay，全文件只在关闭时置 false，没有任何 = true 赋值，触发点也没登记 FWD-REF
- 读到：接线派工只要求解除 resolve_by 指向本切片的 FWD-REF 清单；写错的样子：导航关系表里的某个触发在代码里既没有 onClick，也没有对应的 P-ID
适用范围：把源页面的可点击组件和它打开的页内对话框转成 ArkUI 触发器与可见性状态，以及之后的页内接线
做法：
- 按导航关系表「触发 → 对话框」逐行确认对应组件有 .onClick(() => { 把该可见性状态置为 true })；处理器属于后续切片的，在触发点登记 FWD-REF，不能只建状态和 overlay
- 接线阶段不只解除 FWD-REF 清单，也对照导航关系表查所有触发器，没有 P-ID 的遗漏入口补上接线或回报
- 输出前逐个搜 @Local 对话框可见性状态有没有 = true 的赋值；没有就说明对话框不可达，报告里不能写成已完整实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onClick(event: (event: ClickEvent) => void): T：组件的点击事件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
- 在卡片根容器追加 .onClick(() => { 可见性状态 = true }) 后，对话框可达，对应 UI 验收通过：修好的写法（出处：卡里修好并验证过）
未核实：卡里的行为出自鸿蒙 SDK API 22，核对签名用的是本机 API 23
来源：1 张卡，1 个应用
- case-50cc2b614e68dc07e36c（CleanSweep）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 3、诊断；取值 2 ← 诊断
