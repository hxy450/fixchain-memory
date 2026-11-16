# 预签名上传地址可能是 http 时，网络层按端点放行明文，其余请求仍只接受 https

审的是：代码
触发（任一种）：
- 读到：安卓清单写了 android:usesCleartextTraffic="true"，上传地址由 presign 接口返回后原样 PUT；写错的样子：目标网络层对 Raw 端点的绝对 URL 一律做 `https://` 前缀校验、不是就抛错，或者把返回的 http 地址自动改写成 https
适用范围：目标端自研网络层处理服务端下发的预签名地址或其他动态绝对 URL 时
做法：
- 端点声明里加一个允许明文的开关（例如 allowCleartext: boolean），只给预签名上传的 PUT 端点打开；没打开的端点仍只接受 https 绝对地址
- PUT 时原样使用 presign 返回的地址，不自动升级成 https；网关层和底层 URL 解析处的 https 判断要一起改，不留同类校验
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 端点白名单：仅预签名上传 PUT 允许 http，PUT 原样使用返回地址：改成这样后 http 预签名地址能上传，其余请求仍是默认 HTTPS（出处：卡里修好并验证过）
- Network Kit 从 API version 18 开始默认支持明文 HTTP；API 20 起可在 network_config.json 的 component-config 里开关，默认为 true：@ohos.net.http 本身不拦 http 地址，拦截来自应用自己的校验（出处：http-request.md，明文HTTP访问权限配置说明）
- 错误码 2300997，Cleartext traffic not permitted.：network_config.json 里把 cleartextTrafficPermitted 设成 false 时，系统层拦明文的报错（出处：errorcode-net-http.md，2300997 明文HTTP被拦截）
针对本应用要查的：
- 目标工程有没有在系统层禁止明文：目标工程 src/main/resources/base/profile/network_config.json 的 network-security-config；base-config 或上传域名对应的 domain-config 里 cleartextTrafficPermitted 为 false 时，上传域名也要放开，否则报 2300997
来源：1 张卡，1 个应用
- case-6a6e6b7124655d1844a6（记得日历）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 诊断；取值 1 ← 诊断
