# 数据绑定布局里的点击绑定

agent 会看到什么：读到 <layout><data><variable> 的数据绑定布局，控件上写 android:onClick="@{…}" 或按 ViewModel 状态切换 android:src，交回的代码在对应组件上写了（或没写）.onClick

## 通用查法

### 布局里 android:onClick="@{…}" 的点击，顺着绑定找到处理方法后照它写 .onClick

审的是：代码
触发（任一种）：
- 读到：布局 XML 是 <layout><data><variable type="…"> 的数据绑定布局，控件上写 android:onClick="@{…::…}"，或 android:src 按 ViewModel 状态切换；写错的样子：目标对应组件没有 .onClick，或 .onClick 里只切状态换图，少了处理方法里的跳转和副作用
适用范围：把数据绑定布局里的点击绑定迁成 ArkUI 组件的事件逻辑时
做法：
- 先核对绑定指向的类：<data> 里 <variable> 的 type 包名、规格里的页面类全名、页面类 import 的绑定类包名应属同一个模块；不一致就回报规格缺陷，改按页面类所在模块的布局核对
- 按 @{…::方法名} 的方法名和控件 id，在那个类和 ViewModel 里找方法定义与 when 分支，逐项列出跳转目标和副作用（偏好写入、振动、播放、打开面板）
- 目标 .onClick 里逐项照写；跳转的目标页还没建时，在 onClick 处写已登记的 `FWD-REF`
针对本应用要查的：
- 点击绑定指向的处理方法和它做的事：源工程里 <variable> 的 type 指的 Fragment、Activity 或 ViewModel 的 Kotlin / Java 源文件，按 @{…::方法名} 里的方法名、控件 id 搜方法定义和 when 分支；逐个分支记下启动的页面、偏好读写（读取处的第二个参数就是默认值）、振动和播放调用、面板操作
- 页面类实际绑定的布局里有哪些入口：页面类所在模块 src/main/res/layout 下的同名布局 XML，按 android:onClick 或 @{…} 点击绑定搜；列出入口清单，与目标页面的可点击组件逐项对照
来源：3 张卡，2 个应用
- case-356f707ace6e648548be（android-panorama-map-vest7）：做法第 1 步 ← 建议 4
- case-a224386ed55020afec18（android-train-ticket-vest7）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-db22477c416cef2ebedd（android-panorama-map-vest7）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2

## 规矩

- rule-c375ccd65b29｜页面转换前核对布局 <data> 变量类型与规格里的页面类全名，不一致就回报规格缺陷｜读到：规格指向的布局 XML 里 <data><variable type="…"> 的类全名（包名）和规格里的 Activity/Fragment 全名不同，或源页面类用的 .databinding 绑定类不在这个布局所在的模块；写错：目标页面照另一个模块的布局写出源页面没有的入口（多出的点击行、卡片），和源页面类实际绑定的布局里的 android:onClick 点击对不上
- rule-a95e3362d655｜源布局有 android:onClick 绑定时，目标按钮接跳转或登记 FWD-REF，不按合成快照判无交互｜读到：源布局 XML 里按钮或可点击容器带 DataBinding 点击 android:onClick="@{page::onClick…}"，规格「导航关系」表列了代码触发的目标页；写错：目标写出可见的 Button(...) 却没有 .onClick，页面也没拿 NavPathStack，没写 `FWD-REF`
- rule-bb2ff3a9107a｜布局控件带 onClick 绑定或按状态选图时，onClick 要复刻处理器分支的副作用，不能只取反换图｜读到：布局 XML 里控件写 android:onClick="@{…}" 数据绑定，或 android:src 按 ViewModel 状态三元切换；实际行为写在 Fragment/Activity 统一点击处理器的 when 分支和 ViewModel 里；写错：对应 ArkUI 组件的 .onClick 里只把 @State 布尔取反并换图，没有处理器分支里的偏好写入、振动、音频播放或面板打开
