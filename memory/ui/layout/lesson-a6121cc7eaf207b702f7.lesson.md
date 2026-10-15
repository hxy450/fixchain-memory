# 自绘工具栏导航图标按实际生效者判定：DrawerToggle 接管同一 Toolbar 时画汉堡，有 parentActivityName 时默认显示 Up

ID：`lesson-a6121cc7eaf207b702f7` · 版本：6

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，自绘 ActionBar 代体或标题栏、决定导航图标是返回箭头、汉堡还是不画时；复用模板或兄弟页标题栏时

## 适用情境

判断导航图标的输入：Activity 主题是否带窗口 ActionBar；Manifest 是否为 Activity 声明 parentActivityName 或 PARENT_ACTIVITY meta-data；代码是否调用 setDisplayHomeAsUpEnabled(true/false)，onOptionsItemSelected 是否处理 android.R.id.home；基类 onPostCreate 是否以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState（布局根常为 DrawerLayout + NavigationView）。目标套用自带返回箭头的标题栏模板、兄弟页标题栏，或保留自定义 Up 标题栏。

## 例外与边界

- 主题为 NoActionBar 且自建 Toolbar 时，按 setSupportActionBar 之后对该 Toolbar 的调用（setNavigationIcon、setDisplayHomeAsUpEnabled、DrawerToggle）判断

## 原因

“只在源端启用 Up 时绘制”只是必要条件：AppCompat 窗口 ActionBar 在 Manifest 有 parentActivityName 时默认启用 Up，不调 setDisplayHomeAsUpEnabled 也显示箭头；基类的 ActionBarDrawerToggle.syncState 又会把同一 Toolbar 的 Up 换成汉堡，setDrawerIndicatorEnabled(false) 会改回 homeAsUpIndicator（appcompat 1.7.0 ActionBarDrawerToggle），之后的 setNavigationIcon 还会再覆盖。只看子类一处调用就会画错图标或绕开抽屉基座。

## 做法

1. 按顺序判定①：Activity 或其基类（常见 BaseActivity.onPostCreate）以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState() 时，导航图标是汉堡、点击开关抽屉，目标装配抽屉基座的汉堡栏；再查 setDrawerIndicatorEnabled(false) 与之后的 setNavigationIcon/监听覆盖，关闭指示器时显示 Up。
2. ②否则看主题是否带窗口 ActionBar；③窗口 ActionBar 页在 Manifest 声明 parentActivityName 或 PARENT_ACTIVITY meta-data 时 AppCompat 默认显示 Up，点 Up 走 onOptionsItemSelected 的 android.R.id.home 分支或回父页；④代码显式 setDisplayHomeAsUpEnabled(true/false) 时以它为准；都没有才不画，返回交给系统返回键与手势。
3. 规格写定 Up/汉堡是否显示及依据（主题、parentActivityName、setDisplayHomeAsUpEnabled、DrawerToggle），不写“若有”；规格或派工与源码生效形态冲突时按源码实现并登记差异。复用模板或兄弟页标题栏前先按当前源核对。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-255a399de4580990a70e](../../../store/cases/case-255a399de4580990a70e/f6ed46916e4fffbe8498bb8d8758eba997c05df5680aa0652de88a8b74f512c9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f6ed46916e4fffbe8498bb8d8758eba997c05df5680aa0652de88a8b74f512c9`
- [case-855df43db43e4ed66f9e](../../../store/cases/case-855df43db43e4ed66f9e/90ab1730914da1d421431502024f5fc3fbce0c541761fd4b3ae9ed8a57255a58.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`90ab1730914da1d421431502024f5fc3fbce0c541761fd4b3ae9ed8a57255a58`
- [case-ee2085c48fe78dbd3a2f](../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：recommendation:4, recommendation:6
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
