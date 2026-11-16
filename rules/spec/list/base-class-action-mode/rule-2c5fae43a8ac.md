# 页面类继承共享基类时，打开基类把它代码创建的操作栏写成 UI AC

审的是：规格
触发（任一种）：
- 读到：页面的 Adapter 或 Fragment extends 一个共享基类，页面里只调用基类的进入多选、是否处于 ActionMode 等方法并消费基类提供的标志；基类里有 startActionMode、onCreateActionMode、ActionMode#setTitle、菜单 inflate；写错的样子：规格只写了布局 XML 和页面代码里看得到的底部批量动作栏，没有上下文操作栏的标题格式、关闭键和溢出菜单项；引用基类标志时没写由谁置位
适用范围：规格提取阶段，页面行为有一部分由共享基类用代码创建（ActionMode、菜单、标题）时
做法：
- 打开基类读它用代码创建的 UI：startActionMode 的 Callback 在 onCreateActionMode 里 inflate 的菜单、ActionMode#setTitle 的标题格式、关闭键；把标题格式、关闭键和每个溢出菜单项写成 UI AC
- 规格引用基类的标志（如“是否连懒加载项一起选中”）时，同时写明由哪个入口置位（例如哪个菜单项）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- public ActionMode startActionMode(ActionMode.Callback callback)：以 TYPE_PRIMARY 类型启动上下文操作栏，界面由 Callback 决定（出处：android.app.Activity#startActionMode）
- public boolean onCreateActionMode(ActionMode mode, Menu menu)：这里填进 menu 的项就是操作栏上的动作按钮和溢出菜单（出处：android.view.ActionMode.Callback#onCreateActionMode）
- public abstract void setTitle(CharSequence title)：操作栏标题（如已选数量）在这里设置（出处：android.view.ActionMode#setTitle）
针对本应用要查的：
- 基类创建的操作栏的标题格式和菜单项：源工程里该基类的 Java/Kotlin 文件中 ActionMode.Callback 的实现，以及它 inflate 的 res/menu 下的菜单 XML；逐项列出 setTitle 用的字符串资源和格式参数、菜单 XML 里每个 item 的 title 与点击后的行为
来源：1 张卡，1 个应用
- case-997587966a65e79790b5（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
