# 设窗口级属性时拿的窗口对象

agent 会看到什么：读到源端经 LocalView 或 Activity 取 window，再设 FLAG_SECURE、isAppearanceLightStatusBars 这类窗口级属性；产物里主题服务或页面用 window.getLastWindow(context) 取窗口，还是在 onWindowStageCreate 取到主窗口后注入

## 规矩

- rule-34d35c31e0b5｜窗口级属性在 onWindowStageCreate 取到主窗口后执行，不靠 getLastWindow｜读到：源端在组合期由 LocalView 取 Activity window，再设 FLAG_SECURE 和 isAppearanceLightStatusBars，此时窗口已存在；写错：主题服务用 window.getLastWindow(context) 取窗口设状态栏极性或隐私窗，HANDOFF 写 owner=EntryAbility.onCreate，onWindowStageCreate 里没有注入主窗口
