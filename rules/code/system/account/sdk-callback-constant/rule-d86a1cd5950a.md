# SDK 回调类型常量不凭记忆写数值，从已装 SDK 的声明读或用 instanceof 区分

审的是：代码
触发（任一种）：
- 读到：源端只用符号比较回调类型：resp.getType() == ConstantsAPI.COMMAND_PAY_BY_WX；写错的样子：目标端把支付回调类型写成手写的数值常量（如 = 3），注释称「SDK 同值」，onResp 按它分流
适用范围：实现三方 SDK 回调分派（登录、支付共用回调）时
做法：
- 从已安装 SDK 的声明读常量（鸿蒙微信 SDK 用 Command.kCommandPay），或按 skill 用 instanceof PayResp / SendAuthResp 区分
- 无法核实时在代码里显式标注待核，不写死数值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 微信 SDK 支付回调类型：Android ConstantsAPI.COMMAND_PAY_BY_WX 和鸿蒙 Command.kCommandPay 都是 5；授权是 1：onResp 按类型分派时的取值（出处：卡里修好并验证过）
针对本应用要查的：
- 回调类型常量的值：目标工程已安装的 SDK 包（oh_modules 下该包的 .d.ts / .d.ets 声明）里按常量名找；直接引用常量名，不抄数值
未核实：ConstantsAPI.COMMAND_PAY_BY_WX 和 Command.kCommandPay 的值本机没有源码或声明可核，按卡写
来源：1 张卡，1 个应用
- case-febf3c781ebde9778c30（DeepAI全能PPT）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断
