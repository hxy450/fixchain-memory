# app

应用级入口与横切约定：入口 Ability 的初始化、平台级守护与 skills 声明，系统配置变化的承接与跟随系统字号，冷启动链路、启动去向与首屏就绪（含首页启动弹窗的数据源与守卫），账号退出与游客重建的本地清理，构建模式常量与多模块（壳 HAP + HAR）的跨模块导入与资源归属，Flutter 混合工程的原生桥接与 pub 插件替代，日志写法、应用身份、设置项、平台能力与厂商 SDK 选型（含蓝牙、常驻通知）、地图与定位 SDK 接入，音视频播放服务的封装与播放页，服务卡片的尺寸取得与 form_config 配置，以及媒体保存/导入，以及资源批量转换（values 转 element JSON、drawable 转 media）的输出格式与命名，以及埋点上报引擎与 Android 业务基类横切行为的组合式承接，以及三方授权登录的回调归属，以及 NFC 前台派发与贴卡拉起入口，以及相机（CameraKit 会话、拍照录像产出与取景控制）

[上一级](../index.md)

## 子主题

- [account](account/index.md) — 账号会话：退出登录、账号注销与游客重建时要清理的本地状态、清理顺序（停同步、清表、广播）与计划验收；写操作的账号就绪守卫逐回调迁移与当前账号的响应式读取
- [analytics](analytics/index.md) — 埋点与事件上报：埋点门面与 SPI 引擎列表中自有服务端上报引擎的移植与注册，三方统计 SDK 裁剪的适用范围
- [auth](auth/index.md) — 三方授权登录：授权会话与回调归属，迟到回调与失败收口
- [base-page](base-page/index.md) — Android 业务基类（BaseActivity、BaseBusinessActivity）横切行为迁到组合式 BasePage：生命周期埋点与返回归因、触摸分发与点外收键盘的逐方法映射与逐页接线
- [bluetooth](bluetooth/index.md) — 蓝牙能力：适配器开关状态的真值、门控与初始加载，分协议连接状态的聚合与成功判定，应用内开关蓝牙的方式，扫描等同步接口的抛错收敛与失败态
- [camera](camera/index.md) — 相机功能迁移（Camera2 → CameraKit）：会话的输入输出组合、能力探测与拆卸重建，拍照与录像产出链（拍照桥接与多帧、保存与原生缓冲、元数据、限额与缺口下的失败路径），取景控制（手动参数单位、预览居中与拍照旋转）
- [entry](entry/index.md) — 入口 Ability 与应用级配置：onCreate/onDestroy 中基础设施的显式初始化时机、需要补上的平台级守护，系统配置变化（源 Activity 未声明 configChanges 时的重建语义，含旋转、非托管对话框与 NonConfigurationInstance 取回）在 onConfigurationUpdate 与页面中的承接与跟随系统字号的 configuration，以及 module.json5 中入口 Ability 的 skills（深链、App Links 的 domainVerify）声明、桌面快捷方式（shortcuts）声明与外部 Want 的入口分支；冷启动首帧前按偏好同步恢复主题的时机；进程回收后页面栈恢复（setRestoreEnabled、restoreWindowStage、recoverable）；AndroidManifest 各 intent-filter 到 skills 的逐条映射与入口载荷键；System.exit 式重启迁为 restartApp 并携带界面状态；被第三方拉起并回传结果的入口（terminateSelfWithResult 单一出口）、singleton 入口经 onNewWant 收到的新请求的观察与重放、外部一次性请求在设备就绪回调中消费
- [form](form/index.md) — 服务卡片：卡片页可用的事件与写法限制（@form 标注、V1 卡片页的派生值）、由 FormExtensionAbility 取实际尺寸并派生布局档位，以及 form_config 规格、缩放与刷新从源 appwidget-provider 换算
- [hybrid](hybrid/index.md) — Flutter 与原生混合工程：MethodChannel handler 的方法集合、flutter_boost 宿主页的事件通道、原生路由分流，以及 Flutter pub 插件在 OHOS 上的替代与本地兼容层
- [identity](identity/index.md) — 应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取，以及应用级图标引用与 AppScope 图标资源，以及启动窗图标与底色，以及 productFlavors 工程按选定 flavor 解析身份串
- [logging](logging/index.md) — 日志：日志 API 选择与工程内的日志约定，按源端日志调用边界规划日志点与验收，诊断日志上传的打包内容与协议约束；由构建配置决定是否启用的崩溃上报等采集通道的迁移范围
- [map](map/index.md) — 地图与定位 SDK 接入（如高德鸿蒙 SDK）：各产品单例的隐私与 Key 初始化、查询参数契约、定位权限组的声明、申请与判定、逆地理编码补行政区名、定位结果到相机与坐标系转换、原生地图组件在 Tab 页中的生命周期与触摸分工
- [media](media/index.md) — 媒体与文件的用户可见性：SaveButton 安全控件的样式与授权时序、picker 导入导出、沙箱产物的导出、本地文件的播放 URI，以及按序浏览媒体时后续项的图片预取，以及长内容保存为图片时的快照尺寸限制与分段渲染；保存到相册或文件的权限、URI 取 fd 与下载任务生命周期；本应用最近媒体以自身保存的 URI 为准（整库查询的读权限）、带系统确认框接口的用户取消与失败区分、查看或分享媒体的 Want 类型与读授权
- [modules](modules/index.md) — 构建模式常量与多模块工程（products 壳 HAP + features/components HAR）的边界：BuildConfig.DEBUG 映射为 hvigor 生成的 BuildProfile.DEBUG、HAR 中构建模式的来源，跨模块导入方式、页面迁入或移动时资源闭包的归属与按模块校验，按页面归属规划业务模块边界（不按功能编号或历史包名）；单模块内可复用函数不从路由页面模块导出，放进普通模块
- [nfc](nfc/index.md) — NFC：Android Activity 级前台派发到 UIAbility 注册与可见页登记的仿真，清单声明的贴卡拉起入口（TAG_FOUND skills）及其运行时启停开关的作用范围；读卡入口前能力检查的不支持、已关闭、可用三分支
- [platform](platform/index.md) — 系统平台能力（后台任务与扩展能力承载类、module.json5 extensionAbilities 的 type 登记，通知与常驻通知的订阅归属、画中画回退、动态取色、地图承载，打开系统设置的显式 Want）的实现、替代与降级，激励广告等能力门禁在能力不可用时的入口放行，厂商 SDK 鸿蒙版本的查询与选型，以及后台计时的恢复和退出清理，读当前系统值再增量写回的手势（亮度）读写映射，OAID 采集的跟踪授权；权限清单按已映射 API 在 d.ts 中的 @permission 汇总；画中画到 PiPWindow、动态取色到 wallpaper 的映射，后台计时与进度通知的降级边界，通知按钮 WantAgent 的 requestCode 与正文非空；AlarmManager 到点通知改用代理提醒时的按钮路由、贪睡与失败回退，通知 builder 默认图标；拉起系统能力前的可用性预检、权限申请与无接收方回退（canOpenLink、querySchemes）
- [playback](playback/index.md) — 音视频播放：AVPlayer 封装的异步装载并发与停止复位、错误通道与 Promise 拒绝，应用包 rawfile 资源经 fdSrc 设源，封装类释放方法按重载与宿主销毁分开，控制门面同步路径的回退来源，跨实现组合切换步骤时的入口守卫，视频页 surface 绑定与画面比例；短提示音的音频并发（混播/焦点）与播放中重入；源端 SoundPool 短音效改用 media.SoundPool；退后台继续播放所需的 AVSession 与音频长时任务；需要缓冲态、缓冲位或共享播放器时 AVPlayer + XComponent 与 Video 组件的取舍
- [resources](resources/index.md) — 资源批量转换：Android values 转 element JSON（颜色值形态与 #AARRGGBB 字节序、数组项结构、引用写法）与 drawable 转 media（VectorDrawable 转 SVG 的 viewBox 与显示尺寸、反编译 APK 的内联片段、资源文件名合法性），以及宣布资源阶段完成前的产物校验，以及快捷方式等图标的画布尺寸与图形显示区（低分辨率源图的处理），以及自适应图标转分层图标的图层尺寸与可见区裁切，以及 strings.xml 转 string.json 的 aapt2 编译语义（转义、引号、空白）与内联样式标记的保留；Compose Material 库图标（Rounded 等变体）的矢量来源；语言限定目录只放源端有的文字资源类型（键集审计不复制非文字资源）
- [settings](settings/index.md) — 设置项迁移：偏好存储的同步装载与读写时序，偏好键与默认值（同一键按读点的不同缺省值）之外，每个开关的运行期消费方与应用入口；onPreferenceChange 返回值决定的落值时刻与验证补偿；设置保存的副作用（远端、本地缓存、刷新事件）与切换即持久化界面状态的恢复，应用内语言切换的即时生效；应用壳下传的页面显示设置：占位初值来源与壳层一次计算的派生判定；只改会话字段的选项不建偏好键，以 null 区分缺键而空串合法时的存在性判断
- [startup](startup/index.md) — 冷启动链路：闪屏路由与启动去向（固定进主页与按需登录的分工）、各去向页的初始化请求、登录态组合在哪里处理、首屏等待异步装配完成的就绪门，首启尚无已选项时的状态，加载页的可见时长，以及首页启动弹窗按源函数的接口与显示守卫，采集通道延后时启动门闩等待事件的超时兜底
