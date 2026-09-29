# app

应用级入口与横切约定：入口 Ability 的初始化、平台级守护与 skills 声明，冷启动链路与首屏就绪，Flutter 混合工程的原生桥接，日志写法、应用身份、设置项、平台能力与厂商 SDK 选型（含蓝牙、常驻通知）、地图与定位 SDK 接入，以及媒体保存/导入，以及资源批量转换（values 转 element JSON、drawable 转 media）的输出格式与命名

[上一级](../index.md)

## 子主题

- [bluetooth](bluetooth/index.md) — 蓝牙能力：适配器开关状态的真值、门控与初始加载，分协议连接状态的聚合与成功判定，应用内开关蓝牙的方式，扫描等同步接口的抛错收敛与失败态
- [entry](entry/index.md) — 入口 Ability（onCreate/onDestroy）：基础设施的显式初始化时机、需要补上的平台级守护，以及 module.json5 中入口 Ability 的 skills（深链）声明
- [hybrid](hybrid/index.md) — Flutter 与原生混合工程：MethodChannel handler 的方法集合、flutter_boost 宿主页的事件通道、原生路由分流
- [identity](identity/index.md) — 应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取
- [logging](logging/index.md) — 日志 API 选择与工程内的日志约定
- [map](map/index.md) — 地图与定位 SDK 接入（如高德鸿蒙 SDK）：各产品单例的隐私与 Key 初始化、查询参数契约、定位权限组的声明、申请与判定、逆地理编码补行政区名、定位结果到相机与坐标系转换、原生地图组件在 Tab 页中的生命周期与触摸分工
- [media](media/index.md) — 媒体与文件的用户可见性：SaveButton 安全控件的样式与授权时序、picker 导入导出、沙箱产物的导出、本地文件的播放 URI
- [platform](platform/index.md) — 系统平台能力（后台任务、通知与常驻通知的订阅归属、画中画回退、动态取色、地图承载）的实现、替代与降级，厂商 SDK 鸿蒙版本的查询与选型，以及后台计时的恢复和退出清理
- [resources](resources/index.md) — 资源批量转换：Android values 转 element JSON（颜色值形态、数组项结构、引用写法）与 drawable 转 media（反编译 APK 的内联片段、资源文件名合法性），以及宣布资源阶段完成前的产物校验
- [settings](settings/index.md) — 设置项迁移：偏好键与默认值之外，每个开关的运行期消费方与应用入口
- [startup](startup/index.md) — 冷启动链路：闪屏路由、各去向页的初始化请求、登录态组合在哪里处理、首屏等待异步装配完成的就绪门，首启尚无已选项时的状态，以及加载页的可见时长
