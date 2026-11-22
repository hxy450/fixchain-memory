# 异步初始化里，用户可编辑的输入状态在第一个 await 之前写入初值；源端初始化本是同步的就保持同步，不加输入门控、不吞异常

## 何时使用

ViewModel 实现阶段，编排页面初始化方法中异步存储/SDK 绑定与输入状态初值的先后顺序时；切片实现阶段把源端构造器或 onCreate 里的同步初始化（取尺寸、解码位图、开局）移到组件生命周期，决定是否异步、怎样处理异常时

## 适用情境

源页面在初始化时同步写入关键词或输入框文本，操作读取实时输入；目标输入框双向绑定 ViewModel 字段，初始化方法内含 await（存储、历史、SDK 绑定），页面生命周期回调以不等待的方式调用它。 也包括源端在 Activity.onCreate 或自定义 View 构造器里同步完成取尺寸、初始化与位图解码，之后才接收输入，其中一条路径是规格要求照搬的未捕获异常崩溃；目标 SDK 对这些步骤同时提供 Promise 与 Sync 接口，写者准备在 aboutToAppear 里调用不等待的 async 启动函数、catch 只记日志，并用 booted/ready 标志拦截输入。

## 原因

页面不等初始化完成就可编辑；续体里较晚到达的初值赋值会覆盖用户已输入的文字，点击操作读到空值，表现为“点了没反应”。来源中写者读到源端先同步设置关键词与输入框，却把赋值放到 await 绑定之后；后续写者又在 await 链前插入更多异步步骤，顺序一直保留到返修。 把同步初始化改成生命周期回调里不等待的 async 函数后，其中抛出的异常变成被拒绝的 Promise，不再沿回调同步抛出；再包一层只写日志的 catch，源端会崩溃退出的路径就变成停在空白画面，ready 标志永不置位，输入全被丢弃。源端没有丢弃输入的行为，这种门控只是把异步窗口藏起来。

## 做法

1. 把源端同步设置的输入类状态（关键词、输入框文本、清除按钮可见性）放在第一个 await 之前赋值；异步步骤只加载数据，不在续体里回写用户可编辑字段。 先看源端初始化是否在构造器或 onCreate 里同步做完、之后才接收输入：是的话目标在生命周期回调（如 aboutToAppear）里按源顺序同步执行，SDK 同时有 Promise 与 Sync 变体时用 Sync 变体（写前在同一 interface 的 d.ts 里查，如 ImageSource.createPixelMapSync、resourceManager.getMediaContentSync、WindowStage.getMainWindowSync），不引入异步窗口，也不加“初始化完成前忽略输入”的门控。源端本来会抛出的异常（规格照搬的崩溃），从抛出函数到生命周期入口都不加 try/catch、Promise.catch，也不放进不被等待的 async 包装；工程也不注册 errorManager 的 'error' 观测器（注册后 JS_CRASH 由观测器接住，应用不退出）。
2. 确需在续体赋值时，先确认字段仍是进入时的值再写。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕aboutToAppear 在创建自定义组件新实例后、执行 build() 之前调用，声明为 aboutToAppear?(): void；在其中同步改的状态变量在随后的 build() 里生效
- 〔做法第 1 步〕ImageSource.createPixelMapSync(options?) 自 API 12 起提供，同步解码并返回 PixelMap，解码失败返回 undefined；同一接口里的 createPixelMap(options?) 返回 Promise<PixelMap>
- 〔做法第 1 步〕ResourceManager.getMediaContentSync(resId, density?) 自 API 10 起提供，同步返回媒体资源内容 Uint8Array
- 〔做法第 1 步〕WindowStage.getMainWindowSync() 自 API 9 起提供，同步返回主窗口；window.getLastWindow(ctx) 只有 callback 和 Promise 两种形式
- 〔做法第 1 步〕display.getDefaultDisplaySync() 自 API 9 起提供，同步返回应用所在屏幕的 Display
- 〔原因 / 做法第 1 步〕ArkTS 里抛出的错误沿调用栈向上传递，直到被最近的 try-catch 捕获；始终没有被捕获时程序终止
- 〔做法第 1 步〕errorManager.on('error', observer) 注册错误观测器后，应用产生的 JS_CRASH 由观测器捕获，此时应用不退出
- 〔原因 / 做法第 1 步〕目标 SDK 为 API 23 的设备上：工程没有注册 errorManager 的 'error' 观测器、aboutToAppear 里同步执行且整条链上没有 try/catch 的初始化抛出 TypeError 时，进程退出，hilog 的崩溃栈从抛出函数指回 aboutToAppear
- 〔原因〕目标 SDK 为 API 23 的设备上：aboutToAppear 不等待地调用 async 启动函数、函数体包在只写 hilog 的 try/catch 里时，其中抛出的 TypeError 被吞掉，经 JSON.stringify 记下的错误只剩「{}」；之后的 ready 标志一直没有置位，画面只有背景，触摸被门控全部丢弃
