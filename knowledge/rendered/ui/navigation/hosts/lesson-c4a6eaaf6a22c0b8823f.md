# main_pages.json 只登记经 router 进入或由 loadContent 按路径加载的 @Entry 页：被 Tabs/父页导入的子组件与 @CustomDialog 不登记，10905402 与 @Entry+export 警告先判定角色

## 何时使用

入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时

## 适用情境

源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。

## 原因

main_pages 的每个登记项都被当成路由页，必须恰有一个 @Entry。按 pages/ 目录全部登记，会让 Tab 子组件和弹窗背上路由页约束；为过编译给它们补 @Entry 又保留 export，形成 @Entry+export 角色冲突；去掉 export 又破坏父页导入，修复就在两者间摇摆。来源中弹窗漏补 @Entry 使构建失败，Tab 页的警告一直留到用户在 IDE 里看到；最终为消警告把 Tab 内容内联进主页时，又用只有标题和 TODO 的 builder 顶替了三个 Tab 页。

## 做法

1. 写 main_pages 前逐文件判定角色：被其他 .ets import 并在 Tabs 或父组件中实例化的 struct 是子组件（@Component export，不登记）；经 router.pushUrl 进入、或由 windowStage.loadContent / window.setUIContent 按路径加载的才是路由页（@Entry、不 export、登记）；@CustomDialog 由宿主页弹出，不登记。
2. 遇到 10905402 时，以 main_pages 实际 src 列表逐项检查：该文件被导入作子组件或是弹窗，就移除登记；确为路由页才补 @Entry，并去掉 export、确认没有导入方。若出于既有约束保留某弹窗的登记，就同时保证它恰有一个 @Entry，登记与装饰器一起改。
3. 同一内容既做 Tab 又要单独路由时，抽出 export 的 @Component 供 Tab 使用，另写 @Entry 外壳页包装它；不要用占位 builder 顶替原页面内容。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕WindowStage.loadContent、Window.loadContent 与 Window.setUIContent 按路径加载的页面，路径必须登记在 main_pages.json 里，并与其中 src 的取值完全一致，不支持相对路径写法；入口 Ability 加载的首页（如 pages/Index）虽然不经 router 进入，也必须登记。〔成立范围：对 Stage 模型下按路径加载页面的接口成立（FA 模型登记在 config.json）。不成立：loadContentByName 按 @Entry({ routeName }) 的命名路由名称加载，文档没有要求登记路径。〕
- 〔做法第 1 步〕onPageShow、onPageHide、onBackPress 只对 @Entry 装饰、作为页面加载的自定义组件生效；把原来的页面 struct 改成被 Tabs 或父组件实例化的子组件后，写在它里面的这三个回调不再被调用。它们声明在所有自定义组件的基类上，写在子组件里也能编译。〔成立范围：对 @Component 与 @ComponentV2 自定义组件都成立；依据是声明注释（works only for the custom components decorated by @Entry）和文档说明。不成立：NavDestination 页面的显隐与返回走 onShown、onHidden、onBackPressed，不用这三个回调。〕
- 〔做法第 2 步〕router 的 pushUrl（含 UIContext.getRouter() 上的同名方法）跳到没有登记在 main_pages.json 的页面时，在运行时以错误码 100002（Uri error）失败，replaceUrl 对应的错误码是 200002；url 是字符串，编译不检查。〔成立范围：对按 url 跳转的 router 接口成立；依据是声明里的错误码说明和文档 FAQ（router 跳转的页面要先加入 main_pages.json 的 pages 列表）。不成立：pushNamedRoute 按命名路由跳转，名称不存在时是 100004；NavPathStack 跳转不看 main_pages.json，没注册 builder 时只有 pushDestination、pushDestinationByName、replaceDestination 以 100005 失败，pushPath、pushPathByName 不返回错误码。〕
