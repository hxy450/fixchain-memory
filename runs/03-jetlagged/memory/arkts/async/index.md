# arkts/async

源端同步调用改成 ArkTS 异步（Promise/async）后新增的失败分支与加载态

[上一级](../index.md)

## 本级经验

- [同步读取改成异步 initialize 后，失败分支要复位状态并让页面离开加载态](lesson-338f11844f0010e46bc3.lesson.md)
  - 时机：功能实现阶段（ViewModel 与页面接线），把源端同步读取的设置或数据改成异步加载，并给页面加“加载完成前不显示或不可交互”的门时
  - 情境：源端在首帧前用 SharedPreferences 等同步接口读取（缺键用默认值），界面没有加载态或失败态；目标端改为 async 读取，ViewModel 暴露返回 Promise 的 initialize()，页面在 aboutToAppear 中调用，并用“已加载”标志在 LoadingProgress 与正式内容之间切换。
