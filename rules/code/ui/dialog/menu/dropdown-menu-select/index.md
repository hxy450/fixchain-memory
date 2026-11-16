# 下拉菜单式的选择项（ListPreference 的 DROPDOWN_MENU、DropdownMenu）

agent 会看到什么：读到源端 ListPreference(type = ListPreferenceType.DROPDOWN_MENU) 或 DropdownMenu 从所在行弹出选项菜单；产物里是锚在该行的 bindMenu / Select，还是点击切 expanded、在行下插入选项列表的行内展开

## 规矩

- rule-68fa1bbc2ba6｜ListPreference(DROPDOWN_MENU) 映射为锚在该行的 bindMenu 菜单，不写成行内展开｜读到：ListPreference(type = ListPreferenceType.DROPDOWN_MENU)，规格映射为 Select；写错：目标写成点击切换 expanded、在行下方插入选项列表的行内展开（带 chevron_up / chevron_down），沿用了别的页面 ReadOnlyDropdown 式的先例
