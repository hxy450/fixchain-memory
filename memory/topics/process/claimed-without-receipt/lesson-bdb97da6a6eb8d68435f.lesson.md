# 运行会改写源码的自愈脚本后先审阅其改动；异常尺寸、与已有显式尺寸重复或按错误密度换算的追加要回滚

ID：`lesson-bdb97da6a6eb8d68435f` · 版本：5 · 阶段：verify/converge · 主题：[process/claimed-without-receipt](index.md)

概要：自愈脚本改写 .ets 后先审 diff，异常尺寸回滚

信号：`icon-sizing`, `.width`, `.height`, `Image`, `vector drawable`, `android:width`, `git diff`

## 何时使用

结构收口阶段运行含图标尺寸自愈等会改写 .ets 的检测管线、决定是否接受其结果时；构建或验证阶段读到同一组件出现两组尺寸修饰时

## 适用情境

迁移管线在收口时自动运行图标尺寸自愈（icon-sizing 一类），会直接给 .ets 中的 Image 追加 .width/.height；页面 Image 已在同一行链式写好尺寸（如 '18vp'、'100%'），资源可能是 jpg 启动图标。也包括图标尺寸自愈按“媒体像素 ÷ 源密度”换算由 vector drawable 转来的 SVG，源 drawable 在无密度限定目录时回退到默认密度（如 3x），把图片写成约三分之一大小。

## 原因

自愈脚本读错图片像素时（本例追加值恰为 65535÷3 等异常值的折算，具体解析缺陷未核实），会在已定尺寸后追加上万的宽高；ArkUI 后写生效，组件铺满屏幕，编译与检测计数都不报错。来源中收口者只看 findings 计数和结果文件路径，没打开 icon 结果或 diff 就继续推进；之后构建代理读到这两行也只改了相邻属性。vector 转来的 SVG 尺寸已是 dp，没有密度桶可依；脚本按回退密度相除后直接写回代码，改动不易被察觉。

## 做法

1. 跑完会改写源码的自愈脚本后，先读其改动记录（结果 JSON）或 git diff，再看检测收敛结果；新增尺寸远超屏幕（上万 vp）或与同组件已有显式 width/height 重复时，回滚该处并上报。
2. 图标尺寸自愈只处理缺少尺寸的 Image；同一组件已有显式尺寸的跳过，读不出合法像素尺寸时不写入。
3. 构建或验证中读到同一组件出现两组 width/height 时，按后写生效核对最终尺寸，异常值当场删除或上报。
4. 图标尺寸自愈遇到 vector drawable 转来的 SVG 时不做 ÷density；源 drawable 不在密度限定目录时只报告、不写回。看到自愈结果时，用源 drawable 的 android:width/height 对照一次。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [纵向容器默认起始对齐与贴顶在目标显式写出](../../ui/layout/constraints/lesson-08b9064f678f1635e647.lesson.md)（共享 1 张卡）
- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../../ui/theme/sources/lesson-47785524c7f132ea7efe.lesson.md)（共享 1 张卡）
- [M3 组件默认几何与留白从库 Tokens 分侧取值](../../ui/theme/sources/lesson-5a82d62ff7e087616968.lesson.md)（共享 1 张卡）
- [Material 按钮区分布局占位、背景实绘与触控范围](../../ui/layout/intrinsic/lesson-b73a1ac8908f74856a02.lesson.md)（共享 1 张卡）
- [图标按资源固有 dp 显示，触摸盒放外层不设成盒尺寸](../../ui/graphics/icons/lesson-bdc493f5950835f9bfcc.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-500cf2e63e19988f0420](../../../../store/cases/case-500cf2e63e19988f0420/616fd28a8d66d19b0a16cf8321628b824302afc7e0c2337064550223b689ef08.json) · 结论：diagnosis, rec-78061a2f70, rec-85c1092e08, rec-ca963a5c0f
  卡片版本：`616fd28a8d66d19b0a16cf8321628b824302afc7e0c2337064550223b689ef08`
- [case-d54a9506e30031090325](../../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis, rec-146461d7c1
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
