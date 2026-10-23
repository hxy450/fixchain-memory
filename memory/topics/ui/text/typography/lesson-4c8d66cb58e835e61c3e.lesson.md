# Android 小部件布局迁成 ArkTS 服务卡片时，字号与图标按源 sp/dp 等值落 fp/vp，不按 designWidth 放大

ID：`lesson-4c8d66cb58e835e61c3e` · 版本：1 · 阶段：execute · 主题：[ui/text/typography](index.md)

概要：卡片字号图标按源 sp/dp 等值，不放大

信号：`appwidget-provider`, `textSize`, `drawableTop`, `designWidth`, `autoDesignWidth`, `form_config`, `fontScaleFollowSystem`, `layoutWeight`

## 何时使用

服务卡片实现阶段，把 Android 小部件布局（textSize、drawableTop 图标、wrap_content）转换为 ArkTS 卡片页面，确定文字与图标尺寸时

## 适用情境

源小部件布局以 sp 写字号、以 drawableTop 或 ImageView 放图标，并按 wrap_content、match_parent 随格子尺寸排布，appwidget-provider 只给最小尺寸；目标 ArkTS 卡片的 form_config 可能带 window.designWidth（缺省 720），规格未给卡片元素尺寸。

## 例外与边界

- 当前规格或已批准的设计明确给出卡片元素尺寸时，按其实现

## 原因

form_config 的 window 标签（designWidth、autoDesignWidth）只对 JS 卡片生效，ArkTS 卡片的 vp、fp 不经它缩放，卡片字体还默认随系统字号变化（fontScaleFollowSystem 缺省 true）（OpenHarmony 文档 application-dev/form/arkts-ui-widget-configuration.md，master，访问于 2026-10-23）。按 designWidth 推测源值“太小”而成倍放大字号，再给图标写固定的大 vp 宽高，在较小规格的卡片里会挤压或截断文字。

## 做法

1. 字号按源 sp 等值写 fp（textSize=Nsp → fontSize(N)，默认单位 fp），dp 尺寸等值写 vp；不按 designWidth 或设计稿宽度自行换算。
2. 源图标随格子 wrap_content 排布时不写固定的大 vp 宽高：文字取固有高度，图标 width('100%') 加 layoutWeight(1) 占剩余空间并 objectFit(ImageFit.Contain)；源端给出图标 dp 尺寸时按该尺寸等值写 vp。

## 可选检查

- 对尺寸仍有疑问时，在 supportDimensions 中最小的规格上预览，确认文字完整。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [跨文件补实现的功能登记带负责方与验证的移交项](../../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）
- [一次性拍照请求在相机就绪回调消费，不用页面显示](../../../app/camera/session/lesson-e3bf30ce225c1c8964aa.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-9720ed67e580c21dbd65](../../../../../store/cases/case-9720ed67e580c21dbd65/e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602.json) · 结论：diagnosis
  卡片版本：`e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602`
