# app/cross-cutting

源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线

[上一级](../index.md)

## 本级经验

- [基类横切行为逐方法映射，按子类布局核守卫再接线](lesson-2fcb6612ee4106b34e17.lesson.md) · 阶段：execute · 信号：BaseActivity, BaseBusinessActivity, dispatchTouchEvent, onBackPressed
- [开关控制的常驻通知由应用级服务持有，不随页面 VM](lesson-e9f03fcc7f1e781c4b24.lesson.md) · 阶段：spec/execute · 信号：notificationManager.publish, aboutToAppear, aboutToDisappear, NavDestination
- [新增错误日志沿用 hilog 约定，不写 console.*](lesson-11e9d15d947b30d2ce7e.lesson.md) · 阶段：execute · 信号：hilog.error, console.log, @kit.PerformanceAnalysisKit, DOMAIN
- [日志迁移审计按源端调用边界列日志点，不只核对配置](lesson-e23468a0e439f8cf53e9.lesson.md) · 阶段：plan/execute/verify · 信号：log2File, debugFile, BqLog, hilog.info
- [自有服务端埋点引擎按源码移植并在门面注册](lesson-dc3ac0500599ef7c9636.lesson.md) · 阶段：execute · 信号：ServiceLoader, ApiService, http.createHttp, Tracker
- [设置开关逐项落实运行期消费方，只调 setter 不算完成](lesson-4d0f0176b3d09c33f1eb.lesson.md) · 阶段：execute · 信号：DataStore, SharedPreferences, preferences, @ObservedV2
- [诊断日志上传按源端打包清单与协议实现，收窄先确认](lesson-d434bb5c16bc721d9a00.lesson.md) · 阶段：spec/execute/verify · 信号：usesCleartextTraffic, networkSecurityConfig, presignedUrl, http.request
- [退出登录先停同步再单事务清账号业务表并广播](lesson-8b8e304a737e9fded451.lesson.md) · 阶段：plan/execute · 信号：clearAllTables, RelationalStore, preferences, accessToken
