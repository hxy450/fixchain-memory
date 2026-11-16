# 源端构造器里同步做完的初始化，目标在 aboutToAppear 按源顺序同步执行并用 Sync 接口

审的是：代码
触发（任一种）：
- 读到：源端自定义 View 构造器或 Activity.onCreate 里同步完成取尺寸、初始化、BitmapFactory.decodeResource / createScaledBitmap，之后才接收输入；写错的样子：目标改成 await source.createPixelMap()、await window.getLastWindow(...) 的 async 启动，并加 if (!this.booted) return 这类「初始化完成前忽略输入」的门控
适用范围：把源端构造器或 onCreate 里的同步初始化移到组件生命周期时
做法：
- 在 aboutToAppear 里按源端顺序同步执行各步；SDK 同一 interface 里同时有 Promise 和 Sync 变体的用 Sync 变体（如 createPixelMapSync、getMediaContentSync、getMainWindowSync）
- 不为接口的异步形式引入初始化窗口，不加源端没有的忽略输入门控，删掉只为异步竞争服务的标志
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- createPixelMapSync(options?: DecodingOptions): PixelMap（@since 12），解码失败返回 undefined：ImageSource 的同步解码，和 Promise 版 createPixelMap 并列（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，ImageSource.createPixelMapSync）
- createPixelMap(options?: DecodingOptions): Promise<PixelMap>：异步版本，不要用它替代源端同步解码（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，ImageSource.createPixelMap）
- getMediaContentSync(resId: number, density?: number): Uint8Array：同族接口：ResourceManager 同步取媒体资源字节（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getMediaContentSync）
- getMainWindowSync(): Window（@since 11）：同族接口：WindowStage 同步取主窗口；window.getLastWindow 只有 Promise 形式（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，WindowStage.getMainWindowSync；window.getLastWindow）
- function getDefaultDisplaySync(): Display：同族接口：同步取默认屏幕尺寸（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.getDefaultDisplaySync）
- aboutToAppear 同步执行测尺寸 → 首帧 → 初始化 → 装载位图，位图改用 createPixelMapSync，删掉 booted 门控：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端初始化的顺序：源工程 Activity.onCreate 和自定义 View 构造器（.java / .kt）；按调用顺序列出各步，确认其中没有回调、线程或 Future，目标照这个顺序同步写
来源：1 张卡，1 个应用
- case-bc452cbde49f74ef19a3（Bubble Shooter）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 6 ← 诊断
