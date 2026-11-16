# configChanges 不含 orientation 时，规格列出旋转重建后回到布局初值的可见状态

审的是：规格
触发（任一种）：
- 读到：AndroidManifest 的 <activity> android:configChanges 不含 orientation（如只写 screenSize）；点击监听里用 setBackgroundResource / setImageResource 改视图，没进 onSaveInstanceState；写错的样子：页面规格只把这类状态写成页内状态和「返回重入后保持」，没有「旋转后回到布局初值」的条目
适用范围：规格提取阶段写页面规格，源端 Activity 旋转会重建时
做法：
- 读 manifest 里每个 Activity 的 configChanges；不含 orientation 就把旋转写成 Activity 重建，并逐页列出重建后消失的可见状态：代码设置、没存进 onSaveInstanceState 的视图属性回到布局初值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- configChanges 列出的是 Activity 自己处理的配置变化；没列的变化发生时 Activity 重启：不含 orientation 就是旋转重建（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges（按应用的 compileSdk 取对应平台））
- configChanges 的 orientation = 0x0080（用户旋转设备）、screenSize = 0x0400（可用屏幕尺寸变化，横竖屏切换时也变）：只写 screenSize 不能挡住旋转重建（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 orientation、screenSize（按应用的 compileSdk 取对应平台））
- 配置变化默认让当前 Activity 走 onPause、onStop、onDestroy 销毁：重建时旧实例的视图状态不保留（出处：android.app.Activity（类注释 Configuration Changes 一节））
针对本应用要查的：
- 哪些可见状态是代码设置、重建后会丢的：源工程 Activity 里的点击监听和回调，找 setBackgroundResource、setImageResource、setText 之类调用；再看 onSaveInstanceState / onRestoreInstanceState 有没有存它；没存的就写进「旋转重建后回到布局初值」
来源：1 张卡，1 个应用
- case-d3f1bcc562a64e5f56f7（Bubble Shooter）：做法第 1 步 ← 建议 3、建议 2、诊断
