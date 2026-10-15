# 整页 ScrollView 内 wrap_content WebView：高度首选 layoutMode(FIT_CONTENT)，自身不滚另行锁定

ID：`lesson-fd2dd522fdb03b3e5385` · 版本：3

[本主题](index.md)

## 何时使用

界面实现或对齐修复阶段，把整页滚动容器内的 wrap_content WebView 转换为 ArkWeb，确定 Web 高度与滚动归属时

## 适用情境

安卓 WebView layout_height=wrap_content，位于整页 ScrollView 内，加载含图片等后续资源的远程 H5；目标用 Scroll 包裹 Web，要求滚动全部交给外层页面。

## 原因

整页 ScrollView 以 UNSPECIFIED 测量子项，wrap_content WebView 的高度因此等于文档高度，文档级没有可滚范围；wrap_content 只是测量约束，H5 内 overflow 可滚的元素仍会自己滚。目标里 nestedScroll(PARENT_FIRST) 只决定父子滚动的先后，外层滚到边界后 Web 仍可内滚；onPageEnd 只触发一次，图片等后加载内容撑高文档后不会再测，固定高度或单次测高都会留下 Web 内部滚动区。

## 做法

1. 高度跟随首选 Web.layoutMode(WebLayoutMode.FIT_CONTENT)（API 11 起）配 nestedScroll，并按 web.d.ts 列出的限制判断能否采用：宽或高超过 7680 px 需创建时指定 RenderMode.SYNC_RENDER，创建后不能切换 layoutMode，不支持下拉加载更多的瀑布流页面，不能再用 height 属性改高度。
2. 不能用 FIT_CONTENT 时手动测高：为后加载内容安排复测或持续跟踪文档高度变化，取最大值更新高度，不只在 onPageEnd 测一次；写“多次自适应”一类注释前先核对事件语义。
3. Web 自身不滚另行落实：在 H5 侧锁定文档滚动（如注入脚本给 html/body 设 overflow:hidden），并查 H5 内部是否有 overflow 可滚元素、按源端行为处理；nestedScroll(PARENT_FIRST) 不能代替不自滚。

## 可选检查

- 真机把手指放在页底 Web 区域上下滑动，并在冷启动或图片晚到时检查 Web 是否单独位移、出现滚动条；某次加载恰好测准不能证明已等价于 wrap_content。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-a5865fd3dc0a3f9a028e](../../../store/cases/case-a5865fd3dc0a3f9a028e/cf0b7a96bcaebf83a4bce2e24faecced73414020d594df5e5c4be3b1640d3ba0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`cf0b7a96bcaebf83a4bce2e24faecced73414020d594df5e5c4be3b1640d3ba0`
