# 平台差异决策与偏离

规格或决策台账里写了「无对等」「降级」「不迁移」「PD」「显式差异」「用户例外」这类平台差异决策和偏离，或写它们的依据栏时

## 触发族

- [决策台账里对系统能力写的「平台无对等」和降级条目](system-capability-no-equivalent/index.md)（7 条）：读到源端依赖系统级能力（如 dynamicLightColorScheme 壁纸取色），常带 Build.VERSION.SDK_INT 门槛和回退分支；决策台账写「HarmonyOS 无 X API 对等」或降级成固定配色，没有 d.ts 检索结果和能力探测
- [决策台账里 PD 条目的依据、批准状态和缺陷表](ledger-pd-entries/index.md)（7 条）：读到默认策略、spec 默认原则对 PD 的要求（依据要有条目原文、某类 PD 默认阻断、原版缺陷要保留）；交回的决策台账里 PD 依据只写 skill 名或「@kit.ArkUI d.ts」、凭 gate 自动批准写成 approved，或只有 `PD` 条目没有 `C12` 原版缺陷表
- [spec gap 里安卓固定行为与规格验收的冲突](spec-gap-vs-android/index.md)（1 条）：读到源码理解笔记写明安卓固定行为 X、与规格验收清单的 Y 冲突，台账有忠实迁移原则；spec gap 的处置写成「按 Feature Spec 实现 Y 并记录显式差异」
- [差异决策里当作查证依据的经验提醒](experience-as-evidence/index.md)（1 条）：读到注入的经验提醒或摘要给出两端差异的说法（如导航栏是否算在显示尺寸内）；规格依据栏或决策台账写「团队经验回执」「经验查证回执」，没有源码、平台资源或参照机实测的出处
- [联调时与源端声明不一致的用户描述](user-report-vs-source/index.md)（1 条）：读到用户报告的行为（如首次进入应为未选中）和源 XML 的声明值不一致；例外登记把它记成用户例外（U-…），没写源控件的实际运行语义
- [决策台账里的大字体（随系统字号缩放）条目](font-scale-decision/index.md)（1 条）：读到源端主体是固定 px 字号的 Canvas 自绘，但仍有 AlertDialog.Builder 系统对话框、Toast、菜单或 sp 单位的文本，Manifest 的 Activity 没声明 android:configChanges="fontScale"；决策台账写「大字体 | 不适用」，没列随系统字号缩放的文本和目标落点
- [被记成降级的界面视觉效果（自绘组件、输入框富文本）](ui-effect-downgrade/index.md)（4 条）：读到源端界面有自绘视觉组件（如 Material3 Expressive 的 CircularWavyProgressIndicator）或输入框 visualTransformation 富文本；skip-list、决策台账或转换决策把它记成「实现降级」「能力受限，编辑态降级」的 PD 或已批降级，没核对 Canvas / Path、RichEditor 等候选组件
- [转述平台差异决策时超出它列明的范围](decision-scope-overreach/index.md)（2 条）：读到台账或规格的平台差异决策（PD、显式退化）只列了某几项能力或出口；台账汇总行把别的能力一并写成「执行 approved unavailable UX」，或源码笔记把它扩成整段富文本、全部链接都不实现，decision_gaps 里没有这项偏离
