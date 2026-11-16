# 决策台账里的大字体（随系统字号缩放）条目

agent 会看到什么：读到源端主体是固定 px 字号的 Canvas 自绘，但仍有 AlertDialog.Builder 系统对话框、Toast、菜单或 sp 单位的文本，Manifest 的 Activity 没声明 android:configChanges="fontScale"；决策台账写「大字体 | 不适用」，没列随系统字号缩放的文本和目标落点

## 规矩

- rule-97774d5fcfee｜裁定大字体时不以有无显式 fontScale 代码为准，源端有随系统字号缩放的文本就判为迁移｜读到：源端主体是固定 px 字号的 Canvas 自绘，但仍用 AlertDialog.Builder(...) 的系统对话框、Toast、菜单或 sp 单位的文本；Manifest 的 Activity 没有声明 android:configChanges="fontScale"；写错：决策台账写「大字体 | 不适用（Canvas 固定字号，Android 端无 fontScale 适配）」，没列系统对话框等随系统字号缩放的文本，也没写目标落点
