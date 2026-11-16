# 勾选控件和勾选状态

agent 会看到什么：源端 CheckBox、checkable 菜单项、实现 Checkable 的自定义 View 和它们的 setChecked / postDelayed；产物里 Checkbox 的 shape、select、onChange，MenuItem 的 selectIcon 和勾选后的延时

## 规矩

- rule-c8c69360aaf8｜标准 CheckBox 译成 Checkbox 时设成圆角方形 ROUNDED_SQUARE｜读到：布局里标准的 <CheckBox>（没写 android:button 自定义图），Material 下呈方形复选框；写错：Checkbox().select(…).selectedColor(…) 没写 .shape(…)
- rule-405b9cccbc24｜源端条目带 CheckBox 切换完成状态时，目标写 Checkbox.select 加 onChange｜读到：源端列表条目里 `CheckBox` 的 `isChecked = item.isCompleted`，点击回调调用 ViewModel 的切换方法，再由它调仓库层写入完成状态；写错：目标条目的 `@Builder` 里没有 `Checkbox`，或有 `Checkbox` 没有 `.onChange(...)`；对应 ViewModel 只有 `loadData`/`refresh`，缺切换完成状态的方法
- rule-d679f69f5a3a｜继承 View 的自定义控件上写了 android:checked 时，先核它是否被读取，初值取运行时生效值｜读到：源布局的自定义控件（extends View implements Checkable，不是 CheckBox / CompoundButton）上声明 android:checked="true"，它的构造函数和 init(attrs) 只读自己的 styleable 属性，选中字段没有初值；show 之前没有调用 setChecked；写错：目标端把首显状态写成 `@Local … : boolean = true`，注释只写「源 XML android:checked="true"」作依据
- rule-cbe1fe67e16d｜checkable 菜单项转 MenuItem 时，除 selected 外要写 selectIcon(true)｜读到：菜单 XML 的 <item> 写了 android:checkable="true"；写错：对应 MenuItem 只写了 .selected(...)，没有 .selectIcon(...)，选中时看不到勾
- rule-ba4ca6d47e05｜共享组件承载多个弹窗变体时，每个变体照自己的布局还原勾选等子控件｜读到：几个弹窗变体（普通、严格等）各有一份布局 XML，没有显式勾选状态的变体布局里也有 CheckBox（checked=true）；写错：共享组件里只有带显式勾选状态的变体分支有 Checkbox，其余变体分支没有勾选控件
- rule-c75c21404822｜同意区先 setChecked 动画再 postDelayed 回调时，目标先切选中态，再延时调同意逻辑｜读到：弹窗同意区点击里先 checkBox.setChecked(true, true) 播放勾选动画，再 checkBox.postDelayed({ 回调; dialog.dismiss() }, N)；布局里的勾选控件有 checked / unchecked 两套颜色；写错：同意按钮或同意区 .onClick(() => …) 里直接调同意逻辑并跳转，勾选控件只画了静态的未选中外观，没有延时
- rule-0afac2bcd8f6｜框架主题提供勾选图的 CheckBox，目标用平台两态图按 checked 切换，不改用 ArkUI Checkbox｜读到：源端 CheckBoxPreference 或 CheckBox 没写 android:button，应用 res 里没有勾选图，勾选图由框架主题的 listChoiceIndicatorMultiple 提供；写错：目标写成 Checkbox().shape(CheckBoxShape.ROUNDED_SQUARE).selectedColor(...) 并自定尺寸，或者给勾选图 Image 用 .fillColor() 二次着色
