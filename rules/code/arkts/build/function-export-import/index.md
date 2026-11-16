# 跨文件复用的函数的导出和导入

agent 会看到什么：读到要复用的函数定义在 pages/ 下注册成路由的页面模块里、页面模块的导出注释写着只供 UT 消费，或源端 Kotlin object / Java 静态工具类以 X.method(...) 调用；产物里 import { … } from '…/pages/…'、为此新加的 export function，或 import { X } 和工具文件导出的顶层 export function 对不上

## 规矩

- rule-dedaff7bfaa3｜组件要复用路由页面模块里的函数时，先迁到普通模块再导入，不从页面模块导入｜读到：要复用的校验或工具函数定义在 pages/ 下经系统路由表或 pageMap 注册的页面模块里（文件里有供路由装配的 @Builder），工程另有 services/ 这类放共享逻辑的非页面目录；写错：新组件里写了 `import { … } from '../../pages/…'`，从页面模块导入非 UI 函数；或者页面模块为此把原本私有的 `function` 改成 `export function`
- rule-a3e1e0456859｜Kotlin object 或静态工具类改成顶层 export function 时，调用处改具名导入并去掉类名前缀｜读到：Kotlin `object X { fun … }` 或 Java 静态工具类，调用处写成 X.method(...)；写错：工具文件导出的是顶层 `export function`，调用处却写 import { X } from '…' 和 X.method(...)；编译报 10505001 has no exported member
