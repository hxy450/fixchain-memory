# UI 清单和派工里的源端系统栏形态

agent 会看到什么：源 Activity 只有 FEATURE_NO_TITLE、FLAG_FULLSCREEN 一类窗口写法或主题非全屏，UI 清单和派工却写「各页 needs_immersive_safearea=true」「无标题全屏」，或预写 setWindowSystemBarEnable([]) 隐藏全部系统栏

## 通用查法

### UI 清单或派工写系统栏和避让要求前，按源主题和窗口标志逐边写出系统栏形态

审的是：计划与派工
触发（任一种）：
- 读到：源 Activity 或它用的主题里有 requestWindowFeature(FEATURE_NO_TITLE)、FLAG_FULLSCREEN、windowFullscreen、windowTranslucentStatus 一类窗口写法，或者一个都没有；写错的样子：UI 清单或派工按惯例写「各页 needs_immersive_safearea=true」「无标题全屏」「游戏全屏就隐藏系统栏」，或预写 setWindowSystemBarEnable([]) 这类参数，没写源端状态栏、导航栏各自的形态
适用范围：主会话写 UI 清单、给入口窗口和页面派工，定系统栏与避让任务时
做法：
- 逐个源 Activity 读窗口信号：清单文件里它用的主题、主题里的全屏和透明状态栏项、代码里的窗口标志；逐边定出状态栏、导航栏是隐藏、透明还是照源着色
- 清单和派工按逐边结果写 needs_immersive_safearea 和避让任务，不写与之冲突的系统栏 API 参数；一个信号都没有时写非全屏、系统栏照源着色、页面不做 inset 避让
针对本应用要查的：
- 每个源 Activity 的窗口形态：源工程 AndroidManifest.xml 里该 Activity 或 application 的 android:theme，到 res/values 的样式文件里找这个主题的 windowFullscreen、windowTranslucentStatus；Activity 源码里 requestWindowFeature 和 getWindow() 加的窗口标志；逐边记下状态栏、导航栏的形态。例：只有 FLAG_FULLSCREEN 加 FEATURE_NO_TITLE 时，状态栏隐藏、导航栏可见；主题是 Theme.Holo、代码只有 FEATURE_NO_TITLE 时是非全屏窗口
未核实：主题的 parent 链和代码里的窗口标志谁覆盖谁，族里规矩没有查实
来源：2 张卡，2 个应用
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-bbb49cc9ec510f04eb33（Bubble Shooter）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3

## 规矩

- rule-9ccdd7bed963｜源窗口非全屏时，UI 清单和派工不把各页标成沉浸式、不派四层避让｜读到：源主题非全屏（Theme.Holo 等），代码只有 requestWindowFeature(FEATURE_NO_TITLE)，没有任何全屏或透明系统栏标志；写错：UI 清单写「各页全部 needs_immersive_safearea=true」「FEATURE_NO_TITLE → 无标题全屏」，派工写「needs_immersive_safearea: true → 调 Skill(arkts-immersive-safearea) 实施四层架构」和底部安全区任务
- rule-f9c42bb77195｜派工只写源端逐边的系统栏形态，不预写与之冲突的系统栏 API 参数｜读到：源 Activity 只有 FLAG_FULLSCREEN + FEATURE_NO_TITLE，导航栏可见；写错：派工里预写了 setWindowSystemBarEnable([]) 等隐藏全部系统栏的参数，或写「游戏全屏就隐藏系统栏」
- rule-e288f670e7f7｜派工把沉浸字段缺失当 false 跳过时，改为按页面规格 page_type 判定的值实施｜读到：页面规格按 page_type=full_screen_page 判定 needs_immersive_safearea=true；派发模板写「仅当 meta.json needs_immersive_safearea: true 时实施，false 时跳过」；写错：派工写「needs_immersive_safearea 缺失→按 false 处理」「false/缺失时跳过本契约」
