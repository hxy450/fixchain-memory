# 单 Activity 壳内的 loadChildFragment 子页映射为壳内回退栈，不改成独立路由或清栈切页

ID：`lesson-7bcb44f0e376ec67e5a8` · 版本：1

[本主题](index.md)

## 何时使用

壳层导航实现与页面形态决策阶段，为源端在内容区压栈加载的子 Fragment 确定承载方式、返回与底部导航选中语义时

## 适用情境

源主 Activity 用 loadChildFragment（hide 加 add 加 addToBackStack）打开详情、搜索等子页，子页期间底栏与迷你播放条仍在，工具栏随栈深显示上箭头，带 navigationTag 时同步底栏选中；启动器构造时写入默认 extras。目标同时有 Navigation 路由与壳内容槽。

## 原因

把子页做成 NavDestination 路由会离开壳（失去底栏与迷你条），改成清栈切页会丢失返回路径与上箭头；登记中的错误提示可能与规格冲突。

## 做法

1. 壳状态维护子回退栈（入栈记录上一页 tag 与参数），清栈入口清空它；返回键与上箭头先弹子栈，再走默认页、抽屉、退出分支；navigationTag 非空时覆盖底栏选中。
2. 页面元数据为子组件且源经 loadChildFragment 打开的页，转换为以 @Param 接参数的可嵌入组件，由壳内容区按 tag 承载，不以已存在页面的先例覆盖。
3. 调用点按源 API 区分 loadFragment（清栈并持久化）与 loadChildFragment（压栈）；映射启动器时核对构造器写入的默认 extras；登记提示与规格冲突时以规格为准。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-05f3fb8501654bad9261](../../../../store/cases/case-05f3fb8501654bad9261/a373b466540a298073450a55e68d4a64a6a180fd8fbe15307d211031c7ebe33b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`a373b466540a298073450a55e68d4a64a6a180fd8fbe15307d211031c7ebe33b`
