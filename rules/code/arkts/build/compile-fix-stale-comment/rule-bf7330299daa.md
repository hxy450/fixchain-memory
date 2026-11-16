# 改了扩展基类后，源文件头注释里的注册说明同步改成对应的 type

审的是：代码
触发（任一种）：
- 读到：编译报 @kit.AbilityKit 没有 ServiceExtensionAbility（Did you mean AppServiceExtensionAbility），随后把类改为 extends AppServiceExtensionAbility；写错的样子：源文件已 extends AppServiceExtensionAbility，头注释仍写着「extensionAbilities 注册（type=service, backgroundModes=[…]）」
适用范围：扩展能力的源文件头注释里写有 module.json5 注册说明时
做法：
- 换基类时把头注释的注册说明改成与基类对应的 type（AppServiceExtensionAbility ↔ appService），删掉扩展条目不接受的 backgroundModes
- 没能编译核实的注册字段在注释里标「待核」，不写成确定指令
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 陈旧头注释被后来的修复者照抄，又写回 type=service 和 backgroundModes：不改注释的后果（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-b92afb07b8ec2465afcf（CleanSweep）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 2；取值 1 ← 诊断
