# main_pages.json 只登记经 router 进入或由 loadContent 按路径加载的 @Entry 页：被 Tabs/父页导入的子组件与 @CustomDialog 不登记，10905402 与 @Entry+export 警告先判定角色

## 何时使用

入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时

## 适用情境

源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。工程改用 Navigation 路由时，经 NavPathStack 进入的 NavDestination 子页注册在 navDestination 映射或系统路由表 router_map.json 里，同样不是 main_pages 的登记对象，不为它们补 @Entry；main_pages 只留按路径加载的入口页和仍经 router 进入的页。

## 原因

main_pages 的每个登记项都被当成路由页，必须恰有一个 @Entry。按 pages/ 目录全部登记，会让 Tab 子组件和弹窗背上路由页约束；为过编译给它们补 @Entry 又保留 export，形成 @Entry+export 角色冲突；去掉 export 又破坏父页导入，修复就在两者间摇摆。来源中弹窗漏补 @Entry 使构建失败，Tab 页的警告一直留到用户在 IDE 里看到；最终为消警告把 Tab 内容内联进主页时，又用只有标题和 TODO 的 builder 顶替了三个 Tab 页。

## 做法

1. 写 main_pages 前逐文件判定角色：被其他 .ets import 并在 Tabs 或父组件中实例化的 struct 是子组件（@Component export，不登记）；经 router.pushUrl 进入、或由 windowStage.loadContent / window.setUIContent 按路径加载的才是路由页（@Entry、不 export、登记）；@CustomDialog 由宿主页弹出，不登记。
2. 遇到 10905402 时，以 main_pages 实际 src 列表逐项检查：该文件被导入作子组件或是弹窗，就移除登记；确为路由页才补 @Entry，并去掉 export、确认没有导入方。若出于既有约束保留某弹窗的登记，就同时保证它恰有一个 @Entry，登记与装饰器一起改。
3. 同一内容既做 Tab 又要单独路由时，抽出 export 的 @Component 供 Tab 使用，另写 @Entry 外壳页包装它；不要用占位 builder 顶替原页面内容。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕编译错误 10905402 表示 main_pages.json 或 build-profile.json5 里登记的页面没有 @Entry；登记的页面必须有且仅有一个 @Entry 生效，一个页面里有多个 @Entry 时报的是 10905231
- 〔原因 / 做法第 1 步〕module.json5 的 pages 指向的页面列表里，src 每一项都是当前 Module 的一个页面的路由信息（页面路径以 src/main/ets 为基准），会被当作 UI 页面入口
- 〔原因〕@Entry 装饰的 struct 同时带 export 时编译给出警告；去掉 export 后，仍 import 它的父页编译失败
- 〔做法第 2 步〕已登记在 main_pages.json 的 @CustomDialog 文件在 @CustomDialog 前补上 @Entry、登记不动时，同次编译通过
