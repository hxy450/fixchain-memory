# 列表解析里单条记录的展示文本为空时降级为空串，catch 记下具体异常，不让整页失败

审的是：代码
触发（任一种）：
- 写错的样子：解析器里单条记录的展示字段校验失败就 throw，外层 catch 把整页置为加载失败态，只显示通用错误文案，没记下 error.message
适用范围：目标端解析打包或网络来的列表数据、渲染成列表页时
做法：
- 单条记录的展示文本字段为空或类型不对时降级为空串或占位，继续解析其余条目
- catch 分支用 hilog.error(domain, tag, '%{public}s', String(err)) 记下具体异常（哪一条、哪个字段），界面仍显示资源里的错误文案
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function error(domain: number, tag: string, format: string, ...args: any[]): void：输出 error 级日志；domain 是 0x0–0xFFFF 的十六进制整数，tag 不超过 32 字节（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.error）
- 格式串里的参数隐私标识分 {public} 和 {private}，缺省为 {private}：异常信息要写成 %{public}s 才能明文看到（出处：js-apis-hilog.md，hilog.error）
- 把错误文案临时换成 error.message 后，设备上直接显示出是第几条缺哪个字段：记下具体异常能直接定位到条目和字段（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ffdccd8c954d99b4c6d6（Cofi）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
