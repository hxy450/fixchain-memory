# 源布局写定的尺寸、字号和颜色

agent 会看到什么：读到源布局（含 <include> 的布局、RecyclerView 的 item 布局）里控件的 layout_height、margin、padding、textSize、textColor、background 或 @dimen/、@color/ 引用，交回的代码给组件写了 .height、.margin、.fontSize、.fontColor 等常数，或视觉修复改了这些数

## 通用查法

### 目标的尺寸、字号、颜色是手写常数时，逐项回源布局读出有效值再写

审的是：代码
触发（任一种）：
- 读到：源布局 XML（含 <include> 的布局、Adapter 的 item 布局）给控件写了 android:layout_height、android:layout_margin、android:textSize、android:textColor、android:background，或引用 @dimen/、@color/、style；写错的样子：目标的 .height(...)、.margin(...)、.fontSize(...)、.fontColor(...)、.backgroundColor(...) 是照相似行、style 默认值、资源名字或截图比例定的常数，和源布局对不上
适用范围：迁源布局的视觉属性，或视觉修复改这些数值时
做法：
- 按控件 id 在源布局及它 include 的布局里读这项属性；控件自身写的值优先于它的 style，引用 @dimen/、@color/ 的到 res/values*/ 按名取值
- 目标写成同一数值：dp 写成 vp，sp 数值写成 number（单位 fp）；用 $r('app.float.…') 时先读目标 float.json 里的 value，只引用数值相同的那项
- 源布局没读全（回执带 truncated 警告）的先补读再写；源端和目标已经一致的数值不改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 属性取值的先后：AttributeSet 里控件自身写的值 → 它的 style → defStyleAttr / defStyleRes → 主题：控件上写的属性覆盖 style 里的（出处：android.content.res.Resources.Theme#obtainStyledAttributes）
- fontSize(value: number | string | Resource): TextAttribute；number 的单位是 fp：源端 sp 数值直接写成 number（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontSize）
- float 资源写在 element/float.json，每项 {"name": …, "value": "28.0fp"}，value 带单位：命名资源的实际数值只在 value 里，名字不代表数值（出处：resource-categories-and-access.md，资源文件示例）
针对本应用要查的：
- 控件这一项视觉属性的有效值：源工程 res/layout 下的页面布局、它 <include> 的布局和 Adapter 用的 item 布局 XML，按控件 id 找；引用的 @dimen/、@color/ 到 res/values*/ 的 dimens.xml、colors.xml 按 name 找，style 到 styles.xml；控件自身写的值优先，没有再看 style；读出数值和单位，dp 记成 vp、sp 记成 fp
- 目标命名资源的实际数值：目标工程 resources/base/element/float.json（及限定词目录下的同名文件），按 name 找；读 value 的数值和单位，和源端的数值比较
来源：4 张卡，4 个应用
- case-0389a44b7fd28f48c094（记得日历）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2
- case-639b36918b1cd5c1bbe8（android-train-ticket-vest7）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-85baa9234cc4f4798784（AntennaPod）：做法第 2 步 ← 建议 1
- case-d64f11b7100c739bb292（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2；做法第 3 步 ← 建议 1

## 规矩

- rule-964096c22b46｜页面视觉样式逐项取自源布局和 include 布局，读到的回执被截断时补读后再写｜读到：页面规格只给源布局清单和合成的 view.xml（只有类名、id、文本，没有 `android:background`、`android:textColor`、`android:textSize`），样式在 `<include layout="@layout/…">` 的各个布局里；写错：组件的 `.backgroundColor(...)`、`.fontColor(...)`、`.fontSize(...)` 是通用白底卡片或自拟配色，在源布局里找不到对应的属性值
- rule-6e32e9dbf74f｜列表单元格按 RecyclerView item 布局逐项落尺寸和角标，不用自绘圆或文字色块替代｜读到：`RecyclerView` 的 item 布局 XML 写了 `layout_height`、`layout_margin`、各 `TextView` 的 `android:textSize`，以及做今日、状态角标的 `ImageView`；写错：目标单元格的高度、边距、字号与 item 布局不一致；选中或今日用 `Circle()` 自绘，状态角标用文字色块，没有对应的 `Image`
- rule-88ab0a270dec｜实现列表或输入行时，按源 item XML 逐项取尺寸和可选入口，不照搬工程里的相似行｜读到：源 item XML 写了 android:layout_height、android:layout_marginBottom、paddingStart、圆角背景、android:textSize，另有默认 android:visibility="gone"、由数据决定是否显示的可选入口；写错：目标行照搬工程里已有相似行的 .height / .margin({ top }) / .borderRadius / .padding / .fontSize，和 item XML 不一致，或没有按数据显示可选入口
- rule-af2fef42038b｜共享组件表的行指向安卓 item 布局时，组件按该布局逐项还原，缺材料就不生成｜读到：共享组件表的行写着安卓来源：某个 Adapter 类及其 item 布局（layout/item_*.xml），或页面规格里的 UI 锚点；写错：公共组件里的行组件只是 Row/Column 套几段 Text，字号、颜色、内边距是自拟的固定值，缺 item 布局里的容器尺寸、背景图、标签文字、复制或编辑删除这类图标按钮
- rule-ed15ff4b06d8｜控件自身写了 textSize 时覆盖 style 默认值，目标逐控件取有效字号，不用 style 值统一代替｜读到：按钮用 style 给默认 android:textSize，单个控件上又写了自己的 android:textSize（不同按键各不相同）；写错：目标按键统一写 .fontSize(<style 默认值>)，丢了逐键的覆盖值
- rule-fd81dc307be5｜用命名尺寸资源承载源端 sp 值时，先读资源实际值再选名，注释与资源一致｜读到：源布局写了具体字号 android:textSize="12sp"，或由主题、textAppearance 推出行标题字号（如 16sp）；写错：代码用 fontSize($r('app.float.…')) 这类按名字挑的资源，注释写的 sp 数和该资源在 float.json 里的 value 不一样
- rule-389defb8569c｜视觉修复改尺寸前先读源布局取值，已一致就不改，偏离要有源码或资源依据｜读到：视觉差异单只有文字结论（如「行高更大」「下方内容被下推」），源布局里对应尺寸是 android:layout_height 等属性引用的 @dimen/ 值；写错：目标尺寸被改成和源端 @dimen/ 取值不同的数值，尝试记录里没有引用源端取值
- rule-f862675d8dd8｜读 include 或 item 布局前先确认源码所在的 flavor/源集，不取递归搜索的第一个结果｜读到：源工程有多个 productFlavors 或源集（`src/main` 和各 flavor 目录），同名布局在几个源集里各有一份；Fragment / Adapter 用 `<include layout="@layout/…">` 或按名字引用；写错：目标照另一 flavor 的同名布局实现，`width` / `height` 和装饰线与源码所在源集的那份不一致
- rule-10c2fdd86fc1｜根布局高度是固定 dimen 时用 height()，不写成 constraintSize minHeight｜读到：源布局根节点 `android:layout_height="@dimen/…"`（具体尺寸，不是 `wrap_content`）；写错：目标根节点写 `.constraintSize({ minHeight: ... })`，内容多时会被撑高
