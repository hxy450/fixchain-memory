# 移交和派工里的 module.json5 注册说明要与基类对应，未核实的字段标待核

审的是：计划与派工
触发（任一种）：
- 读到：扩展能力的源文件 extends AppServiceExtensionAbility，或编译时换过扩展基类；写错的样子：handoff 或派工里写着 extensionAbilities 注册 type=service、backgroundModes 等字段，与基类不对应，或没核实就写成确定指令
适用范围：移交项和派工里给后续环节写 module.json5 注册指引时
做法：
- 注册说明写成与基类对应的 type（AppServiceExtensionAbility ↔ appService，WorkSchedulerExtensionAbility ↔ workScheduler），不给扩展条目写 backgroundModes
- 不能编译核实的注册字段标为待核，不写成确定指令
来源：1 张卡，1 个应用
- case-b92afb07b8ec2465afcf（CleanSweep）：做法第 1 步 ← 建议 3、建议 2；做法第 2 步 ← 建议 2
