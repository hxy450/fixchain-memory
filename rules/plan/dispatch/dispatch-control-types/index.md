# 派工补充里改写的控件类型

agent 会看到什么：已审规格写了控件映射（如 CheckBoxPreference → Row + Checkbox），编排者的派工补充写成「CheckboxPreference→Toggle」「→箭头行」，和已审规格不一致

## 规矩

- rule-0616f84a5cc3｜编排者写派工补充前先读已审规格，不在派工里改写规格定下的控件类型｜读到：已审规格写 CheckBoxPreference → Row + Checkbox；源 XML 的带图标 Preference 没有箭头；写错：派工写「CheckboxPreference→Toggle」「→箭头行」「PreferenceActivity → Column+Row+Toggle/Slider/TextInput 复刻」，与已审规格的控件类型不一致
