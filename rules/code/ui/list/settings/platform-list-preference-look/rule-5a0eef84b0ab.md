# 自绘 Holo 偏好列表时，按平台几何写列表内边距、行高、分类头和分隔线规则

审的是：代码
触发（任一种）：
- 读到：android.preference.PreferenceActivity + Theme.Holo，res/xml 里有 PreferenceCategory 和多个偏好项；写错的样子：List 没有左右 16vp 内边距；每行后都画 divider（含分类头前）、末项后不画，或 List.divider 通栏；分类头 Medium 字重、不全大写、没有 2dp 底线；行内边距凭记忆写
适用范围：目标端没有 Preference 框架、逐行自绘 Holo 偏好列表时
做法：
- List 加 .padding({ left: 16, right: 16 })；行 .constraintSize({ minHeight: 64 })、左 8 右 10，文字列右 8，摘要 .maxLines(10)
- 分类头 Text 14fp、FontWeight.Bold、全大写、textColorSecondary 对应色，下方 2vp 线；行间分隔线 2px 白 15%，与分类头相邻不画、末项后画
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 返修按平台 preference_holo 重写后：行最小高 64、左右 8/10，两页 List 左右 16vp，分类头 14sp 粗体全大写带 2dp 线，分隔线与分类头相邻不画、末项后画：改后与源端一致的几何（出处：卡里修好并验证过）
- textCase(value: TextCase): TextAttribute；TextCase.UpperCase 全部大写：全大写的文本属性；声明没说明它对非 ASCII 字母是否按语言规则大写（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textCase；ets/component/enums.d.ts，TextCase.UpperCase）
- maxLines(value: number): TextAttribute：摘要的 android:maxLines="10"（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.maxLines）
未核实：卡里没写分类头全大写用的是 textCase 还是先转字符串；含非 ASCII 字母的语言下两者结果可能不同
来源：1 张卡，1 个应用
- case-a8bb009f2c5e1b854f32（Blockinger）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 诊断、建议 1；取值 1 ← 诊断
