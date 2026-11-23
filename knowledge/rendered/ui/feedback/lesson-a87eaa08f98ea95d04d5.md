# 同一业务链有多个入口时，每个入口都要真正调用服务并在所有终态收口 loading

## 何时使用

界面接线阶段，为同一业务链实现“弹窗确认”与“无弹窗直调”等多个入口，并编写忙态（loading）的起链与收口时

## 适用情境

源端工具方法显示 loading 后直接下载或设置，并在各终态关闭；目标把链路拆成弹窗组件加静态入口方法，服务调用需要 UI context，而 context 只在组件按钮回调里拿得到。

## 例外与边界

- 带确认弹窗的入口，打开弹窗时只置 visible、在确认回调里才显示 loading 并调用服务，是正确的起链方式；不要为了“入口直接调用服务”去掉确认弹窗或在打开时就调服务，用户在弹窗里取消时也不应出现 loading

## 原因

入口若只置 busy/visible 状态而不起链，loading 永不收口（一直显示“设置中”）；方法名和注释写着“直接设置”，路由核验按名字判定已接通也发现不了。

## 做法

1. 逐个入口列出“显示 loading → 调用服务 → 终态收口”三步，确认每个入口都真正调用了服务。
2. 入口是静态方法或全局状态单例、服务需要 UI context 时，在入口签名里显式注入 context（文件选择器一类服务只接受 UIAbilityContext，可由组件的 getUIContext().getHostContext() 取得）与结果回调（或由挂载组件监听请求后起链），不让忙态依赖只在按钮回调里才有的 context。
3. 按“loading 在任一终态恰好收口一次”走查：每个 busy=true 都能经服务终态到达 busy=false。
4. 接线或路由核验时打开方法体确认服务调用与收口存在，不凭方法名或注释判定已接通。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕picker.DocumentViewPicker、picker.AudioViewPicker 的 constructor(context) 只支持 UIAbilityContext 作参数，声明注释指向用 getHostContext 取得这个 context
