# 规格提取把 AndroidManifest 声明（含未声明的平台缺省）解析成实际行为与鸿蒙目标值并指派实现：未声明 screenOrientation 时 EntryAbility 写 orientation: auto_rotation_restricted；未声明 windowSoftInputMode 时按是否含可滚动视图取 RESIZE/OFFSET，并写出首屏焦点与是否弹键盘；“默认”不能作目标值

## 何时使用

规格提取阶段，为每个 Activity 整理全屏、方向、软键盘等窗口行为，并整理 application 级属性（备份等）时；把“横竖屏双布局”“默认弹出”这类结论写进决策账本或页面规格时

## 适用情境

窗口方向（如 screenOrientation=sensorLandscape）只声明在 AndroidManifest，Java 源码只见全屏标志一类调用；页面规格模板与元数据可能没有方向字段。也包括 application 显式 allowBackup=false，activity 未声明 screenOrientation、windowSoftInputMode 而依赖平台缺省；界面图谱把它们记为 unspecified/unknown，功能基线与计划都没有对应任务，目标备份配置保持模板值。 也包括各 activity 未声明 screenOrientation、源有 layout-land/values-land，规格只写“横竖屏双布局全支持”，module.json5 的 abilities 没有 orientation；以及未声明 windowSoftInputMode、布局含 EditText 和 ListView/ScrollView（或 Activity 继承 ListActivity），规格只写“无 windowSoftInputMode（默认弹出）”。

## 例外与边界

- 第 2 步的“可滚动视图”指安卓登记的滚动容器，不是能滚动的视图都算：显式写了 android:isScrollContainer 的按它；没写时开了竖直滚动条的才算，ListView、GridView、ScrollView 的平台样式开了竖直滚动条、RecyclerView 构造时自己登记，都算；androidx 的 NestedScrollView 不自己登记、库里也没有默认样式，布局和应用主题都没给它开竖直滚动条（android:scrollbars="vertical"）或 isScrollContainer 时不算，这时安卓取 adjustPan，目标写 OFFSET
- 窗口带全屏标志（FLAG_FULLSCREEN，主题 windowFullscreen 或代码设置）时，安卓忽略 adjustResize、窗口保持全屏不缩小，按“含可滚动视图取 RESIZE”推出的目标值不成立；这类页不写 RESIZE，源端实际表现上机看过再定目标值
- 源码在运行时调 setRequestedOrientation 时，以运行时设的方向为准写目标值（锁定值按第 1 步写进入页设方向、离开恢复），不按“未声明即随系统旋转”写 auto_rotation_restricted

## 原因

只读 Java 源码会漏掉 manifest 属性；规格与页面元数据都没有方向字段时，实现者会以“规格未覆盖”跳过。记为 unspecified/unknown 的项没有目标值，下游没有写者，模板默认值（如允许备份）会保留到交付。鸿蒙 EntryAbility 不写 orientation 就不随传感器旋转，只迁两套布局时横屏分支永不出现；未声明 windowSoftInputMode 时安卓缺省 adjustUnspecified 由系统按窗口是否含可滚动视图取 adjustResize 或 adjustPan，而 ArkUI 缺省 OFFSET 整页上推；状态半 stateUnspecified 让首个可获焦视图为 EditText 时自动弹键盘，ArkUI 不会自动给输入框焦点。另一应用中注入的一行提醒只剩“无screenOrientation=跟随旋转”“无windowSoftInputMode（默认）”，写者照写安卓语义就算交差，目标值没有进入任何任务。

## 做法

1. 逐个 activity 列出 manifest 属性，把未声明项解析成实际行为再写鸿蒙目标值，“默认/按系统缺省”不能作结论：未声明 screenOrientation（随系统旋转）时，module.json5 的 EntryAbility 写 orientation: auto_rotation_restricted，与权限并列为 module.json5 必做项；sensorLandscape 等锁定值写成“进入页 setPreferredOrientation(对应方向)、离开恢复”的验收条目。
2. 未声明 windowSoftInputMode 且含 EditText 时拆成两条验收并各自指派：调整方式——窗口含 ListView/ListActivity/ScrollView 等可滚动视图为 adjustResize（目标窗口级 setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)），否则为 adjustPan（OFFSET）；状态——首屏焦点给布局顺序中第一个可获焦视图（AdapterView 只在有数据时可获焦），写清各数据分支谁获焦、是否自动弹键盘；要自动弹键盘的分支，目标端等窗口获焦（WINDOW_ACTIVE）以后才给输入框请求焦点。
3. application 级属性同样逐项映射（如 allowBackup → allowToBackupRestore）并为每项指派实现任务，不留 unknown。

## 可选检查

- 解除旋转锁并转 90°，窗口宽高互换、横屏分支出现；点输入框弹出键盘时顶部内容不被推出屏幕、内容区收缩。

来源支持：7 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕android:screenOrientation 不写时取 unspecified（-1）：由系统决定方向；用户没有在设置里关掉基于传感器的旋转时，方向随设备旋转，关掉时忽略传感器
- 〔原因 / 做法第 1 步〕module.json5 abilities 的 orientation 可缺省，缺省值为 unspecified（未指定方向，由系统自动判断显示方向）
- 〔做法第 1 步〕orientation 取 auto_rotation_restricted 时，系统旋转锁定开关关闭的情况下方向可随传感器旋转；取 auto_rotation_unspecified 时是受系统旋转锁定开关控制、并由系统判定的自动旋转模式
- 〔原因 / 做法第 1 步〕鸿蒙手机上 EntryAbility 不写 orientation 时，解除旋转锁并把设备转到 90° 后窗口 Rotation 仍为 0；EntryAbility 写 "orientation": "auto_rotation_restricted" 时同样操作，Rotation 为 1，窗口变成横屏尺寸
- 〔做法第 1 步〕运行时窗口方向枚举 window.Orientation 里，AUTO_ROTATION_RESTRICTED（8）随传感器旋转、受旋转锁控制；AUTO_ROTATION_LANDSCAPE（7）随传感器只在横向内旋转、忽略旋转锁；UNSPECIFIED（0）是默认值，由系统决定
- 〔做法第 1 步〕android:screenOrientation 的 sensorLandscape（6）要求横屏，但可按传感器在正反两个横向之间切换
- 〔做法第 3 步〕android:allowBackup 不写时默认为 true（允许备份）
- 〔做法第 3 步〕鸿蒙备份恢复的元数据资源配置文件（module.json5 的 metadata 引用的 profile，如 backup_config.json）里，allowToBackupRestore 默认为 false，不写就不允许备份恢复
- 〔原因 / 做法第 2 步〕windowSoftInputMode 的调整方式未指定（adjustUnspecified，缺省）时，系统按窗口内容里有没有能滚动内容的视图在 resize 和 pan 之间自动选择，有就 resize
- 〔做法第 2 步〕ViewRootImpl 在首次遍历或视图可见性变化时判定：调整方式为 unspecified 时，已登记的滚动容器里只要有一个 isShown() 就取 SOFT_INPUT_ADJUST_RESIZE，否则取 SOFT_INPUT_ADJUST_PAN
- 〔做法第 2 步〕没有显式设 android:isScrollContainer 的视图，只要开启了竖直滚动条就被登记为滚动容器；平台样式 Widget.AbsListView（ListView、GridView 的父样式）和 Widget.ScrollView 都设了 scrollbars=vertical
- 〔原因 / 做法第 2 步〕windowSoftInputMode 的 stateUnspecified（0）是缺省：软键盘状态未指定，由系统按它认为最合适的方式处理
- 〔做法第 2 步〕AdapterView 的 adapter 为 null 或条数为 0（且不在过滤模式）时把自己设为不可获焦；有数据时按应用期望的可获焦状态设置
- 〔原因 / 做法第 2 步〕安卓上未声明 windowSoftInputMode、布局里 EditText 前只有一个由 adapter 填充的 ListView 的 ListActivity，清数据冷启动、列表为空时 EditText 获焦并弹出软键盘；有记录时 ListView 获焦，不弹软键盘
- 〔原因 / 做法第 2 步〕鸿蒙冷启动时，在窗口获焦（WINDOW_ACTIVE）之前对 TextInput 请求焦点，输入框报告 focused=true，但不绑定输入法、不弹软键盘
- 〔原因 / 做法第 2 步〕UIContext.setKeyboardAvoidMode 不调用时为 KeyboardAvoidMode.OFFSET；OFFSET（0）是布局整体上移，RESIZE（1）是布局尺寸缩小
