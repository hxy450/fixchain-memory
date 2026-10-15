# 源弹窗由独立布局 XML 或弹窗工具函数加载时，按实际布局与函数全文逐控件还原，不以行为代码、相邻弹窗外壳或通用确认弹窗代替

ID：`lesson-1f366fe4ccdc917ce0fc` · 版本：8

[本主题](index.md)

## 何时使用

界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、补齐流程闭环时新建弹窗、考虑复用通用弹窗）时；规格提取阶段整理页面弹窗清单时

## 适用情境

源弹窗由 ViewBinding/inflate 或工具类（如 DialogHelper.showXxx）加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、说明文字、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照，或只拿到“展示、复制、关闭”一类功能描述。

## 例外与边界

- 源弹窗由依赖库按配置对象渲染、工程里没有布局文件时按 lesson-afc5868d6c1a6dec04fa 处理，不适用本条的逐控件对照

## 原因

只读调用代码、功能描述或 toast 文案会漏掉布局里的控件：关闭图标被写成“取消”按钮、单按钮变双按钮、标题与图标缺失、hint 取自 toast；截断的 grep/head 读不到函数结尾的失败与拒绝分支，会把“源端无提示”当成事实。通用确认弹窗缺任何一项都不等价，却会被注成“视觉由通用弹窗承载”后解除标记。

## 做法

1. 从调用代码定位实际加载的布局（XxxBinding.inflate → xxx.xml、setContentView/inflate 的 R.layout 名，或弹窗工具函数里的布局名），读完该 XML 与弹窗函数全文（输出被截断就继续读，拿到目标内容再写）；工程提供弹窗 probe 时用其控件清单。
2. 按源布局逐控件核对：标题文案、图标、正文与说明、按钮数量与文案、每个按钮的回调分支（如拒绝 → 二次确认 → 退出）、关闭控件类型与位置、遮罩点击行为，hint 取 android:hint；每个容器自身的 layout_margin/padding 与子控件属性分开检查；文案与图标引用源弹窗自己的资源，不借用其他页面的字符串。
3. 通用弹窗缺少任一项时不作为等价实现；公共组件不在写权限内时，在页面内用条件浮层复刻，确实做不到就登记未决项并写明缺口。
4. 布局里的可点击复合确认区（勾选或图标加多行文案）按复合按钮整体转换，写法见 lesson-f7f9b40bf3d0e1b62d1f。
5. 规格提取阶段整理弹窗清单时，把经工具方法触发的主弹窗与其确认弹窗一并登记到父页面契约，写明布局、图标资源和按钮分支。

来源支持：5 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-89e7732b8a374944c6b2](../../../store/cases/case-89e7732b8a374944c6b2/810639d11dab94e726e28bbf772da715ae79949171acbf4ea64889179116cb69.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`810639d11dab94e726e28bbf772da715ae79949171acbf4ea64889179116cb69`
- [case-91f8e7d157380a2457fa](../../../store/cases/case-91f8e7d157380a2457fa/8a4c1a540d46c44dc344bf09c6d3da044f8195e0bfe2f99609096816d6dd39f8.json) · 结论：recommendation:2
  卡片版本：`8a4c1a540d46c44dc344bf09c6d3da044f8195e0bfe2f99609096816d6dd39f8`
- [case-ae1e7b09c5cfe5214cd2](../../../store/cases/case-ae1e7b09c5cfe5214cd2/330b086d78a6625e9a9a7fa9cdcd53c10d3ecfef919ec81b12a73fcae4c061c4.json) · 结论：diagnosis, recommendation:1
  卡片版本：`330b086d78a6625e9a9a7fa9cdcd53c10d3ecfef919ec81b12a73fcae4c061c4`
- [case-d5caf639de4ba1e70e28](../../../store/cases/case-d5caf639de4ba1e70e28/aad7cc6e4136641bd8650afd37bf490a21d6d2f71fcbafdb80a0f351bf46b3b7.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`aad7cc6e4136641bd8650afd37bf490a21d6d2f71fcbafdb80a0f351bf46b3b7`
- [case-f62209d059dec8e6aca4](../../../store/cases/case-f62209d059dec8e6aca4/1a18e9b5dfbae66db4693b94563e6ad2a12b31a37a4e5e77f33b0299d6effed1.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`1a18e9b5dfbae66db4693b94563e6ad2a12b31a37a4e5e77f33b0299d6effed1`
