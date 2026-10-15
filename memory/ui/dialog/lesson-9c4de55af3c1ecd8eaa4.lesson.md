# 只靠平台默认外观的 AlertDialog（含 DialogPreference 弹出的偏好对话框）迁移前写出完整可见契约：标题字号色与标题线、消息、按钮条与按钮集合、框体、宽度规则与进出场从源主题的平台资源取值；按钮按角色核对槽位，要求一比一时用共享自定义弹窗复刻

ID：`lesson-9c4de55af3c1ecd8eaa4` · 版本：2

[本主题](index.md)

## 何时使用

规格提取阶段为源端系统对话框（代码中 AlertDialog.Builder 构造，或 PreferenceActivity 中 EditTextPreference、ListPreference 等点击弹出）写转换决策时，以及界面实现阶段按该决策落地 ArkUI 系统弹窗或自定义弹窗时

## 适用情境

源码用 AlertDialog.Builder 内联构造确认框，只设 title、message、setPositiveButton、setNegativeButton，无自定义布局或样式，外观由应用主题继承的平台默认警告框决定；目标准备用 ArkUI AlertDialog.show(primaryButton/secondaryButton) 等系统弹窗替代，项目要求与源端逐屏一致。 也包括应用主题为 Theme.Holo 等框架主题，多个对话框都由 Builder 或 DialogPreference 构造、没有自定义样式；规格只按经验摘要写了“标题左对齐、负左正右、遮罩、cancelable”几项，各页写者凭记忆或兄弟页先例自绘面板。

## 例外与边界

- 项目明确接受目标系统弹窗的固有外观、只要求文案与按键行为一致；此时仍按角色核对按钮槽位

## 原因

“正/负”是按钮角色，不是参数次序。ArkUI AlertDialog 把 primaryButton 放在左侧，自带居中标题、大圆角卡片、首字母大写的彩色按钮与全窗居中；来源中的安卓平台默认警告框是标题左对齐、按钮靠右且负键在左正键在右、全大写、小圆角，遮罩浓度与进出场取自平台主题。只写“系统组件 1:1/行为等价”时规格没有视觉契约，转换者照映射参考直接替换，版式与按钮顺序整体偏离。可见契约只写槽位与遮罩时，标题颜色与字号、标题分隔线、消息字号、按钮条、框体与宽度仍没有来源。另一应用（Theme.Holo）的四个对话框被写成白色 20fp 标题、无蓝线、圆角描边、320vp 封顶；偏好对话框被当作普通自定义弹窗，ListPreference 还漏了平台默认的 Cancel。

## 做法

1. 按源端实际使用的对话框类与应用主题定位平台样式（例如框架 android.app.AlertDialog 在 AppCompat Light 主题下取平台 Theme.Material.Light.Dialog.Alert，Theme.Holo 下取 Holo 对话框样式），从本机 SDK platforms/android-<api>/data/res 读取并写成数值契约：标题样式与 titleDivider（Holo 为 22sp #33B5E5 加 2dp 线）、消息字号、按钮条（分隔线、按钮字号、高度与大小写）、按钮排位、窗口背景（9-patch 或圆角）、宽度规则（windowMinWidthMinor/Major，Holo 竖 95%、横 65% 再减框体内边距）、遮罩浓度、显示位置、进出场，以及每个对话框的 setCancelable 与返回键行为；每项注明资源路径。
2. 映射按钮时先查目标弹窗把每个参数槽位放在哪一侧，再按角色和视觉位置决定正/负键放进哪个槽位。
3. 目标系统弹窗的固有版式与源端对不上而任务要求一比一时，规格直接决定用自定义弹窗（openCustomDialog 加自绘面板）复刻；实现阶段若规格只写了“系统弹窗 1:1”，先与源端截图或平台样式逐项比对，有差异就回报规格或改用自定义实现。
4. DialogPreference 弹出的对话框与代码构造的对话框同等写入契约：按钮集合按框架默认推导（DialogPreference 默认 OK/Cancel，XML 写了 positive/negativeButtonText 用字面值；ListPreference 去掉 positive、点项即写入并关闭、只留 negative），未写的按钮文案取平台 ok/cancel 字符串并按源端语言建多语言资源；内容布局取平台 preference_dialog_edittext、select_dialog_singlechoice_*；EditTextPreference 打开即聚焦并按 numeric/inputType 弹对应键盘。
5. 多个对话框共用同一平台外观时实现一个共享弹窗组件（标题区、可滚动消息、内容槽、按钮条、框体、宽度规则、进出场，cancelable 作参数），各页只传标题、消息、内容与回调；规格只写“按平台默认”而没有数值时，实现者先读平台资源或回报规格缺项，不凭记忆、兄弟页先例或魔法数字报告填值。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-8539606efd3a93a5fcb0](../../../store/cases/case-8539606efd3a93a5fcb0/af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a`
- [case-bee1ccf417ac7e3b453c](../../../store/cases/case-bee1ccf417ac7e3b453c/068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b`
- [case-ed0c3a60e7342aa867b4](../../../store/cases/case-ed0c3a60e7342aa867b4/72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715`
