# 入口 onCreate 里 super.onCreate 之前的调用

agent 会看到什么：读到入口 Activity.onCreate 在 super.onCreate / setContentView 之前调用 setTheme(...) 等；规格只写设置页保存后即时生效，没写冷启动首帧前恢复和目标承接位置

## 规矩

- rule-ff500db88fd8｜入口 onCreate 里 super.onCreate 之前的调用，连同首帧前生效的时机写进规格｜读到：入口 Activity.onCreate 在 super.onCreate / setContentView 之前调用 setTheme(...) 等；写错：规格只写设置页保存后 setColorMode 即时生效，没写冷启动时首帧前恢复主题，也没指定目标承接位置；这一时机只留在设计参考里
