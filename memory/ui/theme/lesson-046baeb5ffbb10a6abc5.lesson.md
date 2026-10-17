# 多字重字族按“族-字重”逐文件 registerFont，排版样式引用注册名，入口调用一次注册

ID：`lesson-046baeb5ffbb10a6abc5` · 版本：3

[本主题](index.md)

## 何时使用

主题令牌阶段，把 Compose FontFamily(Font(R.font.x, weight), ...) 迁到 ArkUI，或确定全局字体注册由谁调用时；把 View 布局中 pixlui:typeface、android:fontFamily 指定的字体文件落到 Text 时

## 适用情境

源字族为同一族声明多个字重文件，资源阶段已把字体文件放进 rawfile；目标要先 registerFont 才能用 fontFamily 引用；主题令牌、公共组件、页面与入口由不同任务分批生成。也包括 View 体系布局用 pixlui:typeface 或 android:fontFamily 指定 ttf，规格要求字体文件入 rawfile/fonts 并用 fontFamily 替换，写者只在注释写字体名。

## 原因

registerFont 的一个 familyName 只绑定一个文件；把整族注册成一个名字会让字重层级失效。若因此放弃注册，或注册函数没有调用点，fontFamily 引用的是未注册名，全应用静默回退系统字体，编译不报错。

## 做法

1. 每个字体文件注册独立的 familyName（如“族-字重”）：this.getUIContext().getFont().registerFont({ familyName, familySrc: $rawfile('fonts/<file>.ttf') })（全局 font.registerFont 自 API 18 废弃，改经 UIContext 取得的 Font 对象注册；HarmonyOS 文档 js-apis-font，访问于 2026-10-17）；排版样式引用注册名，fontWeight 设为该文件本身的字重。
2. 注册函数由应用入口页 aboutToAppear 调用一次；收尾检索 registerFont，确认有真实调用。
3. 源布局按字体文件指定字族时，确认 rawfile/fonts 下有该 ttf，注册后在对应 Text 上写 fontFamily(注册名)；不用 fontWeight(Bold) 代替粗体字族文件，注释里的字体名不算已应用。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-9cfde635e67a08373fe6](../../../store/cases/case-9cfde635e67a08373fe6/2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985.json) · 结论：recommendation:2
  卡片版本：`2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985`
- [case-cfcb1be64b70e328ad81](../../../store/cases/case-cfcb1be64b70e328ad81/3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381.json) · 结论：diagnosis, recommendation:2
  卡片版本：`3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381`
