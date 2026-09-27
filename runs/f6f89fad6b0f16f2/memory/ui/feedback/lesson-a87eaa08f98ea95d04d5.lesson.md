# 同一业务链有多个入口时，每个入口都要真正调用服务并在所有终态收口 loading

ID：`lesson-a87eaa08f98ea95d04d5` · 版本：1

[本主题](index.md)

## 何时使用

界面接线阶段，为同一业务链实现“弹窗确认”与“无弹窗直调”等多个入口，并编写忙态（loading）的起链与收口时

## 适用情境

源端工具方法显示 loading 后直接下载或设置，并在各终态关闭；目标把链路拆成弹窗组件加静态入口方法，服务调用需要 UI context，而 context 只在组件按钮回调里拿得到。

## 原因

入口若只置 busy/visible 状态而不起链，loading 永不收口（一直显示“设置中”）；方法名和注释写着“直接设置”，路由核验按名字判定已接通也发现不了。

## 做法

1. 逐个入口列出“显示 loading → 调用服务 → 终态收口”三步，确认每个入口都真正调用了服务。
2. 入口是静态方法或全局状态单例、服务需要 UI context 时，在入口签名里显式注入 context 与结果回调（或由挂载组件监听请求后起链），不让忙态依赖只在按钮回调里才有的 context。
3. 按“loading 在任一终态恰好收口一次”走查：每个 busy=true 都能经服务终态到达 busy=false。
4. 接线或路由核验时打开方法体确认服务调用与收口存在，不凭方法名或注释判定已接通。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-879046ceea442517d7ce · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`0fba79e7737f3feb8e7ec486cf0b7fe78f0f8cc7d5d039c7c4f2a4d1538ceb06`
