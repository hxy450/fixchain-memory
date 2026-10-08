# arkts/runtime-semantics

源端同步调用或数值运算改成 ArkTS 后的运行时差异：异步失败分支、初始化顺序、错误通道与 number 边界

[上一级](../index.md)

## 本级经验

- [仓库方法前置失败走声明的错误通道不返回空集合](lesson-5c703b4b1128e37dbef5.lesson.md) · 阶段：execute · 信号：UIAbilityContext, requestPermissionsFromUser, photoAccessHelper, Repository
- [可编辑输入状态在初始化首个 await 之前赋初值](lesson-843a70afd7e08bfed97c.lesson.md) · 阶段：execute · 信号：TextInput, aboutToAppear, @Local, ViewModel
- [异步 initialize 失败分支要复位状态并离开加载态](lesson-338f11844f0010e46bc3.lesson.md) · 阶段：execute · 信号：initialize(), LoadingProgress, aboutToAppear, SharedPreferences
- [比值计算保留零分母分支与钳制，0/0 得 NaN](lesson-52d7edb9042110e30eb4.lesson.md) · 阶段：execute · 信号：coerceIn, NaN, total == 0, Math.min
