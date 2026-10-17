# arkts/runtime-semantics

源端同步调用或数值运算改成 ArkTS 后的运行时差异：异步失败分支、初始化顺序、错误通道与 number 边界

[上一级](../index.md)

## 本级经验

- [Float 运算比较按 float32 后用 ===](lesson-0deb51172ebdd2e056a9.lesson.md) · 阶段：spec/execute · 信号：Math.fround, toFloat(), Float, (int)
- [Kit 错误取 message 与 code，码先归一](lesson-b19162077a2ab886d809.lesson.md) · 阶段：spec/execute · 信号：BusinessError, Number(code), instanceof Error, @ohos.net.http
- [仓库方法前置失败走声明的错误通道不返回空集合](lesson-5c703b4b1128e37dbef5.lesson.md) · 阶段：execute · 信号：UIAbilityContext, requestPermissionsFromUser, photoAccessHelper, Repository
- [异步 initialize 失败分支要复位状态并离开加载态](lesson-338f11844f0010e46bc3.lesson.md) · 阶段：execute · 信号：initialize(), LoadingProgress, aboutToAppear, SharedPreferences
- [比值计算保留零分母分支与钳制，0/0 得 NaN](lesson-52d7edb9042110e30eb4.lesson.md) · 阶段：execute · 信号：coerceIn, NaN, total == 0, Math.min
- [超安全整数的 long 常量以字符串拼进 SQL](lesson-5f669c379cfcdb14ad10.lesson.md) · 阶段：execute · 信号：Long.MAX_VALUE, Number.MAX_SAFE_INTEGER, bigint, 9223372036854775807
- [输入初值先于首个 await；源端同步初始化保持同步](lesson-843a70afd7e08bfed97c.lesson.md) · 阶段：execute · 信号：TextInput, aboutToAppear, @Local, onCreate
