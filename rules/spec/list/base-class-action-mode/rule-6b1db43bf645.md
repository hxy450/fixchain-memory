# 规格写列表多选状态表时追读 Adapter 基类，返回键和 ActionMode 结束也列为出口

审的是：规格
触发（任一种）：
- 读到：列表 Adapter 继承一个选择模式基类，长按菜单项进入多选（startActionMode / ActionMode），进入与退出多选的实现在基类里，基类登记了 OnBackPressedCallback；写错的样子：规格的多选状态表只写「菜单动作完成或 onDestroyView → 普通」，没有返回键（handleOnBackPressed）和 ActionMode 结束这两个出口；补锚点时只补计数类验收条目，状态表没改
适用范围：规格提取阶段整理列表多选 / 选择模式状态机时
做法：
- 沿 Adapter 追读基类的进入、退出多选方法，状态表列全部退出触发：菜单动作完成、onDestroyView、返回键（OnBackPressedCallback.handleOnBackPressed）、ActionMode 结束，各标源码位置（类#方法）
- 后来把基类补为锚点时，同步核对已有状态表的出口是否齐全
针对本应用要查的：
- 多选模式的全部退出触发：源工程列表 Adapter 的父类里开始、结束多选的方法，搜 OnBackPressedCallback、addCallback、ActionMode；每个能把多选态结束的调用点记成状态表的一行出口
来源：1 张卡，1 个应用
- case-f32c19bb6ab1caffe063（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
