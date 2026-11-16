# 规格描述带回调的联动流程时，写明每一步的落值时刻与失败分支

审的是：规格
触发（任一种）：
- 读到：源码 onPreferenceChange 返回 true（新值立即生效），随后才调验密弹窗，成功再设同值；写错的样子：验收条目写成「SUCCEED 才真正切换、验密失败后开关回弹原位」，与源码顺序相反；没写每一步的落值时刻和失败分支
适用范围：规格提取阶段描述带回调的开关、确认、验证联动流程的验收条目
做法：
- 验收条目按源顺序写每一步的落值时刻和失败分支，如「返回 true 即落值并持久化（立即生效）；验密是事后补偿；失败、取消不回滚」
- 把源文件与方法位置和「立即生效 / 事后补偿」字样一起写进验收条目
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onPreferenceChange 返回 true 表示用新值更新 Preference 的状态，调用发生在持久化之前：源端新值立即生效（出处：android.preference.Preference.OnPreferenceChangeListener#onPreferenceChange）
来源：1 张卡，1 个应用
- case-a293ed8cf3fa860f8330（omni-notes-hmos）：做法第 1 步 ← 建议 6；做法第 2 步 ← 建议 6
