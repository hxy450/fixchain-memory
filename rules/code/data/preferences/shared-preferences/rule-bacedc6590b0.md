# 源端 Editor 累积后一次 commit 的恢复流程，目标先暂存、全部通过后再 putSync

审的是：代码
触发（任一种）：
- 读到：恢复时往 SharedPreferences.Editor 里逐键 put，末尾一次 commit()，中途异常直接返回 false；写错的样子：目标在解析过程中逐键 putSync 写进共享 Preferences 实例，最后才 flushSync；中途失败时已解析的值留在实例里
适用范围：迁移 SharedPreferences.Editor 累积后 commit 的恢复或批量写入流程时
做法：
- 解析时先把键值放进暂存表（Map），全部校验通过后再逐个 putSync 并 flushSync；中途失败时丢弃暂存表，不碰实例
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Editor 里的改动是批量的，在调用 commit 或 apply 前不会回到原 SharedPreferences：源端中途失败时实例不变（出处：android.content.SharedPreferences.Editor）
- putSync(key: string, value: ValueType): void；直接写进缓存的 Preferences 实例：目标 putSync 立即改共享实例，不等 flush（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.putSync）
- 改为暂存表、finishRestore 时再 put 加 flush 后，中途失败实例不变：修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ad0ab84cef0e7cbc3696（Privacy Friendly 2048）：做法第 1 步 ← 建议 4、诊断；取值 3 ← 诊断
