# 弹窗和弹层的承载形态

agent 会看到什么：源端弹窗是 DialogFragment、XPopup 的 CenterPopupView / AttachPopupView / BottomPopup，交接、派工、弹层矩阵或覆盖清单里写成「page-hosted popup/sheet」「页面内弹层」，或按调用 show() 的类记宿主

## 通用查法

### 计划或交接里列安卓弹窗时，按源弹窗的基类和锚点逐个写出目标承载 API

审的是：计划与派工
触发（任一种）：
- 读到：源端弹窗类继承 DialogFragment、XPopup 的 CenterPopupView / AttachPopupView / BottomPopup 这类基类，依附式的用 atView(...) 指定锚点；写错的样子：计划、派工、交接或核对清单里弹窗只写「page-hosted popup/sheet」「页面内弹层」「恢复可关闭」这类泛称，没有逐个写目标承载 API 和宿主页
适用范围：规划、派工、交接或盘点一批安卓弹窗的迁移时，写每个弹窗承载形态的那一处
做法：
- 逐个弹窗在源码里读出类别：按弹窗类继承的基类分成居中类、锚点类、底部类；锚点类再看 atView 传入的视图取自哪一页，那一页就是宿主
- 按类别写目标承载：居中类写 CustomDialogController 的 open()，锚点类写挂在宿主页锚点组件上的 bindPopup，底部类照已批准的映射写（如 showBindSheet）；项目已有弹窗封装时写同一封装；矩阵、交接和日志里原样写，不改述成泛称
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(value: CustomDialogControllerOptions)；open()；close()：CustomDialogController 的构造和开关，居中类弹窗的承载（出处：鸿蒙 SDK 的 ets/component/custom_dialog_controller.d.ts，CustomDialogController）
- bindPopup(show: boolean, popup: PopupOptions | CustomPopupOptions): T：锚点类气泡的承载，绑在锚点组件上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindPopup）
针对本应用要查的：
- 每个弹窗的类别和宿主页：源工程里弹窗类的声明（继承的基类）和调用处（show()、atView(...)）；按基类归到居中、锚点、底部三类；锚点类看传入 atView 的视图属于哪个 Fragment 或 Activity。例：继承 AttachPopupView、锚点取自 parentFragment 时，宿主是父页，不是调用 show() 的子页
- 项目已采用的弹窗库和封装：目标工程 oh-package.json5 的 dependencies，以及决策台账里关于弹窗形态的条目；有 @pura/harmony-dialog 一类库、已有弹窗走它的 showCustomDialog 时，写同一封装
未核实：底部类弹窗（BottomPopup）对应 showBindSheet 只出自已批准计划的映射，族里规矩没有查实它的签名和行为
来源：3 张卡，1 个应用
- case-58884768863f720f109c（记得日历）：做法第 2 步 ← 建议 2
- case-c777abf40cffa3ab181d（记得日历）：做法第 1 步 ← 建议 1
- case-e2c0fe92e09e74d58cb7（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-d03626997c81｜弹窗恢复批次的交接和派工写出承载形态契约，不写成页面内弹层｜读到：用户要求「真弹窗、可关闭」；安卓端是 DialogFragment、XPopup CenterPopupView / AttachPopupView；写错：交接或派工写成「恢复 page-hosted popup/sheet 的关闭、返回、遮罩」「恢复为可关闭的页面内弹层」「wire … to the existing dialog」，没指明承载形态；或给锚点类留了「轻量 host overlay」选项
- rule-79518050fdcb｜批量改造弹层前先生成逐项弹层矩阵，移交和日志原样引用映射目标 API｜读到：已批准的计划要求先生成逐项弹层矩阵，映射写「BottomPopup → showBindSheet / 系统半模态」；写错：批量宿主化前没有弹层矩阵；handoff 或执行日志把目标改述成「page-hosted popup/sheet」「恢复关闭、返回、遮罩」，不再写 showBindSheet
- rule-da688b99b582｜依附式弹窗按 atView 锚点所在页判宿主，不按调用 show() 的类判｜读到：源端弹窗类继承 `AttachPopupView`，调用方用 atView(...) 指定锚点，锚点视图取自 parentFragment（父页标题栏上的按钮等），show() 却在子 Fragment 里调用；写错：覆盖清单或审计记录把这个弹窗记在调用 show() 的子页名下，写成「子页已内联等价提示」「可删」；或者目标端锚点在源端弹出条件下从未变为可见，仍记成等价
- rule-4e59944573d0｜派工把弹窗统一改成页内浮层时，写明适用范围和 onBackPressed 关闭要求｜读到：上游转换报告以「P-27: inline Stack overlay」上报弹窗做法，没提 Back；写错：派工里写「对话框全部 → 页内 @Builder overlay（P-27）」，没写 P-27 的适用范围和负向守卫，也没要求按 onDismissRequest 接管 Back
