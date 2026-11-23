# onPreferenceChange 返回 true 即接受并持久化新值：其中发起的验证按源顺序先落值再补偿，取消不回滚

## 何时使用

设置页实现阶段，把 Preference 的 onPreferenceChange 监听（含其中发起的验密、确认弹窗）翻译成目标开关回调时；规格提取阶段描述这类联动流程时

## 适用情境

源端在 onPreferenceChange 里发起异步验证后立即 return true，验证成功的回调只做补偿动作（如再次 setChecked 同值），取消没有回滚分支；目标用受控 Toggle 与回调实现，写者倾向“先回滚、验证成功才落值”。

## 例外与边界

- 源端这项 Preference 设了 android:persistent="false" 或没有 key 时，返回 true 只更新这项的显示状态、不写入偏好；目标照样先更新开关显示，但不新增一条持久化写入。

## 原因

onPreferenceChange 的返回值决定这次变更是否被接受：返回 true 时 Preference 随即持久化新值并更新显示，之后到达的验证结果只能做补偿。改成“先回滚、成功才落值”会颠倒落值时刻与失败分支，取消时多出回滚，开关显示与偏好值都和源端不同。

## 做法

1. 按返回值迁移：源端 return true 时先写入新值并更新开关，再发起验证，验证回调只执行源端写明的补偿，取消或失败不回滚；源端 return false 时才保持旧值，由回调决定是否写入。
2. 源设置页只在 onResume 等时机重读的状态，目标不额外订阅事件即时刷新。
3. 规格写这类联动流程时逐步写出落值时刻（立即生效或事后补偿）与失败分支。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 未用；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；androidx.preference:preference 1.2.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕安卓 Preference.OnPreferenceChangeListener.onPreferenceChange 在 Preference 状态更新和持久化之前调用，返回 true 表示用新值更新 Preference 的状态
- 〔原因 / 做法第 1 步〕开关类偏好（TwoStatePreference）被点击时先以新值调用 callChangeListener，监听器返回 true 才调用 setChecked(新值)，setChecked 里写入持久化；android.preference 与 androidx.preference 1.2.1 都是这样
