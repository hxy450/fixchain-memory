# Activity 的 configChanges 和配置变化重建

agent 会看到什么：读过的 AndroidManifest 里 activity 没写 android:configChanges 或不含 orientation，源码有 onSaveInstanceState、直接 show 的对话框或点击后改过的视图；交回的规格没写配置变化重建后哪些状态保留、哪些回到初值

## 规矩

- rule-fd54f3aed22a｜Activity 未声明 configChanges 时，规格写明配置变化重建的 AC 和时序｜读到：AndroidManifest.xml 里该 Activity 没有 android:configChanges（可能只有 android:screenOrientation），Activity 实现了 onSaveInstanceState，并在 onCreate 里按 savedInstanceState 恢复；写错：规格的实现映射把 onSaveInstanceState / savedInstanceState 分支写成「进程恢复」「不迁移，冷启即 load」，生命周期 AC 只覆盖页面显隐和杀进程冷启，没有配置变化重建
- rule-b58dd6c1fbb6｜configChanges 不含 orientation 时，规格列出旋转重建后回到布局初值的可见状态｜读到：AndroidManifest 的 <activity> android:configChanges 不含 orientation（如只写 screenSize）；点击监听里用 setBackgroundResource / setImageResource 改视图，没进 onSaveInstanceState；写错：页面规格只把这类状态写成页内状态和「返回重入后保持」，没有「旋转后回到布局初值」的条目
- rule-1d87a6b39e37｜Activity 未声明 configChanges 时，规格写出重建后消失的对话框和目标端的关闭要求｜读到：Manifest 的 <activity> 没有 android:configChanges，也没有 screenOrientation 锁定；源码用 AlertDialog.Builder(...).show() / Dialog.show() 直接弹出对话框，不经 DialogFragment、showDialog 或 DialogPreference；写错：页面规格只写「Manifest 事实: 无 configChanges、无 screenOrientation」溯源注记；状态接口的关闭条件和验收里没有「配置变化/旋转时关闭对话框」
- rule-2b907fd94568｜未声明 configChanges 时，重建契约列出新实例重跑 onCreate/onResume 的效果｜读到：Activity 没有 android:configChanges；onCreate 的 savedInstanceState 分支、onStart 或 onResume 里有重读持久数据并刷新显示、复位导航或计数字段、按启动 Intent 再次弹窗或导入的语句；写错：规格的重建或配置变化契约只写 onSaveInstanceState 存取和对话框关闭或保留，没有列这些语句的效果；onResume 只映射成回前台路径，重建验收里没有它们
- rule-d5c89ffe3c5d｜DialogFragment 参数经 setter 注入时，规格写明重建后丢失哪些字段、内容和按钮变成什么｜读到：所在 Activity 没声明 android:configChanges；DialogFragment 子类的监听器、文件路径、标题、预填文本经 setter 或构造参数写进实例字段，没有放进 setArguments，也没有在 onSaveInstanceState 里存；写错：规格只写「托管 DialogFragment 保留」「目标不重建，弹层随页内状态保留，onConfigurationUpdate 不关闭」，没有逐个对话框列出重建后丢失的字段和按钮效果，也没有对应的验收条目
- rule-7cb5ff93de65｜源 Activity 未声明 configChanges 的 Compose 界面，规格写“重建后按新尺寸重算”验收｜读到：AndroidManifest 里 Activity 没有 android:configChanges；Compose 组件在 BoxWithConstraints 里读 maxWidth，再在带键的 LaunchedEffect(key)（键不含宽度）里按宽度算格数、列数写回 ViewModel；写错：AC 写“仅 key 变化触发、画布宽度变化不重算”或“转屏后两端均不重算”，同一份规格里又写着源端转屏重建、remember 复位
- rule-cdf9be441fcb｜规格把语言重读写成「$r 自动重解析」时，要求列出代码内文案快照及页面侧重取订阅｜读到：源端 Activity 未声明 configChanges，语言变化走 recreate 重读全部文案；写错：验收条目或计划把「语言变化重读文案」写成「全应用 $r 重解析」或「随语言存储同链刷新」，页面订阅清单只列弹层关闭、计数重判等，没有代码内取值的文案快照
