# 交给外部应用的隐式 Intent 和可用性回退

agent 会看到什么：读到源 helper 按 scheme 用 ACTION_VIEW / ACTION_DIAL / ACTION_SENDTO 交给外部应用、可用性检查为假时回退或提示（如 geo: 打不开改开网页地图）；规格断言目标平台没有这套能力、把回退标 superseded，或服务层只留一个分类函数，动作和可用性探测没有目标符号承接

## 规矩

- rule-ee89faea3137｜把源 helper 翻成服务契约时，动作和可用性探测要有目标符号承接，不只留分类函数｜读到：源 helper 按 scheme 分发：tel → ACTION_DIAL、mailto → ACTION_SENDTO、其他 ACTION_VIEW；可用性检查为真才 startActivity，否则抛异常，页面提示没有应用可处理；写错：服务层契约只定义一个分类函数（返回 'dial' | 'sendto' | 'view' 这类值），动作和可用性探测没有目标符号承接，验收条目只留「无可用 App 提示」
- rule-8f956e45884e｜规格断言目标平台没有某能力前先查声明，未核实前保留源端回退和重启语义｜读到：源码用 ACTION_VIEW 打开 geo: URI，可用性检查为假时改开网页地图 URL（两级回退）；写错：规格断言「HMOS 无 geo: scheme 隐式 intent 体系」，把两级回退的验收条目标 superseded，另立 PD 改成固定网页 URL 单级 startAbility
