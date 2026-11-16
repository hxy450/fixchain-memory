# 关闭 FWD-REF 注入槽而注入落在别处运行时机时，补带断言的 HANDOFF，不只写已兑现注释

审的是：计划与派工
触发（任一种）：
- 读到：基座契约列出的 `FWD-REF`（resolve_by=…）注入槽，以及同类启动期接线已有的 HANDOFF 写法（owner 是 EntryAbility.onCreate）；写错的样子：`FWD-REF` 标记被删掉，换成「已兑现：注入点 = ….getInstance()」一类注释，没有留下 owner 指向启动序列、带 verify=grep:… 机械断言的 HANDOFF
适用范围：关闭基座留下的 FWD-REF 或注入槽、而注入实际要在另一个文件（应用启动序列）的运行时机发生时
做法：
- 按流水线 _common.md §2.1b 的格式补一条 HANDOFF：owner=EntryAbility.onCreate，what=调用注入入口（单例的 getInstance 或 DAO 的钩子 setter），verify=grep:能机械核对这次调用存在的式子
- 不要只把 marker 换成「已兑现、注入点在 X」的注释；收尾装配按 HANDOFF 逐项装配，「已兑现」注释不是核对的终点
未核实：没核到派工说明或执行技能是否明文规定了这类注入槽的位置
来源：1 张卡，1 个应用
- case-97e280ce0a8ddc7a54a1（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、建议 3
