# 入口 Ability 的全局异常监听（errorManager）

agent 会看到什么：读过的源码里有或没有 setDefaultUncaughtExceptionHandler，规格或台账写了未捕获异常照源复刻还是要捕获；交回的 EntryAbility.onCreate 里 errorManager.on('error', …) 的有无和它不一致

## 规矩

- rule-a2774cee7f6d｜入口 errorManager.on('error') 按规格定：照源复刻崩溃时不注册，否则补注册｜读到：入口 UIAbility 由模板改写（onCreate 只有 hilog.info），安卓源没有 UncaughtExceptionHandler 一类的全局异常处理；写错：EntryAbility 或 AbilityStage 的 onCreate 没有 errorManager.on('error', …)，onDestroy 没有 off
