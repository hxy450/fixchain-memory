# 规格AC源锚点含onEventMainThread时，覆盖清单逐条写订阅落点，不以占位清零代替

审的是：计划与派工
触发（任一种）：
- 读到：功能规格的 AC 源锚点写着 onEventMainThread(…Event) 或 @Subscribe（如登录成功后重载数据）；计划的验收模板要求状态、事件、取消、销毁覆盖 AC；写错的样子：占位登记里这一页只有数据加载和点击类占位，没有事件订阅（登录后刷新）那一项；收口报告只写「已清除全部自身 P-S… 占位」，没有逐条 AC 写订阅和释放落在哪里
适用范围：功能切片页面接线的占位登记、派工和收口覆盖清单，规格里有源锚点是 EventBus 订阅回调的 AC 时
做法：
- 把规格里源锚点含 onEventMainThread(…Event) / @Subscribe 的 AC 逐条列进覆盖清单，每项写明：订阅哪个事件、目标页出现时订阅（aboutToAppear）、消失时释放（aboutToDisappear）、事件到达后重读哪些数据
- 订阅清单按源 controller（规格锚点指向的 Fragment）里的 @Subscribe 方法逐个对上，少一个就补一项
- 占位清零不作为这类 AC 的完成依据：收口报告对每条这类 AC 写出订阅和释放的落点
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- UI 壳只为数据加载和点击预留占位、没有登录刷新占位时，占位清零后这条 AC 仍未落实：占位清单不等于 AC 覆盖（出处：卡里修好并验证过）
针对本应用要查的：
- 源 controller 里有哪些事件订阅：源工程里规格 AC 源锚点和计划 controller 锚点指向的 Fragment 源文件，按 @Subscribe 和 onEventMainThread 找；每个带 @Subscribe 的方法是一项订阅，参数类型就是事件，方法体里调用的加载就是要重读的数据
未核实：派工是否单独点名了这类 AC 无法确认
来源：1 张卡，1 个应用
- case-46ac36102451125de693（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1、诊断；取值 1 ← 诊断
