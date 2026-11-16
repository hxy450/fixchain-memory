# 源端应用终止时释放作用域和持有者，目标写 release() 并在 EntryAbility.onDestroy 调用

审的是：代码
触发（任一种）：
- 读到：源 Application.onTerminate 里依次取消应用协程作用域、shutdown 各状态持有者（如 TTS、播放器）；spec 的 AC 规定应用终止时释放并标了目标符号；写错的样子：EntryAbility 的 onDestroy() 只打日志，没有 release() 接口和调用；持有者还没创建时也没有登记 FWD-REF 占位，信封也没列为未实现
适用范围：源端在应用终止时释放全局作用域或单例持有者，迁成 ArkTS 应用壳时
做法：
- 在应用壳服务里写 release(): void：取消应用作用域，各持有者 shutdown 一次；在 EntryAbility 的 onDestroy() 里调用它
- 依赖的作用域或持有者还没创建时，先写 release() 接口和 onDestroy 调用点，缺的依赖登记 FWD-REF
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onDestroy(): void | Promise<void>：UIAbility 销毁时的回调，release() 的调用点（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onDestroy）
- 补上 release()（取消应用作用域，两个持有者各 shutdown）并在 onDestroy 调用后，AC 判定通过：修法（出处：卡里修好并验证过）
- Application#onTerminate 只用于模拟进程环境，在量产安卓设备上从不调用：源端这段释放在真机上不执行；目标仍按 AC 写 release()（出处：android.app.Application#onTerminate）
来源：1 张卡，1 个应用
- case-85c033903030498c795d（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 2 ← 诊断
