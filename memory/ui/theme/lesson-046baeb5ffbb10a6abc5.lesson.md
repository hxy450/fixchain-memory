# 字体文件逐个 registerFont（多字重按“族-字重”命名），排版样式与对应 Text 引用注册名；不以 fontWeight 合成粗体代替字体文件

ID：`lesson-046baeb5ffbb10a6abc5` · 版本：2

[本主题](index.md)

## 何时使用

主题令牌与界面实现阶段，把 Compose FontFamily(Font(R.font.x, weight), ...) 或 View 布局里按控件指定的字体文件（三方 TextView 的 typeface 属性、android:fontFamily）迁到 ArkUI，或确定全局字体注册由谁调用时

## 适用情境

源字族为同一族声明多个字重文件，资源阶段已把字体文件放进 rawfile；目标要先 registerFont 才能用 fontFamily 引用；主题令牌、公共组件、页面与入口由不同任务分批生成。 也包括 View 布局用三方库属性（如 pixlui:typeface）或 android:fontFamily 给不同 TextView 指定不同字体文件，映射基线只写“→ fontFamily，字体入 rawfile/fonts”。

## 原因

registerFont 的一个 familyName 只绑定一个文件；把整族注册成一个名字会让字重层级失效。若因此放弃注册，或注册函数没有调用点，fontFamily 引用的是未注册名，全应用静默回退系统字体，编译不报错。 只在注释里写字体名或用 fontWeight(Bold) 合成粗体时，字形与字宽仍是系统字体。

## 做法

1. 每个字体文件注册独立的 familyName（如“族-字重”）：registerFont({ familyName, familySrc: $rawfile('fonts/<file>.ttf') })；排版样式引用注册名，fontWeight 设为该文件本身的字重。
2. 注册函数由应用入口页 aboutToAppear 调用一次；收尾检索 registerFont，确认有真实调用。
3. 源布局按控件指定字体文件（三方 TextView 的 typeface 属性如 pixlui:typeface，或 android:fontFamily）时，先确认 rawfile/fonts 下有该文件并已注册，再在对应 Text 上写 fontFamily(注册名)；不以 fontWeight(FontWeight.Bold) 合成粗体代替粗体字体文件，注释里写字体名不算已应用。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-9cfde635e67a08373fe6](../../../store/cases/case-9cfde635e67a08373fe6/2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985.json) · 结论：diagnosis, recommendation:2
  卡片版本：`2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985`
- [case-cfcb1be64b70e328ad81](../../../store/cases/case-cfcb1be64b70e328ad81/3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381.json) · 结论：diagnosis, recommendation:2
  卡片版本：`3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381`
