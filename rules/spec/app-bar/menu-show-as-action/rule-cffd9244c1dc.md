# 页面规格登记菜单时写明每项 showAsAction、缺省值、子菜单和宽度规则，不用 bindMenu 一句话代替

审的是：规格
触发（任一种）：
- 读到：源菜单 XML 各项带 app:showAsAction、orderInCategory，有 <menu/> 子菜单，ActionMode 复用同一菜单；写错的样子：页面规格只登记菜单 id 清单和显隐规则，用「标题栏 actions + bindMenu / Menu 组件」「自管多选状态 + 条件渲染操作栏」一句话代替，没有 showAsAction、缺省值、子菜单结构和宽度规则
适用范围：规格提取阶段为带菜单或 CAB 的页面登记菜单时
做法：
- 规格的菜单表每项写：id、showAsAction（未声明的写明选项菜单缺省 never、CAB 缺省 ifRoom）、orderInCategory、子菜单结构；另写一句动作键上限按 ActionBarPolicy 随屏宽取 2–5 个
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getMaxActionButtons 按 screenWidthDp / screenHeightDp / smallestScreenWidthDp 取 5、4、3、2（w ≥ 360 → 3，w ≥ 500 → 4，sw > 600 → 5）：规格里要写的宽度规则（出处：com.android.internal.view.ActionBarPolicy#getMaxActionButtons（框架版））
- MenuBuilder 缺省 SHOW_AS_ACTION_NEVER；StandaloneActionMode 缺省 SHOW_AS_ACTION_IF_ROOM：规格里要写的两种缺省值（出处：com.android.internal.view.menu.MenuBuilder；com.android.internal.view.StandaloneActionMode）
来源：1 张卡，1 个应用
- case-ccade488607d58d27d0e（omni-notes-hmos）：做法第 1 步 ← 建议 5
