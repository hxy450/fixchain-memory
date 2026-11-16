# 窗口 ActionBar 溢出菜单的面板

agent 会看到什么：读到源端窗口 ActionBar 的溢出菜单（菜单有进溢出的项，框架用 PopupWindow 弹出，样式取主题的 actionOverflowMenuStyle、colorPopupBackground）；产物里自绘溢出面板盖不盖住标题栏、底色、点外关闭层和面板挂在哪一层

## 规矩

- rule-299eaea9e9c1｜框架溢出面板按源主题的溢出菜单样式和弹层底色定位置与颜色，Material 系盖住标题栏｜读到：源主题是 Theme.Material 系（如 Theme.Material.Light.DarkActionBar）的窗口 ActionBar，菜单有进溢出的项；写错：溢出面板 margin top 等于栏高、贴在标题栏下，底色写成 #FFFFFFFF 纯白
- rule-e9f5340024f5｜共享组件里的锚定面板要配点外关闭层时，组件用 OverlayManager 把遮罩加面板整层挂到窗口级｜读到：源端溢出菜单是 ActionBar 的 PopupWindow（浮在窗口最上层，点外部只关闭菜单）；页内原写法是全幅透明捕获层后接面板，注释写「面板 z 序居上」；写错：共享标题栏把面板画在自身节点里（根 Stack 子节点或 .overlay()），组件契约写「外点捕获层由宿主兑现」，宿主在标题栏之后的兄弟 Stack 里放全幅捕获层，面板项点不中
