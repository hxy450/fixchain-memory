# 登录、授权与三方 SDK

源端按 token 判登录态，或调微信这类 SDK 授权、支付并在回调里按类型分流，目标端有登录态判断、授权回调的 state 校验和 SDK 回调处理时

## 触发族

- [单会话授权回调的 state 校验](auth-callback-state/index.md)（2 条）：读到每次请求带随机 state 的 SDK 授权（SendAuthReq 一类）、规格写「state 错配拒绝」「旧回调必须失效」「迟到回调」；产物里回调处理的判断顺序和它的契约测试
- [按 token 判定的登录态](token-login-state/index.md)（3 条）：读到源端按 token（hasToken 一类）判登录、启动固定进主页、退出登录还清本地数据库业务表；交回的启动写成 token.length > 0 ? 主页 : 登录页、用昵称判空决定显示「未登录」，或退出只清 preferences
- [SDK 回调类型常量](sdk-callback-constant/index.md)（1 条）：读过的源码只用符号比较回调类型（resp.getType() == ConstantsAPI.COMMAND_PAY_BY_WX）；交回的代码把回调类型写成手写的数值常量，onResp 按它分流
