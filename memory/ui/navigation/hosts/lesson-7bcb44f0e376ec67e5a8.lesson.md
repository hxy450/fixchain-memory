# 源壳在内容容器内以 hide+add+addToBackStack 打开子页、底栏仍可见时，子页留在壳内并由壳维护回退栈

ID：`lesson-7bcb44f0e376ec67e5a8` · 版本：2

[本主题](index.md)

## 何时使用

壳层导航实现与页面形态决策阶段，为源端在主 Activity 内容区压栈加载的子 Fragment 确定承载方式、返回与底部导航选中语义时

## 适用情境

源主 Activity 在内容容器内用 FragmentTransaction 的 hide(当前) + add(子页) + addToBackStack 打开详情、搜索等子页（项目封装名如 loadChildFragment），子页期间底栏、迷你播放条等壳元素仍在，工具栏随回退栈深度显示上箭头，可能按子页标签同步底栏选中；另有 replace 并清栈的切页入口（如 loadFragment）。目标同时有 Navigation 路由与壳内容槽。

## 例外与边界

- 源端子页以新 Activity 或替换整个壳的方式打开（底栏不可见）时，按普通路由页处理

## 原因

把壳内压栈的子页做成 NavDestination 路由会离开壳，失去底栏与常驻条；改成清栈切页又丢掉返回路径与上箭头。

## 做法

1. 按调用点的方法体而不是方法名区分：只 replace 并清回退栈（可能持久化当前页）的是切页，hide/add + addToBackStack 的是压栈子页；启动器构造时写入的默认 extras（如是否清栈）与读取端默认值一并核对。
2. 压栈子页转换为以 @Param 接参数的可嵌入组件，由壳内容区按标签承载；壳状态维护子回退栈（入栈记录上一页标签与参数），清栈入口清空它；返回键与上箭头先弹子栈，再走默认页、抽屉、退出分支；子页带底栏标签时覆盖底栏选中。
3. 登记提示或规格与源壳的 FragmentTransaction 调用冲突时，以源码为准实现，并回写规格与登记。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-05f3fb8501654bad9261](../../../../store/cases/case-05f3fb8501654bad9261/a373b466540a298073450a55e68d4a64a6a180fd8fbe15307d211031c7ebe33b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`a373b466540a298073450a55e68d4a64a6a180fd8fbe15307d211031c7ebe33b`
