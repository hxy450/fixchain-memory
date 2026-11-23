# 服务卡片按实际宽高选布局：由 FormExtensionAbility 取尺寸下发，V1 卡片页的派生值写成普通方法

## 何时使用

服务卡片实现阶段，卡片需要按实际宽高选择布局档位，或在 V1 @Entry 卡片页里由尺寸等状态派生布局值时

## 适用情境

源端 Glance AppWidget 用 SizeMode.Exact/LocalSize 按卡片实际宽高选布局（宽度断点、按高度显示标题栏等）；目标为 ArkTS 服务卡片（V1 卡片页 + FormExtensionAbility + form_config 离散规格），实现者准备在卡片页用通用尺寸事件取宽高，或只按 FormDimension 档位一档对一形态。

## 例外与边界

- getFormRect 与 onSizeChanged 自 API 20 起才有，且 getFormRect 在能力不支持时抛错误码 801：工程最低兼容版本低于 API 20 或调用失败时拿不到实际宽高，这时保留第 2 步按离散规格换算出的档位作为卡片的初始数据，不让卡片因缺尺寸停在默认分支

## 原因

卡片页可用的事件与组件受限：onAreaChange 等通用尺寸事件的 SDK 注释不带 @form，编译会拒绝；只按离散规格一档对一形态时，档位与源端宽度阈值不一定对应。来源中 V1 卡片页 struct 的 get 访问器在转译产物里不存在，运行时取到 undefined，卡片恒走默认分支（修复者查看编译产物确认，未在其他 SDK 版本复核）。

## 做法

1. onAddForm 后调用 formProvider.getFormRect(formId)，并实现 onSizeChanged(formId, newDimension, newRect)，把 vp 宽高经 formProvider.updateForm 写进卡片数据；卡片页用 @LocalStorageProp 读取，按源端阈值派生档位（来源 SDK 中 getFormRect 标注为 API 20）。
2. 离散规格只作兜底提示：按目标设备上该规格的实际 vp 宽度对照源阈值换算档位，冲突时上报，不强行一档对一形态。
3. V1 卡片页里由状态派生的值写成 build 内调用的普通方法，不写 struct getter。
4. 拿不准某个通用事件或组件能否用在卡片里时，查 SDK .d.ts 注释是否带 @form；本地 skill 检索无结论不等于可用。

## 可选检查

- 派生值是否生效有疑问时，查编译产物中该方法仍在，或在卡片加日志确认档位随尺寸变化。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 3 步〕V1 @Entry 卡片页 struct 里写的 get 访问器在编译产物里不存在，卡片运行时读它恒为 undefined，依赖它的分支总走默认分支
- 〔做法第 1 步〕FormExtensionAbility.onSizeChanged 在卡片尺寸变化时回调，newRect 给出新的卡片矩形，单位 vp（API 20 起）
- 〔做法第 1 步〕formProvider.getFormRect 返回卡片相对屏幕左上角的位置和卡片尺寸（API 20 起）；formInfo.Rect 的 left、top、width、height 单位都是 vp
- 〔做法第 1 步〕卡片提供方和卡片 UI 是两个独立进程，数据只能通过 LocalStorageProp 传递：提供方 updateForm 推送的数据，卡片页用 @LocalStorageProp(键名) 接收，不能用 getContext
