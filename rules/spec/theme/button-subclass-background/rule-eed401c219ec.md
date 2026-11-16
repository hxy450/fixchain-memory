# 禁用外观只靠换背景且字色固定时，规格写换背景加拦截点击，不用 .enabled(false)

审的是：规格
触发（任一种）：
- 读到：源码先 setBackgroundResource(R.drawable.…) 换成灰底再 setEnabled(false)（或布局 android:enabled="false"），背景 drawable 的 <selector> 没有 android:state_enabled 分支，android:textColor 是固定颜色而非 ColorStateList；写错的样子：规格的转换决策写「.enabled(…) + 背景切换」「enabled(false) 同时拦截点击」，没提 ArkUI 禁用态会对整个组件降透明，也没给禁用态的取色判据
适用范围：规格提取阶段，为运行时 setEnabled 切换或 android:enabled 的控件写 ArkUI 转换决策时
做法：
- 写决策前先查禁用外观的来源：背景 drawable 和 textColor 有没有 state_enabled 分支，按钮 style 的 stateListAnimator
- 禁用外观只由代码显式换背景决定、字色固定时，规格写「禁用 = 换背景 + 不响应点击（hitTestBehavior(HitTestMode.None) 或点击回调内判态）；不用 .enabled(false)：ArkUI 禁用态会整体降透明」，并给判据「禁用态取色等于源背景色值（不透明）、文字为源端固定字色」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 组件 .enabled(false) 时背景和文字整体约 40% 透明：和源端不透明灰底的禁用外观冲突（出处：卡里修好并验证过）
- Widget.Material.Button 的 stateListAnimator = @anim/button_state_list_anim_material，未启用时 elevation、translationZ 都是 0：源端按钮禁用时投影归零（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.Button；data/res/anim/button_state_list_anim_material.xml（按应用的 compileSdk 取对应平台））
- Base.Widget.AppCompat.Button 的 parent 是 android:Widget.Material.Button：AppCompat 按钮在 API 21 以上沿用平台的 stateListAnimator（出处：androidx.appcompat:appcompat 包内 res/values-v21/values-v21.xml，Base.Widget.AppCompat.Button（按应用依赖的版本））
针对本应用要查的：
- 源端禁用外观来自哪里：源工程 res/drawable*/ 下按钮背景 drawable 的 <selector> 有没有 android:state_enabled="false" 的 <item>；res/color*/ 下 textColor 引用的是不是 <selector>；按钮 style 或主题里的 stateListAnimator；有 state_enabled 分支的，取分支里的颜色值显式写进规格；没有的，禁用态就是代码里换上的那个背景加固定字色
来源：1 张卡，1 个应用
- case-787e380c801fb46d89a7（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断
