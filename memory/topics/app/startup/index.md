# app/startup

冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫

[上一级](../index.md)

## 本级经验

- [启动弹窗按源函数接口与显示守卫实现不换列表接口](lesson-bbb31db6c369047ee32c.lesson.md) · 阶段：execute · 信号：@GET, Retrofit, CustomDialog, promptAction.openCustomDialog
- [延后采集通道时单独移植超时兜底发布就绪事件](lesson-99a8d47085e4b1ae44de.lesson.md) · 阶段：spec/execute · 信号：OaidResultEvent, Observable.timer, FWD-REF, OAID
- [持久化主题在 loadContent 前同步设好](lesson-dcb3c5e66dec2d126234.lesson.md) · 阶段：spec/execute · 信号：ApplicationContext.setColorMode, setColorMode, getPreferencesSync, loadContent
- [源端启动固定进主页时目标也进主页，登录页压在其上](lesson-4c254d10ef9264683c55.lesson.md) · 阶段：spec/execute · 信号：SplashActivity, NavPathStack, pushPathByName, LoginGuard
- [目标初始化极快时把首启加载页最短可见时长写进验收](lesson-41bb62cd13921e4eedde.lesson.md) · 阶段：spec/plan/execute · 信号：SplashActivity, SplashScreen, windowStage.loadContent, setTimeout
- [迁启动链路时列出各去向页初始化请求与登录态组合](lesson-8c24f05ec8df45401482.lesson.md) · 阶段：spec/execute · 信号：initRequestData, SplashActivity, MainActivity, refreshToken
- [首启无已选项时定义显式空态，不以空编码请求](lesson-95aa64d6b0a5c041d326.lesson.md) · 阶段：spec/execute/verify · 信号：hasInit, selectedCity, cityCode, preferences
- [首屏依赖异步装配服务时用可复位就绪门await后路由](lesson-ccbf0a7f5b1809ef5880.lesson.md) · 阶段：execute · 信号：EntryAbility.onCreate, loadContent, onReady, Promise
