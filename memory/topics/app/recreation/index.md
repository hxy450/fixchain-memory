# app/recreation

源端 Activity 重建与新实例语义：配置变化、进程回收、重启与新请求在不重建的 UIAbility 上显式处理

[上一级](../index.md)

## 本级经验

- [singleton 收新请求时带版本重跑请求解析](lesson-45ae43a8f3ace3513834.lesson.md) · 阶段：spec/execute · 信号：android:launchMode, launchType, onNewWant, onCreate
- [保留实例按是否配置重建区分，不以单例存在代替](lesson-ed571550c44efdeb321e.lesson.md) · 阶段：spec/execute · 信号：NonConfigurationInstance, onConfigurationUpdate, hasInstance, configChanges
- [回收重建单列分支：仅系统回收时恢复整栈与原参数](lesson-b0405a29415547485ecb.lesson.md) · 阶段：spec/execute · 信号：rememberNavController, NavHost, savedInstanceState, TaskStackBuilder
- [无 configChanges 时按源重建时序刷新关弹窗](lesson-94715d0df4c03a8fb5a5.lesson.md) · 阶段：spec/execute · 信号：android:configChanges, screenOrientation, onSaveInstanceState, savedInstanceState
- [有随系统字号缩放的文本就声明跟随系统字号](lesson-ea965b7baf2488be23cd.lesson.md) · 阶段：spec/plan/execute · 信号：fontScale, configChanges, fontSizeScale, followSystem
- [杀进程意在重启用 restartApp 不用退出](lesson-73618bb856a8a7dfe7fc.lesson.md) · 阶段：spec/execute · 信号：System.exit, Runtime.exit, Process.killProcess, ApplicationContext.restartApp
