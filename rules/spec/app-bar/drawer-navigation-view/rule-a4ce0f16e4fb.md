# 规格写 NavigationView 转自定义抽屉的映射行时，补上菜单项选中、未选的可见契约

审的是：规格
触发（任一种）：
- 读到：源 DrawerLayout + NavigationView 没写 item 样式，menu 分组带 checkableBehavior；写错的样子：规格的抽屉映射行或 AC 只写 checked 布尔同步（点击项选中、其余清除），没写菜单项选中、未选的底色、字重、文字与图标着色，组间分隔几何和列表上下留白
适用范围：规格提取阶段写 DrawerLayout + NavigationView 迁成自定义抽屉的映射行时
做法：
- 映射行补可见契约：选中、未选的底色、字重、文字色和图标着色，组间分隔线的粗细、是否通栏和上下间距，列表上下留白，并注明取自 Material NavigationView 默认样式
来源：1 张卡，1 个应用
- case-cee85a6c89d26db1ef48（Privacy Friendly 2048）：做法第 1 步 ← 建议 3
