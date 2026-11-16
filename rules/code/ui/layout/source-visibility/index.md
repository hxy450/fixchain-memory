# 源端控件的显隐：XML 初值和代码里的 setVisibility

agent 会看到什么：读到布局 XML 里的 android:visibility="gone" / "invisible"，或 Activity、Fragment、Adapter 里按状态、开关、渠道调的 setVisibility(View.GONE / VISIBLE / INVISIBLE)；产物里对应组件的 if 条件、.visibility(...)，或被无条件渲染、被删掉

## 通用查法

### 源控件带 visibility 属性或被 setVisibility 时，先读初值和全部分支再写显隐

审的是：代码
触发（任一种）：
- 读到：布局 XML 里 android:visibility="gone" / "invisible"，或 Activity、Fragment、Adapter 代码里 setVisibility(View.GONE / View.VISIBLE / View.INVISIBLE)；写错的样子：目标无条件渲染、整块删掉，或几个控件包进一个共同 if；没按源端初值和各个条件写 if / .visibility(...)
适用范围：安卓控件的显隐迁成 ArkUI 的条件渲染或 visibility 属性时
做法：
- 从源布局 XML 取控件的 android:visibility 初值，再在 Activity / Fragment / Adapter 源码里按它自身的 id 搜全部 setVisibility 调用，记下每处的条件
- 从不置为可见的 gone 控件不渲染；有条件的逐个控件照条件写：View.GONE 写 if 不渲染或 .visibility(Visibility.None)，View.INVISIBLE 写 .visibility(Visibility.Hidden) 保留占位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- visibility：visible = 0，invisible = 1（不显示但占位），gone = 2（完全隐藏，如同没加这个 View）：源端三个取值（出处：Android SDK 平台资源 data/res/values/attrs.xml，visibility（按应用的 compileSdk 取对应平台））
- visibility(value: Visibility): T：目标的可见性属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.visibility）
- Visibility.None：隐藏且不参与布局、不占位；Visibility.Hidden：隐藏但占位：gone 对应 None，invisible 对应 Hidden（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
针对本应用要查的：
- 控件的显隐初值和每个改变它的条件：源工程 res/layout 下布局 XML 里这个控件的 android:visibility；Activity、Fragment、Adapter 绑定方法里对它 id（R.id.… 或 binding 字段）的 setVisibility 调用；逐处读出 setVisibility 的参数和外面的 if 条件，原样搬成目标端 if 的条件或 .visibility 三元表达式的条件；同一行里几个控件条件不同的，各写各的
来源：2 张卡，2 个应用
- case-55bbad53c11b2d1b95e6（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-be590c45de6e4195a7aa（实时公交）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-28cbc623af25｜源 View 是 android:visibility="gone" 且代码没设为 VISIBLE 时，目标不渲染它｜读到：布局 XML 里某个容器带 android:visibility="gone"，代码只改它子控件的 setText(...) / setVisibility(...)，没有对容器自身的 id 调 setVisibility(View.VISIBLE)；写错：目标 build() 里无条件渲染这个容器，和别处同语义的标题、删除入口重复
- rule-2e37d1258b95｜源 XML 里 visibility="gone" 的节点不无条件渲染，与规格快照冲突时以源 XML 为准｜读到：源布局里 TextView 等控件写 android:visibility="gone"，页面规格的快照却把它的文字列为可见文本；写错：鸿蒙页 build 里无条件画出这个节点（如一个总在显示的标题 Text）
- rule-ddd465514597｜源 XML 容器 visibility=invisible 且带 margin 时，目标在所有状态下都保留这块占位｜读到：源布局里容器写 `android:visibility="invisible"`，并带 `android:layout_marginTop` 一类的边距（如广告位）；写错：目标组件只在加载成功、失败等部分状态的 `if` 分支里渲染这个容器，默认态什么都不渲染，边距留白丢失
- rule-561757db23ee｜源容器 GONE 而内部组件常驻并自报可见性时，目标常建该组件，不用 if 或 Visibility.None 包住｜读到：布局里容器 android:visibility="gone"，但 onCreate 无条件用 FragmentTransaction.replace 把 Fragment 挂进去，由这个 Fragment 自己回调宿主切换容器 VISIBLE / GONE；写错：目标把这个组件放进 if(…) 条件分支或 .visibility(Visibility.None) 下，而把可见状态置 true 的正是它自己（aboutToAppear 里经 @Event 上抛）
- rule-3ffe7967b80d｜源端按状态切换控件显隐时，目标照分支隐藏和显示对应区块，不以换文字替代｜读到：源 Fragment 按登录等状态切换可见性：某个文字控件 `View.GONE`、另一块区域 `View.VISIBLE`，原来的 `setText` 赋值被注释掉；写错：目标只改了 `Text(...)` 的内容（如登录时显示昵称、否则显示「未登录」），该状态下没有隐藏那个控件，也没有渲染应显示的区块
- rule-4f7943e1a3dc｜源码按配置开关隐藏可选区块时，目标显隐沿用同一开关，不用列表非空推断｜读到：Fragment 源码里由远端配置对象的布尔开关方法决定收益、签到、任务这类可选区块是否显示；写错：目标把显隐开关写成几个接口列表任一非空（`.length > 0 || …`），源端开关关闭时这些区块在有数据时也露出来
- rule-0a6af7108f6c｜截图里缺、源码布局仍有的入口，先查可见性分支，是渠道或开关变体就保留｜读到：源 Fragment / Activity 里对这些 tab、入口或区块按渠道（`getChannel()`）、会员或开关分支调用 `setVisibility(View.GONE)`；布局 XML 里它们仍有定义，代码里有点击逻辑；写错：截图对照修复时，目标端把截图里没出现的 tab、入口、详情按钮或整块区域从 `build()` 里删掉，或把对应子组件的调用移除
- rule-cad34ae4ed25｜展示条件和展示列表照源端：按源端字段决定显示与否，不自行往列表里插当前用户｜读到：源端详情页对源数据的成员列表用 `for` 循环原样逐个构造头像，并按规则字段决定某一行（如重复结束）是否显示、无结束日期时写固定文案；写错：目标端在成员列表缺当前用户时 .unshift(当前用户)，或把某行的显示条件改成另一个字段非空（如只在结束日期非空时显示）
- rule-9924fcf5a269｜源 Adapter 按条件显隐的子卡，目标都要建出，显示条件照源端写｜读到：Adapter 绑定方法里按条件设子布局的 visibility（View.VISIBLE / View.GONE），控制一块附属子卡显不显示；写错：目标区块里没有这块子卡对应的组件，也没有对应的 if 条件或 .visibility(...)；或者删掉了旧骨架里的入口，却没用等价组件替换
- rule-824adb669c70｜ViewHolder.bind 对子控件分别 setVisibility 时逐个照搬条件，不包进一个共同条件｜读到：ViewHolder.bind 里同一行的几个子控件各自 setVisibility(…)，条件不同；写错：目标把整行包进一个 if (…) { Row() {…} }，该单独显示的控件也跟着隐藏
- rule-da9ad85e3026｜检查器报 binding-dropped 时补真实的显隐分支和控件，不加同名包装函数凑匹配｜读到：绑定/显隐检查器报源端控件 `binding-dropped`；写错：只新增一个与检查器驱动名同名的包装函数，或收窄绑定清单让 `binding-dropped` 消失，对应的控件和显隐分支仍不存在
- rule-97632bc538ed｜源端有偏好标记控制的首次引导图时，浮层实现引导和标记读写，或在交接中列为差异｜读到：源码里引导 ImageView 只在偏好标记为真时 VISIBLE、点击隐藏，显示后随即写回标记；布局为 match_parent 加 android:scaleType="fitXY"；写错：浮层组件里没有引导用的 Image 和首次状态的 @Param，偏好类没有引导标记的读写，交接报告也没列这项差异
- rule-70fb95cb98b0｜源控件是 INVISIBLE 时，目标用 Visibility.Hidden 保留节点，不写条件渲染｜读到：布局 XML 里控件写 `android:visibility="invisible"`；写错：目标写成 `if (this.text !== '')` 一类的条件渲染，空时整个节点不出，注释还写「源 XML visibility=invisible」
- rule-c74bd532a8df｜规格规定按钮随某状态出现或隐藏时，状态层暴露该状态标志并在回调里置位刷新｜读到：规格的 AC 条目写「某状态且某计数归零 → 按钮出现」「退出该状态 → 隐藏」；写错：会话状态里只加了计数字段，没有这个状态的标志；进入状态的回调不置位、不刷新布局，build() 里没有按两个条件显示按钮的分支
