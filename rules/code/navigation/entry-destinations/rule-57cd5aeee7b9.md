# 自绘弹层替代源端 SDK 弹窗时，源配置里的每个回调都映射到 onClick 和路由

审的是：代码
触发（任一种）：
- 读到：源端启动页给第三方隐私弹窗配置对象注册了多个回调：服务协议链接、隐私政策链接各自 startActivity 打开 WebView 页，另有同意、拒绝回调；写错的样子：自绘弹层里协议文字只是 Text(...).fontColor(...) 或 .fontWeight(...)，没有 .onClick，也没有 `FWD-REF` 占位；只有取消、确定接了回调
适用范围：用页面内自绘弹层替代源端 SDK 提供的隐私、协议弹窗时的交互接线
做法：
- 先列出源配置里的全部回调，逐一映射到目标控件：协议文字写 .onClick(() => this.navPathStack.pushPathByName('<WebView 页的路由名>', <带 url 的参数>))，同意、拒绝接各自的处理；写完逐条核对每个回调都有绑定
- WebView 页已存在、URL 提供者归后续切片时，仍给协议文字绑定 onClick，在处理里留指向负责切片的 `FWD-REF` 占位；不把可点击链接降级成只改字色的静态 Text
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onClick(event: (event: ClickEvent) => void): T：组件通用的点击事件，Text 上同样可用（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
- pushPathByName(name: string, param: unknown, animated?: boolean): void：按路由名压入目标页，param 里带 url（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- 两条协议文字补点击，URL 经校验后 pushPathByName 到 WebView 页，复检由 missing 变 matched：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源配置里有哪些回调、各自打开什么：源工程启动页 Activity 里构造隐私弹窗配置的那段代码；把配置对象上每个回调属性和它里面 startActivity 的目标、取 URL 的方法逐条抄下来，对到目标弹层的控件
来源：1 张卡，1 个应用
- case-1f107c5992d58b6efb4a（实时公交）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 3 ← 诊断
