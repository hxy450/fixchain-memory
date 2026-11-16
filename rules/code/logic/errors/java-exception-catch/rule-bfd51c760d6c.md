# Kit API 的 catch 值不按 Error 实例取消息，统一走公共取消息函数

审的是：代码
触发（任一种）：
- 读到：源端 catch 里用 e.getMessage() / exception.getMessage() 写日志、提示、通知或下载结果详情；写错的样子：目标端 catch 里写 error instanceof Error ? error.message : String(error)，被捕获的是 @ohos.net.http、文件、数据库等 Kit 抛出或 reject 的 BusinessError
适用范围：目标端 catch 到 Kit API（网络、文件、relationalStore、媒体等）的失败值，要取消息或错误码时
做法：
- 公共层建一个取消息函数：Error 取 message；否则读 (e as BusinessError).message 和 code；都没有才 String() / JSON.stringify()
- 各 catch 统一调用它，不在每处写 instanceof Error ? message : String()；新增 catch 前先找项目里已有的取消息函数，复用的旧服务代码里的这种写法一并替换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- export interface BusinessError<T = void> extends Error { code: number; … }：BusinessError 的声明：带数字 code，message 来自 Error 的声明（出处：鸿蒙 SDK 的 ets/api/@ohos.base.d.ts，BusinessError）
- 运行期 catch 到的 BusinessError 是 {code, message} 普通对象，instanceof Error 为 false，String(error) 得到 '[object Object]'：按 Error 实例处理时消息丢失；改成 Error.message → BusinessError.message → String 的顺序后日志得到真实消息（出处：卡里修好并验证过）
针对本应用要查的：
- 项目里已有的统一取消息函数：目标工程公共层（system、common、utils 一类目录）的 .ets 文件，按 BusinessError 和 message 搜；有就直接调用；没有就新建一个，并把已有的 instanceof Error ? … : String(…) 写法替换掉
未核实：OPML 解析、自动导出、数据库写入、在线 feed 查找这类调用点修复期没有逐一复现 BusinessError，真机只复查了 HTTP 刷新路径
来源：1 张卡，1 个应用
- case-bae545fb004bef3f5772（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、建议 4；取值 2 ← 诊断
