# 由 Material 库组件内部布局提供的留白要分侧写出，不把单侧 token 扩成对称 padding

ID：`lesson-f648d0ae072e9bcf83c3` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为源侧由 Material 组件内部布局（而非源码显式 modifier）决定的留白确定 ArkUI padding 时；规格提取阶段写入同一组件的 M3 默认值时

## 适用情境

源是 Compose Material3 TopAppBar / IconButton 等库组件，标题槽内是 Row { Text(weight 1) + IconButton }，源码本身没有 padding 修饰符；库的内部留白（TopAppBarTitleInset、导航/动作槽宽度）需要实现者自行补出；spec 只写了容器高度等部分 M3 默认值。

## 原因

converter 在 spec、源码、合成 view.xml 都没有横向留白的情况下自行补 M3 内部留白，注释写明「TopAppBarTitleInset = 16dp」（起始侧 token）却应用成 `.padding({ left: 16, right: 16 })`，末端多 16vp，箭头离右缘 28vp（Android 12dp）。

## 做法

1. 按该库的布局规则分侧写出：哪一侧有 inset、由什么槽位撑开；不要把单侧 token 扩成对称 padding。
2. 补库内部留白后用 Android dump/截图核一次两端元素与屏缘的距离；没有 dump 至少在注释里写清该值来自哪条库规则、作用于哪一侧。
3. 规格提取若已写入 M3 默认值（如容器高 64dp），把同一组件的标题 inset / 槽位规则一并写出。

## 检查

- Android dump 里尾部 IconButton 右缘与屏缘距离（如 1080−1048=32px=12dp）与目标端一致。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-2280cf8a2bf7682ff26b](../../../../store/cases/case-2280cf8a2bf7682ff26b/fb66b756db6239a68a90d290915c7f952fb80cf460b3c14484bb91ab77ace622.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fb66b756db6239a68a90d290915c7f952fb80cf460b3c14484bb91ab77ace622`
