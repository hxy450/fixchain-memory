# 为过编译删掉承载核心行为的调用时，同步改掉声称它仍在的注释并回报退化

审的是：代码
触发（任一种）：
- 读到：编译报错指向承载核心行为的调用，如卡片页的 .onAreaChange( 报 `can't support form application`；写错的样子：调用删了，文件头或注释仍写着由 onAreaChange 之类驱动；被它赋值的 @State 变量只剩声明、再没有赋值
适用范围：编译门或修编译错误时删除、替换承载功能行为（如尺寸测量）的调用
做法：
- 删调用的同一次修改里改掉相关注释，写明现在实际靠什么驱动，或写明该行为暂缺
- 回报里把行为退化列为待修项并附可替代的平台接口；卡片尺寸的替代是 FormExtensionAbility.onSizeChanged 与 formProvider.getFormRect
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 6；做法第 2 步 ← 建议 6、建议 1
