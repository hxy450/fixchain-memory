# CheckBox、RadioButton 和单选列表行

agent 会看到什么：读到带 android:text 的 CheckBox / RadioButton、RadioGroup，或 setSingleChoiceItems / ListPreference 的单选列表；产物里 Checkbox / Radio 加 Text 的行的可点范围和选中样式

## 规矩

- rule-434e0aa8c96b｜Checkbox/Radio 另配 Text 时，外层统一 onClick，框设 HitTestMode.None｜读到：CheckBox / RadioButton 带 android:text，或代码里 setText(...)，文字本身属于可点控件；写错：目标写成 Row { Checkbox(); Text(...) } 或 Row { Radio(); Text(...) }，Text 和外层容器都没有 onClick，只有方框或圆环可点
- rule-e89f346d3c5f｜带文字的 CheckBox/RadioButton 按源宽度定可点范围，折行的 layoutWeight 不扩命中区｜读到：XML 里带 android:text 的 CheckBox / RadioButton，layout_width 为 wrap_content（无 layout_toLeftOf），或 match_parent、alignParentLeft + toLeftOf 两端锚定；写错：wrap_content 项的 Text 写 .layoutWeight(1).onClick(...) 或整行 Row 挂 onClick；match_parent 项只有框和文字可点
- rule-ecac931616ce｜RadioButton 或单选列表译成 Radio 时，用 indicatorType CUSTOM 画外环加圆点｜读到：RadioButton，或 AlertDialog.Builder.setSingleChoiceItems 单选列表，Material 下选中态是外环加圆点；写错：Radio({ value, group }) 只设 .radioStyle({ checkedBackgroundColor, uncheckedBorderColor })，没写 indicatorType
- rule-a35c03e8ea12｜框架单选对话框的行按 Material 样式自绘圆环、行高 48，不用鸿蒙 Radio 默认样式｜读到：源端单选列表来自框架 select_dialog_singlechoice_material（ListPreference 的 setSingleChoiceItems），圆环是 ?attr/listChoiceIndicatorSingle（btn_radio_material_anim）；写错：目标单选行用 Radio({ group, value }) 加 .radioStyle(...)，行高、字号按估值（行上下 14、16 号）
