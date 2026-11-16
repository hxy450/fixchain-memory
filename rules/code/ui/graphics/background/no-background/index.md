# 没写背景或背景为 @null 的控件

agent 会看到什么：读到源控件和它的父容器没写 android:background，或写了 android:background="@null"；产物里对应组件多了 .backgroundColor(...)、.border(...)，或留着组件默认的 padding

## 通用查法

### 源控件没写背景或写 @null 时，顺父容器和主题查出透出的底色，目标这一层不垫色

审的是：代码
触发（任一种）：
- 读到：源控件和它的父容器没写 android:background，或写了 android:background="@null"（RecyclerView、FrameLayout、EditText、SurfaceView 等）；写错的样子：目标对应组件上多了源端没有的 .backgroundColor(...)，或沿用组件默认的 padding，盖住下层、底色或内边距和源端不一致
适用范围：安卓控件没有自己的背景（未写或 @null），迁成 ArkUI 组件时
做法：
- 顺着父容器往上找第一个有 android:background 的那层；到布局根都没有，页面底色按 Activity 主题的 windowBackground 写
- 目标对应这一层不设背景或设 .backgroundColor(Color.Transparent)，底色只写在源端有背景的那一层；@null 去掉的还有背景带来的内边距，padding 按源端实际值四边写全
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- View 的内边距来自背景 drawable 的 getPadding；background=@null 时没有这部分内边距：源端去掉背景后，没写 padding 的边是 0（出处：android.view.View#setBackgroundDrawable）
- Stack 的子组件按顺序依次入栈，后一个子组件覆盖前一个子组件：叠在下层之上的组件设了不透明底色就会盖住下层（出处：ts-container-stack.md，页首说明）
- TextInput 默认 padding { top: 8vp, right: 16vp, bottom: 8vp, left: 16vp }：例：输入框不写 left 时起始边有 16vp 内边距（出处：ts-basic-components-textinput.md，属性说明）
针对本应用要查的：
- 透出来的底色：源工程布局 XML 里从这个控件往上各层父容器的 android:background；都没有时看 AndroidManifest.xml 里 Activity 或 application 的 android:theme，到 res/values 的主题文件里找 android:windowBackground；取到 @color/… 或 @drawable/… 再读出实际值，写在目标对应的那一层（通常是页面根容器）上；规格给的底色在源端查不到引用时登记差异
未核实：主题没写 windowBackground 时父主题里的默认值，族里的卡没查实
来源：3 张卡，3 个应用
- case-2a82c31c11fb4f1c7fa5（Blockinger）：做法第 1 步 ← 诊断
- case-5d12548f9d559985c27d（app_hnaccurateweather_live_android）：做法第 2 步 ← 建议 2
- case-85baa9234cc4f4798784（AntennaPod）：做法第 2 步 ← 建议 6

## 规矩

- rule-7b168aeccc07｜源 RecyclerView 无背景叠在头图上时，目标滚动内容层保持透明，只给卡片设背景｜读到：布局里头图 ImageView 在下层，SwipeRefreshLayout / RecyclerView 和根容器都没有 android:background，叠在头图之上；写错：Stack 里位于头图 Image 之上的全高 List（height('100%')）设了不透明 .backgroundColor(...)，头图被完全遮住
- rule-a42243423dff｜规格给的底色和源布局冲突时先回源核对引用，不能确认就登记差异，不照写颜色键｜读到：源布局根没有 android:background、SurfaceView 为 android:background="@null"，规格却写某个颜色「透出」；写错：页面根写 .backgroundColor($r('app.color.…')) 用规格里的颜色键，注释写这个颜色 shows through
- rule-07cb9591a4fb｜无来源兜底预览不加源端没有的描边，未选择时所有预览分支都不画边框｜读到：源端预览容器是 wrap_content 的空 FrameLayout，没有 stroke 或背景；编辑状态里选中的边框默认为 null，边框只在选择后由 Drawable 绘制；写错：无预览源分支把 Blank() 换成带 .border({ width: …, color: … }) 的占位
- rule-76f210561ab8｜EditText 去掉背景、起始无内边距时，TextInput 的 padding 显式写 left: 0｜读到：EditText 写了 android:background="@null"，起始边没有 paddingStart，文字贴边；写错：TextInput 的 .padding({...}) 只写了 top、bottom、right，没写 left，起始边仍有默认内边距
