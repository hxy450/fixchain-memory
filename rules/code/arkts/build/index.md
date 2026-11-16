# 构建与模块

源端有 BuildConfig 字段，或交回的代码涉及 BuildProfile、HAR 模块、跨模块和跨文件的 import / export、新建的常量类文件，或为修编译错误改过文件时

## 触发族

- [BuildConfig 的构建字段（DEBUG、VERSION_NAME、VERSION_CODE）](buildconfig-fields/index.md)（3 条）：读到源端条件或页面用 BuildConfig.DEBUG、BuildConfig.VERSION_NAME / VERSION_CODE；交回的表达式删掉了 DEBUG 腿、没有 BuildProfile.DEBUG，或版本号抄成了页面常量
- [新建的主题令牌、常量类 .ets 文件](new-token-class-file/index.md)（2 条）：读到派工要求新建主题令牌类（DesignTokens 一类）或示例用 static readonly X = { … } 承载令牌；交回的令牌类写了无类型的对象字面量，或新文件没被任何页面 import 却报告全量构建通过
- [HAR 模块里的 BuildProfile 和跨模块导入](har-buildprofile-import/index.md)（4 条）：读到或产物里 HAR 模块的 .ets 有 import { DEBUG } from 'BuildProfile'、if (DEBUG && …) 门控、跨模块的 import 路径，或宿主入口调用下沉到 HAR 的服务 initialize()
- [为修编译错误改过的文件](build-error-fix/index.md)（2 条）：读过的构建日志只报 import / export、@Entry 或某个符号未导出（has no exported member、not exported）；交回的修复改动超出报错处：整文件重写换掉了没报错的组件写法，或删掉了整块功能
- [禁编译时一次写出的整页文件](no-compile-page/index.md)（1 条）：读过的派工写「禁止任何编译/构建」、要一次写出整页 @ComponentV2 文件；交回的代码引用了没有 const 声明的大写常量，或没有 @Local / @Param / private 声明的 this. 成员
- [被搬页面归到哪个模块](page-module-placement/index.md)（1 条）：读到被搬的页面 import 了某业务模块的 ViewModel 或 Service，入口却是另一模块列表页的条目跳转；产物里页面按 import 移进那个模块，同一业务对象的列表、新增、详情页和 Model、Service、ViewModel 分在两个模块
- [跨文件复用的函数的导出和导入](function-export-import/index.md)（2 条）：读到要复用的函数定义在 pages/ 下注册成路由的页面模块里、页面模块的导出注释写着只供 UT 消费，或源端 Kotlin object / Java 静态工具类以 X.method(...) 调用；产物里 import { … } from '…/pages/…'、为此新加的 export function，或 import { X } 和工具文件导出的顶层 export function 对不上
- [编译报错后删改的调用和基类](compile-fix-stale-comment/index.md)（2 条）：读到编译报错指向承载核心行为的调用或扩展基类（卡片页 .onAreaChange 报 can't support form application、@kit.AbilityKit 没有 ServiceExtensionAbility）；产物里为过编译删了调用或改了 extends，文件头和注释仍写着由它驱动或旧的注册 type，被它赋值的 @State 只剩声明
- [循环导入和顶层继承的初始化顺序](circular-import/index.md)（1 条）：产物里新加 import { X } from M 并 class … extends X（或在模块顶层、类静态初始化里用 X），而 M 直接或间接 import 回本文件，运行时报 ReferenceError: X is not initialized
