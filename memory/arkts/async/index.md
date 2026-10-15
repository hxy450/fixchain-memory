# arkts/async

源端同步调用改成 ArkTS 异步（Promise/async）后新增的失败分支、加载态，异步初始化与用户输入的先后顺序，依赖先后生效的连续平台调用在网关内串行，单线程执行器改成 Promise 串行队列后的重入，仓库方法前置失败分支（未初始化、未授权）的错误通道，以及 Kit API catch 值（BusinessError）的取消息与按错误码分类，以及源 API 以返回值表示被拒、以异常表示故障而目标都 reject 时的单次适配

[上一级](../index.md)

## 本级经验

- [Kit API 的 catch 值按 BusinessError 取 message 与 code，网络失败按错误码映射源错误类型](lesson-b19162077a2ab886d809.lesson.md)
  - 时机：规格提取与服务实现阶段，迁移源端按异常类型分类、以 getMessage() 记录详情的 catch 分支时
  - 情境：目标 catch 到的是网络、文件、数据库等 Kit API 抛出或拒绝的 BusinessError：@ohos.base.d.ts 声明它 extends Error，运行时可能是 Error 实例，也可能是只含 code、message 的普通对象；源端按 IllegalArgumentException、SocketTimeoutException、UnknownHostException 等异常类型分支；@ohos.net.http 的失败码为 2300000 加 libcurl 码。
- [单线程写执行器改为 Promise 串行队列时，为重入调用提供不经队列的内部版本](lesson-cdc6de4ebcdeeadc287c.lesson.md)
  - 时机：数据层实现阶段，把源端单线程 Executor（调用方已在执行线程即同步内联）移植为异步串行队列时
  - 情境：源端写方法在已处于执行线程时直接内联执行嵌套调用（如按线程名判断后 runnable.run()）；目标队列任务体内会再调用同类公开写方法。
- [同步读取改成异步 initialize 后，失败分支要复位状态并让页面离开加载态](lesson-338f11844f0010e46bc3.lesson.md)
  - 时机：功能实现阶段（ViewModel 与页面接线），把源端同步读取的设置或数据改成异步加载，并给页面加“加载完成前不显示或不可交互”的门时
  - 情境：源端在首帧前用 SharedPreferences 等同步接口读取（缺键用默认值），界面没有加载态或失败态；目标端改为 async 读取，ViewModel 暴露返回 Promise 的 initialize()，页面在 aboutToAppear 中调用，并用“已加载”标志在 LoadingProgress 与正式内容之间切换。
- [异步初始化里，用户可编辑的输入状态在第一个 await 之前写入初值](lesson-843a70afd7e08bfed97c.lesson.md)
  - 时机：ViewModel 实现阶段，编排页面初始化方法中异步存储/SDK 绑定与输入状态初值的先后顺序时
  - 情境：源页面在初始化时同步写入关键词或输入框文本，操作读取实时输入；目标输入框双向绑定 ViewModel 字段，初始化方法内含 await（存储、历史、SDK 绑定），页面生命周期回调以不等待的方式调用它。
- [源 API 用返回值表示“被拒”、用异常表示故障，而目标 SDK 两者都 reject 时，用一个单次原语适配器还原三态，所有重试与返回码路径都经它](lesson-47faf26b44bb4075b0d2.lesson.md)
  - 时机：服务或引擎实现阶段，把以 boolean 返回业务结果、以异常表示 I/O 失败或目标丢失的源 API（如 MIFARE 扇区认证）映射到只以 Promise reject 报错的 SDK，并实现带重试或返回码的上层方法时
  - 情境：源方法返回 false 表示被拒并据此按偏好重试，只有 IOException、TagLostException 等才立即失败；目标方法返回 Promise&lt;void&gt;，被拒与 I/O、状态异常都以 BusinessError reject，d.ts 只列错误码、不说明各码对应哪种情形；同一文件里可能已有区分两者的单次函数，却只被部分路径调用。
- [源端连续的同步平台调用（先取消再振动、先停止再启动）映射到返回 Promise 的 API 时，在网关内串行发出或改用同步变体，不各自 fire-and-forget](lesson-ba0cb144aa48f9584060.lesson.md)
  - 时机：功能实现阶段封装平台能力网关，把源端依赖先后生效的连续同步系统调用映射为返回 Promise 的目标 API 时；规格提取阶段为这类映射写契约时
  - 情境：源端在同一方法里依次同步调用两个平台方法且后者依赖前者已生效（如 Vibrator.cancel() 后立刻 vibrate(pattern)）；目标 API（如 vibrator.stopVibration/startVibration）返回 Promise，网关接口按规格声明为 void，调用方仍按源顺序逐个调用。
- [需授权、需初始化或依赖定位坐标的仓库方法，前置条件缺失时按源端分支处理（改走其他查询，或走与声明一致的错误通道），不静默返回空集合](lesson-5c703b4b1128e37dbef5.lesson.md)
  - 时机：数据层实现阶段，为依赖上下文与运行时权限的枚举、查询类仓库方法编写前置失败分支（上下文未初始化、未授权、枚举失败）时；为依赖定位的附近列表确定无坐标、未授权时的查询分支与结果状态时
  - 情境：仓库方法依赖 UIAbilityContext 与运行时权限（如媒体读取）；规格或源端要求失败时由调用方显示错误提示，调用方靠捕获异常区分“出错”与“确实为空”的空态引导；方法还会把结果写入缓存。也包括依赖定位的附近列表：源端有权限且有坐标时按坐标加半径搜索，无权限或坐标未知时改按当前城市等条件查询；目标坐标可能未知，决策要求失败保持显式错误、不伪造空成功，而目标页面没有区分“出错”与“真空”的状态，空列表直接进入空态文案。
