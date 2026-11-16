# Activity 窗口的 FLAG_KEEP_SCREEN_ON

agent 会看到什么：读到 Activity 的 onCreate 里 getWindow().addFlags(FLAG_KEEP_SCREEN_ON)，没有 clearFlags；规格的映射行或验收只写「onCreate 时机 setWindowKeepScreenOn(true)」「进入该页不熄屏」

## 规矩

- rule-ad84365156f4｜Activity 窗口加 FLAG_KEEP_SCREEN_ON 且无清除时，规格写成页面可见期内成对开关｜读到：源端 Activity 的 onCreate 里 getWindow().addFlags(FLAG_KEEP_SCREEN_ON)（建议里也点名 FLAG_SECURE 等窗口标志），没有 clearFlags 之类的清除代码；写错：规格的映射行或验收只写「onCreate 时机 setWindowKeepScreenOn(true)」，没写作用范围是该页可见期间，也没写离开该页时设回 false
- rule-3de5a775f1aa｜窗口常亮的验收只有进入页面不熄屏时，补一条离开页面后按系统超时熄屏｜读到：源端 Activity 自身窗口上 getWindow().addFlags(FLAG_KEEP_SCREEN_ON)，没有清除代码；写错：验收条目的设备判据只有「进入该页后屏幕不自动熄灭」，缺离开该页（返回主菜单、进设置等）之后的熄屏判据
