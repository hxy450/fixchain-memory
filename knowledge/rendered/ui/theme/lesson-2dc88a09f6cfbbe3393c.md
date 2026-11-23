# 源端一个背景选择对象同时表达图片、单色与渐变时，逐分支迁移到目标渲染绑定：url 非空用图片，否则按颜色数与方向生成纯色或渐变

## 何时使用

渲染实现阶段，把编辑器的背景选择对象绑定到预览或组件的背景渲染节点时

## 适用情境

源端一个选择对象同时承载 url、colors、orientation，渲染方法按 url 非空→图片、colors 长度 1→纯色、长度 2→按方向渐变分支；目标在模型层把选择对象映射到运行时渲染属性，外观配置模块已能保存与恢复 colors 和 orientation。

## 原因

只实现首个分支时，图库背景能显示，纯色与渐变选择却没有效果；写者把多分支的源方法概括成“使用 url”，测试也只覆盖 url 用例，遗漏不会被发现。

## 做法

1. 迁移前把源方法的每个分支（图片、纯色、渐变、为空恢复默认）列成清单，逐项落到目标绑定（如 url 为空且 colors 非空时清空运行时图片并设置填充色与角度；角度按 ArkUI 的定义换算（0 度自下而上、顺时针为正：LEFT_RIGHT 对应 90，TOP_BOTTOM 对应 180，BOTTOM_TOP 对应 0），不照搬 GradientDrawable 的角度数值），未实现的分支明确标注。
2. 测试覆盖每种输入形态：url、colors 长度 1、colors 长度 2 加方向、选择对象为空；写交接摘要前对照源方法原文，摘要只剩一个分支时回查遗漏。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕GradientDrawable.Orientation 八个值表示渐变的起止方向：TOP_BOTTOM 自上而下、BOTTOM_TOP 自下而上、LEFT_RIGHT 从左到右、RIGHT_LEFT 从右到左、TL_BR 左上到右下、BR_TL 右下到左上、TR_BL 右上到左下、BL_TR 左下到右上；应用没有另设方向时默认 TOP_BOTTOM
- 〔做法第 1 步〕GradientDrawable 的 XML 角度按逆时针、以从左到右为 0：0 → LEFT_RIGHT、45 → BL_TR、90 → BOTTOM_TOP、135 → BR_TL、180 → RIGHT_LEFT、225 → TR_BL、270 → TOP_BOTTOM、315 → TL_BR
- 〔做法第 1 步〕ArkUI linearGradient 的 angle 单位是度，0 度时渐变方向从下往上，顺时针为正；没写时默认 180（自上而下）；angle 不是 undefined 时 direction 不生效
