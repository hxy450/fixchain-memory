# 源端用 TaskStackBuilder 带父栈跳转时，规格按 Manifest 父链写出完整栈和返回落点

审的是：规格
触发（任一种）：
- 读到：源码 TaskStackBuilder.create(this).addNextIntentWithParentStack(intent).startActivities()，Manifest 为目标写了 android:parentActivityName 或 PARENT_ACTIVITY meta-data；写错的样子：规格的实现映射写「pushPathByName 带回栈（Main 为根天然栈底）」，验收写「返回落回来源页」，副作用表没写清栈和按父链重建
适用范围：规格提取阶段，把源端父栈跳转（尤其是被多个页面继承的基类方法）映射到 NavPathStack 并写返回验收时
做法：
- 按 Manifest 父链写出跳转后的完整栈和返回落点（如 [父页, 目标]，返回到父页），实现映射写「NavPathStack.clear → 按父链依次 pushPathByName 父页 → pushPathByName 目标」
- 把某页规格里的映射行复用到被多个宿主页调用的基类方法前，先核对它成立的前提（「根页天然在栈底」只在来源页就是根页时成立）
- 判据用从非根页发起的样例：非根页 → 抽屉 → 目标 → 返回，应回到父页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- addNextIntentWithParentStack 把目标在 Manifest 里声明的父链一并加入合成的任务栈：跳转后的栈由目标的父链决定，与来源页无关（出处：android.app.TaskStackBuilder#addNextIntentWithParentStack）
- 栈底那个 Intent 加 FLAG_ACTIVITY_NEW_TASK | FLAG_ACTIVITY_CLEAR_TASK | FLAG_ACTIVITY_TASK_ON_HOME：startActivities 会清掉当前任务，不是在当前栈上压栈（出处：android.app.TaskStackBuilder#getIntents）
针对本应用要查的：
- 每个目标的父链：源工程 AndroidManifest.xml 里目标 <activity> 的 android:parentActivityName，或 <meta-data android:name="android.support.PARENT_ACTIVITY">；从目标沿父链一路往上读到没有父为止，倒过来就是跳转后的栈
来源：1 张卡，1 个应用
- case-ece3192169e927e18aa5（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2
