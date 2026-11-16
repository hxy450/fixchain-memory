# 共享基类里的 ActionMode 多选

agent 会看到什么：读过的页面、Adapter 或 Fragment extends 一个共享基类，基类里有 startActionMode、onCreateActionMode、OnBackPressedCallback，或覆盖 lint 把基类报为未锚定；交回的规格没写基类建的上下文操作栏和多选的进出口

## 规矩

- rule-2c5fae43a8ac｜页面类继承共享基类时，打开基类把它代码创建的操作栏写成 UI AC｜读到：页面的 Adapter 或 Fragment extends 一个共享基类，页面里只调用基类的进入多选、是否处于 ActionMode 等方法并消费基类提供的标志；基类里有 startActionMode、onCreateActionMode、ActionMode#setTitle、菜单 inflate；写错：规格只写了布局 XML 和页面代码里看得到的底部批量动作栏，没有上下文操作栏的标题格式、关闭键和溢出菜单项；引用基类标志时没写由谁置位
- rule-6b1db43bf645｜规格写列表多选状态表时追读 Adapter 基类，返回键和 ActionMode 结束也列为出口｜读到：列表 Adapter 继承一个选择模式基类，长按菜单项进入多选（startActionMode / ActionMode），进入与退出多选的实现在基类里，基类登记了 OnBackPressedCallback；写错：规格的多选状态表只写「菜单动作完成或 onDestroyView → 普通」，没有返回键（handleOnBackPressed）和 ActionMode 结束这两个出口；补锚点时只补计数类验收条目，状态表没改
- rule-00f9a8b3d49a｜覆盖 lint 报基类未锚定时读完整实现再写 AC，不并进无关组只写计数语义｜读到：覆盖 lint 把共享基类文件报为未锚定；grep 它的声明已能看到 onDestroyActionMode(ActionMode) 等 ActionMode 信号；写错：基类被并进无关的工具类组 AC，只写一句计数语义、判:unit，没有它的可见行为（操作栏、菜单、标题）
