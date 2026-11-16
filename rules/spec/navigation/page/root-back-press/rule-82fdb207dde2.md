# 源根 Activity 没覆写返回时，规格的返回契约先列 finish() 的效果，不直接写退后台

审的是：规格
触发（任一种）：
- 读到：源启动 Activity 没有覆写 onBackPressed / onKeyDown，onDestroy 里有 release() / close()，页面持有 EditText 文字、所选值、背景音乐等实例态；写错的样子：规格写「源 Activity 默认：退后台，不出栈」，或把「栈深≤1 时 moveAbilityToBackground 不 pop」写成验收项，没写返回会触发 onDestroy、实例态回到初值
适用范围：规格提取阶段为没有覆写返回处理的启动（根）Activity 写栈底返回契约
做法：
- 返回契约先列 finish() 的可观察效果：onPause、onStop、onDestroy 各自做什么（释放哪些资源）；哪些实例态回到初值（输入框文字、所选值、音乐播放位置）；哪些静态单例保留
- 只有参照设备按实际启动方式实测为移到后台时才写「退后台、保留实例」；确认不了时，写成待核验收项：「返回后再启动时输入框、所选值、音乐、续局入口的状态」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- S 以前默认 finish 当前 Activity；S 起，任务根 Activity 且清单里声明了 ACTION_MAIN + CATEGORY_LAUNCHER 的 intent-filter 时，连同任务移到后台而不 finish，其他 Activity 照样 finish：Activity 默认返回行为随平台版本和清单声明而变（出处：android.app.Activity#onBackPressed）
- SDK 37 模拟器上用 am start -n 启动，根 Activity 返回后进程 pid 不变，再启动为 WARM，输入框和所选等级回到初值，静态单例里的续局仍在：实测是 finish 语义：onDestroy 执行、实例态丢失、进程和静态单例保留（出处：卡里修好并验证过）
针对本应用要查的：
- 根 Activity 是否声明了启动器 intent-filter、参照设备的平台版本和启动方式：源工程 AndroidManifest.xml 里这个 activity 的 intent-filter（android.intent.action.MAIN、android.intent.category.LAUNCHER）；参照设备的系统版本；两者都满足且实测返回后再启动是 HOT（原实例恢复）才写退后台；否则按 finish 写
未核实：从桌面图标（MAIN/LAUNCHER）启动时 SDK 37 是否同样 finish，卡里没实测；卡里实测平台是 SDK 37 模拟器，onBackPressed 的说明照本机 android-36.1 源码核对
来源：1 张卡，1 个应用
- case-65b537ef55556598f2ee（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 2 ← 诊断、建议 4
