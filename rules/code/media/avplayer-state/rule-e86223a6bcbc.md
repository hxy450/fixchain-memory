# 源端同步装载改成带 await 的 AVPlayer 装载时，每次装载带代数并持有自己的实例

审的是：代码
触发（任一种）：
- 读到：源端播放器在调用线程（或内部单线程 executor）内顺序执行 stop → 新建播放器 → `setDataSource` → `prepare`；写错的样子：目标装载函数经过多个 `await` 后才对共享的 `this.avPlayer` 设源，`completed` 回调不核对是不是当前实例；两次装载交错时后到的设源报 not idle，前一次照常起播并按播完收尾
适用范围：把源端同步的播放装载改写成异步 AVPlayer 单例装载时
做法：
- 每次装载分配一个代数或令牌（如自增的 loadGeneration），装载用自己创建的 AVPlayer 实例，不共享一个字段
- 每个 await 之后核对代数，已被新装载、引擎错误或停止服务取代就放弃；completed、error 回调先核对实例是否为当前实例，不是就忽略
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 加装载代数、每次装载独占自己创建的实例、completed 只认当前实例后，交错装载不再串台：修好的写法（出处：卡里修好并验证过）
- AVPlayer 的 url 只能在 idle 状态设置：两次装载共用一个已 initialized 的实例时，后一次设源会失败（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.url）
未核实：一次点按产生第二次装载的具体触发点卡里没查清
来源：1 张卡，1 个应用
- case-0b0bf6cdf94608e17cbb（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
