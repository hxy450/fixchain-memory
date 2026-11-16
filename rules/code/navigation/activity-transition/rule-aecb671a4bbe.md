# 页面转场按源端目的地 Activity 的转场设置查实后显式写

审的是：代码
触发（任一种）：
- 读到：源端 startActivity / finish 切换的 Activity，它或基类 onCreate 里的 overridePendingTransition、主题的 windowAnimationStyle；写错的样子：目标 @Entry 页没有 pageTransition()，或 pushPathByName / replacePathByName 没写 animated，沿用鸿蒙默认转场
适用范围：源端 Activity 跳转迁成 router 的 @Entry 页或 NavPathStack 页面时
做法：
- 查目的地 Activity 及基类的 onCreate、startActivity / finish 前后有没有 overridePendingTransition(…)；没调用时转场来自主题 windowAnimationStyle
- 是 overridePendingTransition(0, 0) 的，写 pushPathByName / replacePathByName(name, param, false)；用默认动画的，在 @Entry 页写 pageTransition() 的 Push、Pop 四段，duration、curve 显式写
- 查不到目标值就作为规格缺口回报
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- PageTransitionOptions：type 默认 RouteType.None；duration 单位 ms，默认 1000；curve 默认 Curve.Linear：不写 duration 时转场是 1 秒（出处：鸿蒙 SDK 的 ets/component/page_transition.d.ts，PageTransitionOptions）
- Push：A 的 PageTransitionExit 和 B 的 PageTransitionEnter（type 为 None 或 Push）生效；Pop：B 的 Exit 和 A 的 Enter（type 为 None 或 Pop）生效：Push Enter 对 open_enter、Push Exit 对 open_exit、Pop Enter 对 close_enter、Pop Exit 对 close_exit（出处：ts-page-transition-animation.md，RouteType枚举说明）
- pushPathByName(name: string, param: unknown, animated?: boolean): void，animated 默认 true：进入页面，false 表示无转场（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
针对本应用要查的：
- 目的地 Activity 有没有关掉或换掉切换动画：源工程里目的地 Activity 及其基类的 Java / Kotlin 文件，startActivity、finish 调用处的前后，按 overridePendingTransition 搜；参数是 (0, 0) 就是关闭转场；没有调用就按主题的默认动画查
- 没调用时四段默认动画的值：规格里的导航契约；没有时去 Android SDK platforms/android-<参照机 API>/data/res/anim/activity_{open,close}_{enter,exit}.xml；alpha 的 from 写进 opacity，scale 的 from（入场）或 to（退场）写进 scale，translate 写进 translate，duration、interpolator 写进 duration、curve
未核实：overridePendingTransition 传自定义动画资源（不是 0, 0）时怎么对到 Push / Pop 四段，族里规矩没有查实；应用主题自己覆盖 windowAnimationStyle 时各段动画取自哪个属性，族里规矩没有查实
来源：2 张卡，2 个应用
- case-6f936bc6ca2d4ec18528（Bubble Shooter）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2
- case-ab2bd55b44e47971676a（Privacy Friendly 2048）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
