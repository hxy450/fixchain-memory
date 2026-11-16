# 播放通道因 context 为空短路时，分支里先写 hilog.warn 再回调失败

审的是：代码
触发（任一种）：
- 写错的样子：封装类的 load 等方法里 if (ctx === null) 之类的短路分支直接回调失败或 return，没有 hilog.warn 或 hilog.error
适用范围：目标端封装的音频播放通道（音乐、音效）里，因宿主已释放、context 为空而提前返回的分支
做法：
- 短路分支里先写 hilog.warn(DOMAIN, TAG, 'context released, skip load') 再走失败回调，和同一文件里其他通道已有的 'context released' 日志写法一致
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function warn(domain: number, tag: string, format: string, ...args: any[]): void：警告级日志（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.warn）
- domain 是 0x0–0xFFFF 的十六进制整数，超出范围不打印；tag 不超过 32 字节，超出截断：DOMAIN、TAG 两个参数的限制（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.warn）
- function error(domain: number, tag: string, format: string, ...args: any[]): void：同族接口：错误级日志，参数相同（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.error）
来源：1 张卡，1 个应用
- case-6f949100d998a4784716（Blockinger）：做法第 1 步 ← 建议 3
