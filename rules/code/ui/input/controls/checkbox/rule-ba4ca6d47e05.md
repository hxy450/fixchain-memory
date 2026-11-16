# 共享组件承载多个弹窗变体时，每个变体照自己的布局还原勾选等子控件

审的是：代码
触发（任一种）：
- 读到：几个弹窗变体（普通、严格等）各有一份布局 XML，没有显式勾选状态的变体布局里也有 CheckBox（checked=true）；写错的样子：共享组件里只有带显式勾选状态的变体分支有 Checkbox，其余变体分支没有勾选控件
- 读到：点击回调里先 setChecked(true, true) 让勾选播放动画，再 postDelayed(…, 700) 执行后续；写错的样子：目标保留了 setTimeout(…, 700)，但没有它依附的 Checkbox 和勾选动作
适用范围：一个共享组件用分支承载多个源端弹窗变体，或迁移时保留了依附于视觉元素的延时时
做法：
- 每个变体分别打开自己的布局文件对照；布局里有勾选控件的变体就写 Checkbox().select(<checked 初值>)（或同尺寸的勾选图标），不按别的变体有没有显式勾选状态推断
- 保留延时时把它依附的视觉一起还原：点击先把勾选置为选中，再 setTimeout(<源端延时>) 执行回调
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (options?: CheckboxOptions): CheckboxAttribute：Checkbox 的构造（出处：鸿蒙 SDK 的 ets/component/checkbox.d.ts，CheckboxInterface）
- select(value: boolean): CheckboxAttribute：设置是否选中，对应源端 checked 初值和 setChecked（出处：鸿蒙 SDK 的 ets/component/checkbox.d.ts，CheckboxAttribute.select）
- 普通变体补上勾选和两行文案，严格变体保留原「同意」加勾选校验：修好后各变体各照自己的布局（出处：卡里修好并验证过）
针对本应用要查的：
- 每个变体对应哪份布局：源工程里弹出这些弹窗的代码（按变体分支 inflate 或 setContentView 的布局资源），以及规格里的变体目录；一个变体对一份布局，逐份读出勾选控件、文案行数和字号
来源：1 张卡，1 个应用
- case-a3404675917f8a352eb9（话费流量查询助手）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
