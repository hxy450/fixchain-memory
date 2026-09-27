# 源弹窗按它实际加载的布局 XML 与函数全文逐控件还原，不以行为代码、相邻弹窗外壳或通用确认弹窗代替

ID：`lesson-1f366fe4ccdc917ce0fc` · 版本：1

[本主题](index.md)

## 何时使用

界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、考虑复用通用弹窗）时

## 适用情境

源弹窗由 ViewBinding/inflate 加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照。

## 原因

只读调用代码或 toast 文案会漏掉布局里的控件：关闭图标被写成“取消”按钮、单按钮变双按钮、标题与图标缺失、hint 取自 toast；截断的 grep/head 读不到函数结尾的失败分支，会把“源端无提示”当成事实。通用确认弹窗缺任何一项都不等价，却常被注成“视觉由通用弹窗承载”后解除标记。

## 做法

1. 从调用代码定位实际加载的布局（XxxBinding.inflate → xxx.xml、setContentView/inflate 的 R.layout 名），读完该 XML 与弹窗函数全文（被截断就继续读）再写。
2. 按源布局逐控件核对：标题文案、图标、正文、按钮数量与文案、关闭控件类型、遮罩点击行为，hint 取 android:hint；每个容器自身的 layout_margin/padding 与子控件属性分开检查。
3. 通用弹窗缺少任一项时不作为等价实现；公共组件不在写权限内时，在页面内用条件浮层复刻，确实做不到就登记未决项并写明缺口。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-89e7732b8a374944c6b2 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ea957e3dd6e31c5c5819e209e293add0c7624cb66aa6c1ba2d36eb87da7bd3f4`
- case-91f8e7d157380a2457fa · 结论：recommendation:2
  卡片版本：`63a1df91953a84392576c2bcd0d96e81fc5cb6819a5d932ed630aba4896e9cb1`
- case-d5caf639de4ba1e70e28 · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`3e13cfc20d6d4935b5840ccd818318d4b125224c3eeaead04471ced30ff53cf2`
