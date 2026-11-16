# 行组件内层 onClick 调空默认 @Event、外层 ListItem 也挂 onClick 时，点击只留一个归属

审的是：代码
触发（任一种）：
- 读到：安卓 PreferenceScreen 里整行可点的 Preference、ListPreference 或子屏入口，规格要求点整行触发行动作（弹层、压栈、分支处理）；写错的样子：@ComponentV2 行组件里声明了带默认空实现的 @Event 回调（= () => {}），组件内层 Row 的 .onClick 调用它；调用处不传这个事件，真实动作挂在外层 ListItem().onClick 上
适用范围：把整行可点的设置项迁成 List / ListItem 里的可复用自定义行组件、行动作由父页面提供时
做法：
- 点击只给一个归属，二选一：行组件声明 @Event 并在组件内 .onClick 里调用，每个调用点都传入动作；或者行组件内部不挂 .onClick，由外层 ListItem().onClick 处理。不要内外两层同时挂 .onClick
- @Event 带默认空实现、组件内 .onClick 会调用它的，逐个检查调用点有没有传这个事件；没传却在外层挂了 .onClick 的，删掉行组件里的 @Event 和内层 .onClick（或改成调用点传入）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 删掉行组件的 @Event 和内层 .onClick 后，外层 ListItem 的 .onClick 动作生效：内层空回调吞掉点击的修法（出处：卡里修好并验证过）
- 当父子组件均绑定同一类手势时，子组件优先于父组件触发：内层 .onClick 会抢走点击，外层 ListItem 的 .onClick 不再触发（出处：arkts-gesture-events-multi-level-gesture.md，手势与事件）
- 除了 onTouch 以外的手势与事件都由基础手势或组合手势实现：onClick 也按手势竞争，不是 DOM 冒泡（出处：arkts-gesture-events-multi-level-gesture.md，手势与事件）
- @Event 没有初始化时自动生成一个空函数作为默认回调；未被外部初始化但本地有默认值时用本地默认函数：调用点不传事件时，组件内 .onClick 调到的是空函数，点击被吞而不报错（出处：arkts-new-event.md，@Event 的使用规则）
- onClick(event: (event: ClickEvent) => void): T：组件通用的点击事件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
未核实：卡里上机所用 SDK 是 API 24（6.1.1），声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-f6ac0fc6805f2fc8ff14（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断
