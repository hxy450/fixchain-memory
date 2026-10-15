# 修复点击或滑动无响应前先在设备复现并分层定位，确认触摸可达再改约束；修复前已存在的字符串不作 RED/GREEN 依据

ID：`lesson-afae8d13e00941efe808` · 版本：5

[本主题](index.md)

## 何时使用

缺陷修复阶段，修复“点击没有反应”“滑不动”一类交互问题、决定改哪一层并选择回归验证方式时

## 适用情境

页面菜单项、按钮已绑定 onClick 却点击无效；或弹层、卡片内一片控件全部不响应点击或滑动，候选原因同时有祖先节点的命中测试设置（hitTestBehavior）与滚动容器的尺寸约束；设备可连接，但 UI 测试可能在启动 Ability 阶段超时，修复者考虑用 grep 结构契约代替设备断言。

## 原因

没有复现就按猜测改容器，再用修复前已存在的字符串做契约，改前改后都会通过，“已修复”的结论没有依据。HitTestMode.Block 会让整棵子树失去触摸响应，表现与尺寸约束错误相同；同时改几处时，修好后会把效果记到错误的改动上，形成错误经验。

## 做法

1. 修复前先在设备复现并分层定位：用 uitest 点击（hdc shell uitest uiInput click x y）后 dumpLayout，确认是菜单未弹出、点击未命中还是回调未改状态，再决定改哪一层。
2. 一片区域内控件全部不响应时，先点其中一个可点控件确认触摸能否到达，并检查祖先节点的 hitTestBehavior（HitTestMode.Block 会阻断子节点）；确认可达后再调整尺寸约束。每次只改一处并复测，记录是哪一处改动让行为恢复。
3. UI 测试被环境问题阻断时，改用 uitest 点击 + dumpLayout 做设备断言（点击后标题、日期等可见状态的变化）；修复前已存在的源码字符串在修复前后都会通过，不作 RED/GREEN 依据；设备断言做不了就按未验证交付，不写成已修复。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-30d42aa2ba7c8354db17](../../../store/cases/case-30d42aa2ba7c8354db17/caedcf037b4f51f56e370b09f5e18559d3a5abf76c513a88e701ad9ca342fe0f.json) · 结论：diagnosis, recommendation:1
  卡片版本：`caedcf037b4f51f56e370b09f5e18559d3a5abf76c513a88e701ad9ca342fe0f`
- [case-845bfd8c093e7d531cd4](../../../store/cases/case-845bfd8c093e7d531cd4/de7ca71b50e7ddcbe58900c12dc2a828e9fac7d95169a90f773c3a2b7d6b43b6.json) · 结论：diagnosis, recommendation:3
  卡片版本：`de7ca71b50e7ddcbe58900c12dc2a828e9fac7d95169a90f773c3a2b7d6b43b6`
- [case-e5d42507c82fd492f62b](../../../store/cases/case-e5d42507c82fd492f62b/8893472b8fe96d909e01764d81865f80681f137f4e7482c990f84f36d5924130.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`8893472b8fe96d909e01764d81865f80681f137f4e7482c990f84f36d5924130`
