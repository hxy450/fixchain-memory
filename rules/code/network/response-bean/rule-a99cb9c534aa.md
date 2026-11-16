# 手写 raw JSON 取值时按 res.data 对应的 Bean 字段链逐层写键，不照抄源端路径

审的是：代码
触发（任一种）：
- 读到：源端 Retrofit 回调写 success { result -> result.data?.xxx }，result 已是解包后的容器 Bean，容器 Bean 自身还有一个名为 data 的字段；写错的样子：目标服务层对 res.data 直接按键取 xxx（如 getArray(res.data, 'cols')），少取容器内层的 'data'
适用范围：目标网络层把 BaseResponse.data 原样作为 raw Record 返回、由服务层按键手动取值时
做法：
- 先确认目标 res.data 对应源端哪一层类型（通常是解包后的容器 Bean），再按该 Bean 的字段链逐层取：容器有内层 data 时先取 getObject(res.data, 'data')，再从它取 xxx
- 同一服务写完多个容器端点后，列出每个端点「目标取值键链 ↔ Bean 字段链」对照；Bean 含内层 data 的，取值链里必须有对应的一层 'data'
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 先取内层 getObject(res.data, 'data')，再取目标数组；实测响应是 body.data.data.xxx：修好的取值链（出处：卡里修好并验证过）
针对本应用要查的：
- 这个端点 res.data 对应的 Bean 和它的字段链：源工程里 Repository 方法返回类型对应的 Kotlin data class（按类名搜定义），以及目标 Api 文件里这个端点的注释或返回类型；从 res.data 对应的那层开始，逐层写出到目标字段的键名
来源：1 张卡，1 个应用
- case-18365c67d94d72d8a825（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
