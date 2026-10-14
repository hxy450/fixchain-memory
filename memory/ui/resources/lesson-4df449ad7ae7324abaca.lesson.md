# 迁移9-patch背景时保留拉伸区和内容内边距

ID：`lesson-4df449ad7ae7324abaca` · 版本：1

[本主题](index.md)

## 何时使用

资源转换、派工与界面实现阶段，迁移.9.png背景并交代其绘制方式时

## 适用情境

源以.9.png作容器背景，四边1px标记定义拉伸区与内容内边距；资源可能位于drawable-nodpi，按物理像素绘制。

## 原因

只裁掉标记边存成普通png，拉伸区和内边距信息就丢了，下游只能整图拉伸或猜切线；整图拉伸会把边框与圆角一起放大，文字贴边。

## 做法

1. 资源转换时从上/左标记读出拉伸区，从下/右标记读出内容区内边距，连同密度目录写进资源映射，再输出去标记位图。
2. 派工写明“9-patch背景”及切线、内边距和密度目录，不只给文件名。
3. 实现时：无需按物理像素保留四角时，可用backgroundImageResizable的slice/lattice（按vp计量）；nodpi需要按物理像素保留四角时，用px单位Canvas按切线分9块绘制；同时给容器加内容内边距。
4. 只拿到资源名时，先在源各drawable目录查实际文件；是.9.png就不用ImageSize.FILL整图拉伸。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4869da5358a4a82f70a6](../../../store/cases/case-4869da5358a4a82f70a6/535c159f3832abceea24fd48cd04be0ad96c12c83d2648ee7b871bc7316b1d21.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`535c159f3832abceea24fd48cd04be0ad96c12c83d2648ee7b871bc7316b1d21`
