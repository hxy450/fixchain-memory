# 平台默认外观的 AlertDialog 迁移前按对话框样式的 layout 与面板资源写可见契约：按钮按角色核槽位，返回键与点外部两条取消路径分别核对

ID：`lesson-9c4de55af3c1ecd8eaa4` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段为代码中 AlertDialog.Builder 构造的系统对话框写转换决策时，以及界面实现阶段按该决策落地 ArkUI 系统弹窗或自定义弹窗时

## 适用情境

源码用 AlertDialog.Builder 内联构造确认框，只设 title、message、setPositiveButton、setNegativeButton（可有 setView），无自定义样式，外观由主题的平台默认警告框决定；目标准备用 ArkUI AlertDialog.show(primaryButton/secondaryButton) 等系统弹窗替代，项目要求与源端逐屏一致。也包括应用主题为 Theme.Holo 等框架主题，多个对话框共用同一平台外观；规格只写了“标题左对齐、负左正右、遮罩、cancelable”几项，或把取消方式写成“仅返回键可关闭”，各页写者凭记忆或兄弟页先例自绘面板；源端会同时叠放多个对话框。

## 例外与边界

- 项目明确接受目标系统弹窗的固有外观、只要求文案与按键行为一致；此时仍按角色核对按钮槽位
- android.preference 偏好页弹出的 DialogPreference/ListPreference 对话框：外观契约同本条，按钮集合、内容布局与提交语义另按偏好框架默认推导，见 lesson-3f95e9d0ad81b3c431e9

## 原因

“正/负”是按钮角色，不是参数次序。ArkUI AlertDialog 把 primaryButton 放在左侧，自带居中标题、大圆角卡片、首字母大写的彩色按钮与全窗居中；安卓平台默认警告框随主题而异（例：AppCompat Light 主题下的框架 Material 警告框为标题左对齐、按钮靠右且负左正右、全大写、2dp 圆角），遮罩浓度与进出场取自平台主题。主题文件只给对话框样式的入口，按钮排位与面板底色在样式指向的布局与 drawable 里；点外部取消由对话框主题决定，与返回键是两条独立路径；多个对话框叠放时窗口层遮罩只暗一次。只写“系统组件 1:1/行为等价”或只写槽位与遮罩时，标题颜色与字号、标题分隔线、消息字号、按钮条、框体与宽度都没有来源，各页写者只能凭记忆或兄弟页先例补值。

## 做法

1. 先按实际对话框类、构造时的 Context 与 themeResId、主题的 alertDialogTheme 定位提供方，没有覆盖时才取平台默认样式（例：框架 android.app.AlertDialog 在 AppCompat Light 主题下取 Theme.Material.Light.Dialog.Alert，Theme.Holo 下取 Holo 对话框样式；androidx 或 MDC 的 MaterialAlertDialogBuilder 取库资源，见 lesson-39077e6612d5f97b0731）。
2. 从本机 SDK platforms/android-<api>/data/res 读取并写成数值契约，每项注明资源路径。主题文件 themes_*.xml 只给 alertDialogStyle 等入口：按钮先后、等分还是靠右、大小写与面板底色取该样式 layout 属性指向的布局（如 layout/alert_dialog_holo.xml 中 buttonPanel 各按钮的顺序、layout_gravity、layout_weight）与 fullDark/topDark 等面板 drawable，遮罩浓度取主题 backgroundDimAmount；另列标题样式与 titleDivider、消息字号、按钮条（分隔线、字号、高度）、窗口背景（9-patch 或圆角）、宽度规则（windowMinWidthMinor/Major，即 dimens.xml 的 dialog_min_width_minor/major，再减框体内边距）、显示位置与进出场。例：Holo 标题 DialogWindowTitle.Holo 为 22sp #33B5E5 加 2dp titleDivider，宽度竖屏 95%、横屏 65%；框架 Material 对话框圆角为 dialog_corner_radius 2dp。来源冲突时只认带资源文件或行号回执的结论；只读了主题文件就写槽位，或凭“哪一代平台改过按钮顺序”的记忆裁定，都回到布局文件核对。
3. 取消契约分两条写：返回键（setCancelable，未调用时为 true）与点窗口外部（Dialog.setCanceledOnTouchOutside；未调用时沿对话框主题 parent 链取 windowCloseOnTouchOutside，再到 values/config.xml 解析它引用的 config_closeDialogWhenTouchOutside）。除非源码显式关闭，不写“仅返回键可关”；页内遮罩复刻时，遮罩点击与返回键走同一个“关闭最上层”处理，源端不可取消时才吞掉点击。
4. 映射按钮时先查目标弹窗把每个参数槽位放在哪一侧，再按角色和视觉位置决定正/负键放进哪个槽位。
5. 目标系统弹窗的固有版式与源端对不上而任务要求一比一时，规格直接决定用自定义弹窗（openCustomDialog 加自绘面板）复刻；实现阶段若规格只写了“系统弹窗 1:1”，先与源端截图或平台样式逐项比对，有差异就回报规格或改用自定义实现。
6. 多个对话框共用同一平台外观时实现一个共享弹窗组件（标题区、可滚动消息、内容槽、按钮条、框体、宽度规则、进出场，cancelable 作参数），各页只传标题、消息、内容与回调；面板组件只画面板，契约里每个区的底色都落到容器上。规格只写“按平台默认”而没有数值时，实现者先读平台资源或回报规格缺项，不凭记忆、兄弟页先例或魔法数字报告填值。
7. 源端会同时叠放多个对话框时，变暗是窗口层效果、只暗一次：由宿主统一画一层遮罩，浓度取主题 backgroundDimAmount，叠放与关闭顺序由宿主管理。

来源支持：7 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-20015832edaeb45f53bb](../../../store/cases/case-20015832edaeb45f53bb/c5b354b6bb37ff1dccf5f009e901cc7aa26ff2d922b0dd77dda899f9632e66a4.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`c5b354b6bb37ff1dccf5f009e901cc7aa26ff2d922b0dd77dda899f9632e66a4`
- [case-21e1e83afaa8d814dc37](../../../store/cases/case-21e1e83afaa8d814dc37/ca414833340bf1b9bc1cc58bf84fee86761e2d34439da34c71d729729161668a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ca414833340bf1b9bc1cc58bf84fee86761e2d34439da34c71d729729161668a`
- [case-8539606efd3a93a5fcb0](../../../store/cases/case-8539606efd3a93a5fcb0/af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a.json) · 结论：diagnosis, recommendation:4
  卡片版本：`af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a`
- [case-bee1ccf417ac7e3b453c](../../../store/cases/case-bee1ccf417ac7e3b453c/068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b`
- [case-dadda7b6820516f5f415](../../../store/cases/case-dadda7b6820516f5f415/550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b.json) · 结论：recommendation:7
  卡片版本：`550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b`
- [case-ed0c3a60e7342aa867b4](../../../store/cases/case-ed0c3a60e7342aa867b4/72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715`
- [case-fe1caa813d814978decf](../../../store/cases/case-fe1caa813d814978decf/bb305d041d425a8b483114db46cb3c1ee12f6182a6539259a9fd9aeb76c8c0cf.json) · 结论：recommendation:1
  卡片版本：`bb305d041d425a8b483114db46cb3c1ee12f6182a6539259a9fd9aeb76c8c0cf`
