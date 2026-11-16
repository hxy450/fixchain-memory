# Activity 只委托辅助类弹窗时，规格展开辅助类和它的布局，写明点击反馈、延时和回调顺序

审的是：规格
触发（任一种）：
- 读到：Activity 里只有一句对辅助类 show…Dialog 方法的委托调用（带同意回调 lambda，里面持久化并 dismiss），勾选控件和延时都在辅助类和它 inflate 的布局里；写错的样子：验收条目只写「显示同意弹窗；接受后先持久化再继续」，android_source_anchors 里没有这个辅助类和它 inflate 的主弹窗布局，没写点击后的选中反馈、延时和回调顺序
适用范围：规格提取阶段，源端弹窗由 Activity 委托给辅助类构建时
做法：
- 打开辅助类实现和它 inflate 的每个布局，列进 android_source_anchors；dialog 契约覆盖辅助类用到的每个布局（主弹窗，不只是二次确认弹窗）
- 验收条目写明点击后的视觉反馈、延时和回调顺序，如「setChecked(true, true) 播放勾选动画 → postDelayed N ms → 回调并 dismiss」，N 取源码
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- View#postDelayed(Runnable action, long delayMillis)：delayMillis 单位是毫秒，Runnable 在 UI 线程上执行：源端延时回调的写法，规格里照写毫秒数（出处：android.view.View#postDelayed）
针对本应用要查的：
- 点击后的反馈和延时：源工程里该辅助类构建弹窗的方法：同意区的点击监听，以及它 inflate 的布局 XML 里的勾选控件；读出 setChecked 的参数、postDelayed 的毫秒数和回调、dismiss 的先后，照顺序写进验收条目
来源：1 张卡，1 个应用
- case-c89aab9f64f62b2e0de6（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
