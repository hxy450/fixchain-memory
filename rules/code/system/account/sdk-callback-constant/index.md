# SDK 回调类型常量

agent 会看到什么：读过的源码只用符号比较回调类型（resp.getType() == ConstantsAPI.COMMAND_PAY_BY_WX）；交回的代码把回调类型写成手写的数值常量，onResp 按它分流

## 规矩

- rule-d86a1cd5950a｜SDK 回调类型常量不凭记忆写数值，从已装 SDK 的声明读或用 instanceof 区分｜读到：源端只用符号比较回调类型：resp.getType() == ConstantsAPI.COMMAND_PAY_BY_WX；写错：目标端把支付回调类型写成手写的数值常量（如 = 3），注释称「SDK 同值」，onResp 按它分流
