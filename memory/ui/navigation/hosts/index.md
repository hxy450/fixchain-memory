# ui/navigation/hosts

Navigation/@Entry宿主与页面注册、嵌入页取栈、路由跳板和跨页面共享生命周期。

[上一级](../index.md)

## 本级经验

- [main_pages.json 只登记经 router 进入的 @Entry 页：被 Tabs/父页导入的子组件与 @CustomDialog 不登记，10905402 与 @Entry+export 警告先判定角色](lesson-c4a6eaaf6a22c0b8823f.lesson.md)
  - 时机：入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时
  - 情境：源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。
- [一进入就无条件跳转并 finish 的 Activity 是路由跳板：目标按同样条件直达实际页面，不把它的布局做成可见页](lesson-0b72c197ea20fbe6f277.lesson.md)
  - 时机：页面转换阶段迁移入口类 Activity、以及调用方为 Intent(X) 确定目标路由时
  - 情境：Android Activity 在 onCreate/initView 开头按条件 startActivity 到另一页并立即 finish()（如登录入口按配置转到短信登录或一键登录），它的布局文件仍含可渲染的按钮；多个调用方以 Intent 指向这个跳板 Activity。
- [入口页 Navigation 宿主：NavDestination 首屏只在 navDestination 映射中注册并压入同一栈，不作根内容；.navDestination 直接传 @Builder](lesson-8953e390416a80d7dd8c.lesson.md)
  - 时机：入口页实现或收尾接线阶段，创建 Navigation 宿主、决定首屏放在根内容还是压栈、编写 navDestination 分发时
  - 情境：目标入口页用 Navigation + @Provider NavPathStack 承载路由；首屏（启动页等）写成返回 NavDestination 的组件，在 onReady 取栈并按启动决策 pushPathByName 下一页；目的地由 @Builder 映射分发。
  - 例外：首屏是普通组件（不返回 NavDestination）、作为 Navigation 根内容常驻，且不依赖 NavDestinationContext 取栈
- [嵌在 Swiper/Tabs 里的页面组件只用 @Consumer 注入的根 NavPathStack，不在 onReady 用 context.pathStack 覆盖](lesson-1cebb531c991239d2691.lesson.md)
  - 时机：页面转换与主壳接线阶段，为由主页 Tab/Swiper 承载的 Fragment 页确定导航栈来源、编写 onReady 时；把已有页面接入主页 Swiper/Tabs 时
  - 情境：Android 主 Activity 用 ViewPager/底部 Tab 承载多个 Fragment；目标由入口页 Navigation 以 @Provider 提供根 NavPathStack，主页 Swiper 嵌入各 Tab 页组件，子页用 @Consumer('navPathStack') 取栈，外层仍保留 NavDestination 与 onReady；工程里经 pushPathByName 压栈的页面普遍在 onReady 写 this.navPathStack = context.pathStack。
  - 例外：页面本身经 pushPathByName 压入根栈、不在 Swiper/Tabs 子树内时，onReady 的 context.pathStack 就是根栈，该赋值无害
- [源端一个 Composable 内多屏共享的清理，拆成多页面后归属外层生命周期，切屏不释放](lesson-2ed8c21943925bf0ae9a.lesson.md)
  - 时机：规格提取与计划阶段，把源端 DisposableEffect/onDispose 等清理映射成目标多页面的生命周期契约时；实现阶段把共享服务的 stop/dispose 挂到页面回调时
  - 情境：源端单 Activity 在同一个 Composable 里用状态变量切换多个屏幕，播放器等资源和 DisposableEffect 清理挂在这个外层 Composable；目标端拆成 Navigation 下的多个页面，共享服务需要重新确定由哪一层、在什么时机停止和释放。
  - 例外：源端清理本就挂在单个屏幕自己的 Composable 上，切屏即离开组合，此时按该屏对应页面的退出处理
