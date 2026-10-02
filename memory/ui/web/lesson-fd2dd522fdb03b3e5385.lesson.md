# 整页 ScrollView 内的 wrap_content WebView 转 ArkWeb：分别实现“高度跟随文档”和“Web 自身不滚”，锁 H5 滚动并对后加载内容复测

ID：`lesson-fd2dd522fdb03b3e5385` · 版本：1

[本主题](index.md)

## 何时使用

界面实现或对齐修复阶段，把整页滚动容器内的 wrap_content WebView 转换为 ArkWeb，确定 Web 高度与滚动归属时

## 适用情境

安卓 WebView layout_height=wrap_content，位于整页 ScrollView 内，加载含图片等后续资源的远程 H5；目标用 Scroll 包裹 Web，要求滚动全部交给外层页面。

## 原因

wrap_content 同时意味着高度等于内容、Web 不消费滚动。nestedScroll(PARENT_FIRST) 只决定父子滚动的先后，外层滚到边界后 Web 仍可内滚；onPageEnd 只触发一次，图片等后加载内容撑高文档后不会再测，固定高度或单次测高都会留下 Web 内部滚动区。来源中修复者读到了源布局并自述“自身永不内滚”，首轮只在 onPageEnd 测一次高并设 PARENT_FIRST，注释称会多次触发；用户随后报告资讯区单独滑动、有滚动条，第二轮加锁滚动与多次复测才解决（竞态时序为修复者推断）。

## 做法

1. 把两条约束分别实现：高度取文档高度并随内容变化更新；同时在 H5 侧锁定滚动（如注入脚本给 html/body 设 overflow:hidden）或用其他方式关闭 Web 自身滚动。nestedScroll(PARENT_FIRST) 不能代替不自滚。
2. 用 onPageEnd + scrollHeight 测高时，为后加载内容安排复测（如 0/1000/2500ms 取最大值）或持续跟踪；写“多次自适应”一类注释前先核对事件语义。

## 可选检查

- 真机把手指放在页底 Web 区域上下滑动，并在冷启动或图片晚到时检查 Web 是否单独位移、出现滚动条；某次加载恰好测准不能证明已等价于 wrap_content。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-a5865fd3dc0a3f9a028e](../../../store/cases/case-a5865fd3dc0a3f9a028e/cf0b7a96bcaebf83a4bce2e24faecced73414020d594df5e5c4be3b1640d3ba0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`cf0b7a96bcaebf83a4bce2e24faecced73414020d594df5e5c4be3b1640d3ba0`
