# 字体文件逐个 registerFont（多字重按“族-字重”命名），排版样式与对应 Text 引用注册名；不以 fontWeight 合成粗体代替字体文件

## 何时使用

主题令牌与界面实现阶段，把 Compose FontFamily(Font(R.font.x, weight), ...) 或 View 布局里按控件指定的字体文件（三方 TextView 的 typeface 属性、android:fontFamily）迁到 ArkUI，或确定全局字体注册由谁调用时

## 适用情境

源字族为同一族声明多个字重文件，资源阶段已把字体文件放进 rawfile；目标要先 registerFont 才能用 fontFamily 引用；主题令牌、公共组件、页面与入口由不同任务分批生成。 也包括 View 布局用三方库属性（如 pixlui:typeface）或 android:fontFamily 给不同 TextView 指定不同字体文件，映射基线只写“→ fontFamily，字体入 rawfile/fonts”。

## 例外与边界

- 字体要在整个应用生效时，文档要求在 EntryAbility 的 onWindowStageCreate 里、windowStage.loadContent 的回调中注册；工程已在那里注册的，保留原调用点，不要挪到入口页 aboutToAppear，也不要在两处重复注册（registerFont 是异步接口，不支持并发调用）。“入口页 aboutToAppear 调用一次”只用于还没有任何真实调用点的情形。
- familyName 文档建议只用字母、数字和下划线：“族-字重”指每个文件一个名字的命名结构，注册名写成 Family_Bold 这类形式即可，已按此注册的名字不必改成连字符。

## 原因

registerFont 的一个 familyName 只绑定一个文件；把整族注册成一个名字会让字重层级失效。若因此放弃注册，或注册函数没有调用点，fontFamily 引用的是未注册名，全应用静默回退系统字体，编译不报错。 只在注释里写字体名或用 fontWeight(Bold) 合成粗体时，字形与字宽仍是系统字体。

## 做法

1. 每个字体文件注册独立的 familyName（如“族-字重”）：registerFont({ familyName, familySrc: $rawfile('fonts/<file>.ttf') })；排版样式引用注册名，fontWeight 设为该文件本身的字重。
2. 注册函数由应用入口页 aboutToAppear 调用一次；收尾检索 registerFont，确认有真实调用。
3. 源布局按控件指定字体文件（三方 TextView 的 typeface 属性如 pixlui:typeface，或 android:fontFamily）时，先确认 rawfile/fonts 下有该文件并已注册，再在对应 Text 上写 fontFamily(注册名)；不以 fontWeight(FontWeight.Bold) 合成粗体代替粗体字体文件，注释里写字体名不算已应用。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕registerFont 的字体注册过程是异步的，不支持并发调用；文档建议在页面初始化阶段（如 aboutToAppear）提前调用，让字体在使用前注册完成
- 〔做法第 2 步〕应用要全局使用自定义字体时，文档要求在 EntryAbility 的 onWindowStageCreate 里、windowStage.loadContent 的回调中注册
- 〔做法第 1、3 步〕Text 的 fontWeight 传 number 时取值 [100, 900]、间隔 100，数值越大越粗；应用没有另设时默认 FontWeight.Normal（数值 400；穿戴设备默认 Regular）
