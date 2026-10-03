# app

应用级入口与横切约定：入口 Ability 的初始化、平台级守护与 skills 声明，冷启动链路、启动去向与首屏就绪（含首页启动弹窗的数据源与守卫），账号退出与游客重建的本地清理，多模块（壳 HAP + HAR）的构建常量、跨模块导入与资源归属，Flutter 混合工程的原生桥接与 pub 插件替代，日志写法、应用身份、设置项、平台能力与厂商 SDK 选型（含蓝牙、常驻通知）、地图与定位 SDK 接入，服务卡片的尺寸取得与 form_config 配置，以及媒体保存/导入，以及资源批量转换（values 转 element JSON、drawable 转 media）的输出格式与命名，以及埋点上报引擎与 Android 业务基类横切行为的组合式承接，以及三方授权登录的回调归属

[上一级](../index.md)

## 子主题

- [account](account/index.md) — 账号会话：退出登录、账号注销与游客重建时要清理的本地状态、清理顺序（停同步、清表、广播）与计划验收
- [analytics](analytics/index.md) — 埋点与事件上报：埋点门面与 SPI 引擎列表中自有服务端上报引擎的移植与注册，三方统计 SDK 裁剪的适用范围
- [auth](auth/index.md) — 三方授权登录：授权会话与回调归属，迟到回调与失败收口
- [base-page](base-page/index.md) — Android 业务基类（BaseActivity、BaseBusinessActivity）横切行为迁到组合式 BasePage：生命周期埋点与返回归因、触摸分发与点外收键盘的逐方法映射与逐页接线
- [bluetooth](bluetooth/index.md) — 蓝牙能力：适配器开关状态的真值、门控与初始加载，分协议连接状态的聚合与成功判定，应用内开关蓝牙的方式，扫描等同步接口的抛错收敛与失败态
- [entry](entry/index.md) — 入口 Ability（onCreate/onDestroy）：基础设施的显式初始化时机、需要补上的平台级守护，以及 module.json5 中入口 Ability 的 skills（深链）声明、桌面快捷方式（shortcuts）声明与外部 Want 的入口分支
- [form](form/index.md) — 服务卡片：卡片页可用的事件与写法限制（@form 标注、V1 卡片页的派生值）、由 FormExtensionAbility 取实际尺寸并派生布局档位，以及 form_config 规格、缩放与刷新从源 appwidget-provider 换算
- [hybrid](hybrid/index.md) — Flutter 与原生混合工程：MethodChannel handler 的方法集合、flutter_boost 宿主页的事件通道、原生路由分流，以及 Flutter pub 插件在 OHOS 上的替代与本地兼容层
- [identity](identity/index.md) — 应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取，以及应用级图标引用与 AppScope 图标资源
- [logging](logging/index.md) — 日志：日志 API 选择与工程内的日志约定，按源端日志调用边界规划日志点与验收，诊断日志上传的打包内容与协议约束
- [map](map/index.md) — 地图与定位 SDK 接入（如高德鸿蒙 SDK）：各产品单例的隐私与 Key 初始化、查询参数契约、定位权限组的声明、申请与判定、逆地理编码补行政区名、定位结果到相机与坐标系转换、原生地图组件在 Tab 页中的生命周期与触摸分工
- [media](media/index.md) — 媒体与文件的用户可见性：SaveButton 安全控件的样式与授权时序、picker 导入导出、沙箱产物的导出、本地文件的播放 URI，以及按序浏览媒体时后续项的图片预取，以及长内容保存为图片时的快照尺寸限制与分段渲染
- [modules](modules/index.md) — 多模块工程（products 壳 HAP + features/components HAR）的边界：构建模式常量的来源、跨模块导入方式、页面迁入或移动时资源闭包的归属与按模块校验，按页面归属规划业务模块边界（不按功能编号或历史包名）；单模块内可复用函数不从路由页面模块导出，放进普通模块
- [platform](platform/index.md) — 系统平台能力（后台任务与扩展能力承载类、module.json5 extensionAbilities 的 type 登记，通知与常驻通知的订阅归属、画中画回退、动态取色、地图承载，打开系统设置的显式 Want）的实现、替代与降级，激励广告等能力门禁在能力不可用时的入口放行，厂商 SDK 鸿蒙版本的查询与选型，以及后台计时的恢复和退出清理，读当前系统值再增量写回的手势（亮度）读写映射，OAID 采集的跟踪授权
- [resources](resources/index.md) — 资源批量转换：Android values 转 element JSON（颜色值形态、数组项结构、引用写法）与 drawable 转 media（反编译 APK 的内联片段、资源文件名合法性），以及宣布资源阶段完成前的产物校验，以及快捷方式等图标的画布尺寸与图形显示区（低分辨率源图的处理）
- [settings](settings/index.md) — 设置项迁移：偏好键与默认值之外，每个开关的运行期消费方与应用入口；设置保存的副作用（远端、本地缓存、刷新事件）与切换即持久化界面状态的恢复
- [startup](startup/index.md) — 冷启动链路：闪屏路由与启动去向（固定进主页与按需登录的分工）、各去向页的初始化请求、登录态组合在哪里处理、首屏等待异步装配完成的就绪门，首启尚无已选项时的状态，加载页的可见时长，以及首页启动弹窗按源函数的接口与显示守卫，采集通道延后时启动门闩等待事件的超时兜底
