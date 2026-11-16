# 导航目的地声明了 <argument> 时，分页规格写明页面入参的名称、类型、可空和取参处

审的是：规格
触发（任一种）：
- 读到：导航图 XML 的目的地下有 <argument android:name=… app:argType=…>（可带 app:nullable、android:defaultValue），Fragment 用 requireArguments() / arguments 读取；写错的样子：分页规格没有「页面入参 / 取参方式」一项；导航图一节只留起始目的地、底部导航和深链占位（如 {参数名}），丢了各目的地的 argument 声明
适用范围：从 Navigation Component 的导航图迁页面时，分页规格的页面入参项和导航图总表
做法：
- 每个目的地在分页规格的「页面入参」里逐项写：参数名（android:name）、类型（app:argType）、是否可空（app:nullable）、默认值（android:defaultValue），没写可空也没写默认值的记为必填；再写源 Fragment 里读取它的位置（requireArguments().getString(键) / arguments）
- 导航图总表同样按目的地列出这些参数，不只保留 deep link 的占位符
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- NavArgument 的属性：android:name、android:defaultValue、nullable（format=boolean）、argType（format=string）：<argument> 上可写的四个属性，规格的页面入参照这四项抄（出处：androidx.navigation:navigation-common 包内 res/values/values.xml，NavArgument（按应用依赖的版本））
未核实：分页规格模板本身是否含「页面入参」必填项，卡里没能确认
来源：1 张卡，1 个应用
- case-b3ded04b6b14f7ce8c8b（星途清单）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
