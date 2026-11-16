# 规格权限节对跨栈映射里每个目标 API 反查 @permission，不只从源 Manifest 推

审的是：规格
触发（任一种）：
- 读到：源能力在安卓上无需权限，源 Manifest 只有少量或未用的权限；跨栈映射写了 FLAG_SECURE → setWindowPrivacyMode；写错的样子：权限节、决策台账写「目标不声明任何权限」，或静态验收写「module.json5 无 requestPermissions 条目」，没核各目标 API 的 @permission
- 读到：源端用无需权限的 SensorManager（加速度计、陀螺仪）或删除 MediaStore 条目，Manifest 里没有对应权限；写错的样子：权限节写「逐项映射 manifest」、WRITE_EXTERNAL_STORAGE「不需要」；跨栈表已映射 @ohos.sensor，权限节却没有 ACCELEROMETER / GYROSCOPE、WRITE_IMAGEVIDEO
适用范围：规格提取时写 module.json5 的权限契约（权限节、静态验收、决策台账）时
做法：
- 对跨栈映射里每个目标 API 查 SDK d.ts 的 @permission，逐项写进权限节；源 Manifest 只说明源端声明过什么，未核实前不写「不需要」「不申请」「不声明任何权限」
- 例：FLAG_SECURE → setWindowPrivacyMode 要 PRIVACY_WINDOW；sensor.on 加速度计、陀螺仪要 ACCELEROMETER / GYROSCOPE；deleteAssets 和图库写入要 WRITE_IMAGEVIDEO
- 写「requestPermissions 为空」一类静态验收前，逐个核规格列出的系统能力面的 @permission，有一个带权限就不写全空；只约束某类权限的验收不扩成全空
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowPrivacyMode(isPrivacyMode: boolean): Promise<void>，@permission ohos.permission.PRIVACY_WINDOW，缺权限时抛 201：FLAG_SECURE 的目标 API 需要声明权限（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowPrivacyMode）
- ohos.permission.PRIVACY_WINDOW：权限级别 normal，授权方式 system_grant（API 9-10 为 system_basic，API 11 起 normal）：写进权限契约时只需声明，不涉及运行时申请（出处：permissions-for-all.md，ohos.permission.PRIVACY_WINDOW）
- FLAG_SECURE：把窗口内容当作安全内容，不出现在截屏里：源端只是窗口标志，安卓上不需要权限（出处：android.view.WindowManager.LayoutParams#FLAG_SECURE）
- function on(type: SensorId.ACCELEROMETER, callback: Callback<AccelerometerResponse>, options?: Options): void，@permission ohos.permission.ACCELEROMETER，无权限抛 201：订阅加速度计要声明权限（出处：鸿蒙 SDK 的 ets/api/@ohos.sensor.d.ts，sensor.on）
- function on(type: SensorId.GYROSCOPE, callback: Callback<GyroscopeResponse>, options?: Options): void，@permission ohos.permission.GYROSCOPE：订阅陀螺仪要声明权限（出处：鸿蒙 SDK 的 ets/api/@ohos.sensor.d.ts，sensor.on）
- static deleteAssets(context: Context, uriList: Array<string>): Promise<void>，@permission ohos.permission.WRITE_IMAGEVIDEO，无权限抛 201：删除媒体资源要写图库权限；另有按 Array<PhotoAsset> 的重载，权限相同（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetChangeRequest.deleteAssets）
- ACCELEROMETER、GYROSCOPE：权限级别 normal，系统授权（system_grant）：只要在 module.json5 声明，不需要运行时弹窗（出处：permissions-for-all.md，ohos.permission.ACCELEROMETER、ohos.permission.GYROSCOPE）
- WRITE_IMAGEVIDEO：受限权限，权限级别 system_basic，用户授权（user_grant）：要声明、要运行时请求，还要按受限权限的流程申请（出处：restricted-permissions.md，ohos.permission.WRITE_IMAGEVIDEO）
未核实：case-68b4a8d96f961e70b0c9 的环境是鸿蒙 6.1.1(24)，本机按 API 23 核对
来源：2 张卡，2 个应用
- case-0524405ca4510433cf06（GameOfLife）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2、建议 1
- case-68b4a8d96f961e70b0c9（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
