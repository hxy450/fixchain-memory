# 单 Activity 壳内的 loadChildFragment 子页映射为壳内回退栈，不改成独立路由或清栈切页

## 何时使用

壳层导航实现与页面形态决策阶段，为源端在内容区压栈加载、且子页期间底栏等壳元素仍可见的子 Fragment 确定承载方式、返回与底部导航选中语义时

## 适用情境

源主 Activity 用 loadChildFragment（hide 加 add 加 addToBackStack）打开详情、搜索等子页，子页期间底栏与迷你播放条仍在，工具栏随栈深显示上箭头，带 navigationTag 时同步底栏选中；启动器构造时写入默认 extras。目标同时有 Navigation 路由与壳内容槽。

## 例外与边界

- 返回时要回到上一页原来的样子：源端 hide 只隐藏上一页、不销毁，弹栈后显示的是同一个实例（输入、滚动位置、已加载的数据都在）；壳内容区若用 if/else 按 tag 切换，切走的分支组件会被删除、其中的状态随之丢失，需保留上一页的组件实例，或把要恢复的状态放在壳状态里随子栈一起记录。

## 原因

把子页做成 NavDestination 路由会离开壳（失去底栏与迷你条），改成清栈切页会丢失返回路径与上箭头；登记中的错误提示可能与规格冲突。

## 做法

1. 壳状态维护子回退栈（入栈记录上一页 tag 与参数），清栈入口清空它；返回键与上箭头先弹子栈，再走默认页、抽屉、退出分支；navigationTag 非空时覆盖底栏选中。
2. 页面元数据为子组件且源经 loadChildFragment 打开的页，转换为以 @Param 接参数的可嵌入组件，由壳内容区按 tag 承载，不以已存在页面的先例覆盖。
3. 调用点按源 API 区分 loadFragment（清栈并持久化）与 loadChildFragment（压栈）；映射启动器时核对构造器写入的默认 extras；登记提示与规格冲突时以规格为准。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕FragmentTransaction.addToBackStack 让事务在提交后被记住，之后从回退栈弹出时反向执行这次事务的操作（框架 android.app 版）
- 〔适用情境 / 原因〕FragmentTransaction.hide 只隐藏一个已存在、视图已加到容器里的 Fragment，不销毁它（框架 android.app 版）
- 〔做法第 3 步〕Intent.getBooleanExtra(name, defaultValue) 返回此前 putExtra 放入的值；没有放入该键时才返回 defaultValue
