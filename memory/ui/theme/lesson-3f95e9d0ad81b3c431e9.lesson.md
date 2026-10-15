# android.preference 偏好页的列表行、分类头、行内控件与偏好对话框按平台资源和框架默认行为复刻

ID：`lesson-3f95e9d0ad81b3c431e9` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，迁移继承 PreferenceActivity/PreferenceFragment（android.preference，无自定义布局）的设置页，确定行几何、分类头、分隔线与行内控件，以及 EditTextPreference、ListPreference 等点击弹出的对话框时

## 适用情境

页面由 addPreferencesFromResource 挂载，没有布局 XML；复选框、分类头、行高与内边距、列表左右内边距、分隔线规则、点击弹出的对话框都由平台 preference_holo/preference_material 等布局与资源隐式提供；代码中看不到 AlertDialog.Builder，规格却把 ListPreference 写成 Select、bindSheet 或“选项单”，或把行内控件写成 Toggle、带尾部箭头的通用列表行，或用估计内距与目标平台 sys 色。

## 例外与边界

- AndroidX Preference（PreferenceFragmentCompat）或带自定义 layout/widgetLayout 的偏好：按库资源与应用布局取值，本条的平台几何不适用

## 原因

偏好页的外观与对话框都由框架生成，应用代码里看不到；按通用设置页控件迁移会改掉行几何、分类头样式与控件类型（CheckBoxPreference 是方形复选框，不是开关），把偏好对话框当普通弹窗会改掉按钮集合与提交语义（ListPreference 没有确定钮、点项即写入）。这些值在本机 SDK 平台资源与源码里可查，用估计值或目标平台 sys 色代替会整体偏离。

## 做法

1. 按主题取平台偏好布局写进规格：Theme.Holo 读 platforms/android-<api>/data/res/layout/preference_holo.xml、preference_category_holo.xml，Material 读 preference_material.xml 与 values/dimens_material.xml，连同相关 drawable，写出列表左右内边距、行最小高度、文字列内边距、标题与摘要字号、摘要 maxLines、分类头样式与分隔线规则（例：android-36.1 中 preference_holo.xml 的行最小高度取 Theme.Holo 的 listPreferredItemHeight 64dip、摘要 maxLines 10，分类头为 listSeparatorTextViewStyle 的 14sp 粗体全大写加 2dp 底线（list_section_divider_holo_dark），列表左右 16dp；preference_material.xml 的行 minHeight 取 listPreferredItemHeightSmall 48dip、左右 16dp、文字区上下 16dp、title 16sp、summary 14sp）。
2. 分隔线全宽、末项后也画，Holo 下与分类头相邻时不画；颜色取主题 listDivider 的实际资源，不用目标平台 sys 色。
3. 行内控件按偏好类型落实：CheckBoxPreference 用方形复选框（平台多态图），SwitchPreference 的开关不单独接收点击、由整行切换；SeekBarPreference 按源布局叠放数值与 SeekBar；带 icon 的 Preference 只有图标框与标题，没有尾部箭头；源端没有的元素不补。
4. DialogPreference（EditTextPreference、ListPreference、MultiSelectListPreference）弹出的是平台默认 AlertDialog：外观按平台对话框契约复刻（遮罩、卡宽、圆角、标题、单选圆环，见 lesson-9c4de55af3c1ecd8eaa4），不写成 Select、bindSheet 或目标平台卡片样式，单选圆环不用 ArkUI Radio 默认样式；内容布局取平台 preference_dialog_edittext、select_dialog_singlechoice_*。多个偏好对话框与代码构造的平台对话框共用同一个共享弹窗组件，输入框、单选列表做成内容槽。
5. 按钮集合按框架默认推导：DialogPreference 默认 OK/Cancel（android-36.1 styles.xml 的 Preference.DialogPreference 为 @string/ok、@string/cancel），XML 写了 positive/negativeButtonText 用字面值；ListPreference 在 onPrepareDialogBuilder 中 setPositiveButton(null, null) 去掉确定钮、保留 negative（未设 negativeButtonText="@null" 时为平台 cancel），取消路径为 CANCEL、点外与返回；未写的按钮文案取平台 ok/cancel 字符串，并按源端支持的语言建多语言资源。
6. ListPreference 点项即按确定处理并关闭对话框，关闭后的 onDialogClosed 中先 callChangeListener(新值)，返回 true 才 setValue 写入（sources/android-36.1 android/preference/ListPreference.java）；源端注册了 OnPreferenceChangeListener 或自定义子类覆写时保留其拒绝写入的分支。EditTextPreference 打开即聚焦（如 onAppear 中 requestFocus）并按 numeric/inputType 弹对应键盘，点 OK 写入原串，Cancel 或点外不写入。

来源支持：5 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-01ea7d8b923cd659dbba](../../../store/cases/case-01ea7d8b923cd659dbba/47a9f8cf52b0f7110a910cabd68145e781df2e4650e126db023c482fd2521561.json) · 结论：diagnosis
  卡片版本：`47a9f8cf52b0f7110a910cabd68145e781df2e4650e126db023c482fd2521561`
- [case-8539606efd3a93a5fcb0](../../../store/cases/case-8539606efd3a93a5fcb0/af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:5, recommendation:4
  卡片版本：`af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a`
- [case-a8bb009f2c5e1b854f32](../../../store/cases/case-a8bb009f2c5e1b854f32/2ad5b75a8506d9f60b20e5c1cf933e2abfb9372026badeeaf0e7ac0f6e07659a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:5
  卡片版本：`2ad5b75a8506d9f60b20e5c1cf933e2abfb9372026badeeaf0e7ac0f6e07659a`
- [case-dadda7b6820516f5f415](../../../store/cases/case-dadda7b6820516f5f415/550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b.json) · 结论：recommendation:7, recommendation:5, recommendation:2
  卡片版本：`550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b`
- [case-fe1caa813d814978decf](../../../store/cases/case-fe1caa813d814978decf/bb305d041d425a8b483114db46cb3c1ee12f6182a6539259a9fd9aeb76c8c0cf.json) · 结论：diagnosis, recommendation:1
  卡片版本：`bb305d041d425a8b483114db46cb3c1ee12f6182a6539259a9fd9aeb76c8c0cf`
