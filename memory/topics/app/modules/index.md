# app/modules

多模块（壳 HAP + HAR）边界：构建常量来源、跨模块导入、资源闭包归属与可复用函数的模块放置

[上一级](../index.md)

## 本级经验

- [HAR 不引宿主 BuildProfile，模式由壳层注入](lesson-6bd9ae0de39cecc06744.lesson.md) · 阶段：execute/repair · 信号：BuildProfile, assembleHap, Index.ets, oh-package.json5
- [业务模块拆分按页面归属建表，不以源包分组为边界](lesson-99b35920e77ae01076ea.lesson.md) · 阶段：plan/execute · 信号：pageMap, NavPathStack, oh-package.json5, features/
- [共用非 UI 函数迁到普通模块，不从路由页面模块导出](lesson-b58f26f0fdb7fb00db9e.lesson.md) · 阶段：execute · 信号：pages/, pageMap, services/, utils/
- [页面迁入 HAR 时带走 $r 与按名取资源的资源闭包](lesson-edb937b04e0f1494ca37.lesson.md) · 阶段：execute · 信号：$r, getStringByNameSync, Unknown resource name, oh-package.json5
