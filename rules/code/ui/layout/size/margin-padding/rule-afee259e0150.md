# 配置驱动列表的各项不套统一间距，上下间距取源 Fragment 根布局

审的是：代码
触发（任一种）：
- 读到：源端各 Fragment 按顺序加进同一个无间距容器，每项的间距写在各自根布局的 android:padding* / android:layout_margin* 上，外壳容器有一次四边间距；写错的样子：目标给列表每一项统一套 .padding({ top: 10, bottom: 10 }) 一类对称间距，或没读源布局就自填间距值
适用范围：把按顺序拼起来的多个源 Fragment 迁成 ArkTS 列表的各项时
做法：
- 列表容器和插槽不加统一间距；每项的上下间距取自它对应的源 Fragment 根布局，没读到那份布局前不填数值
- 公共容器只保留源端外壳的那一次四边间距
针对本应用要查的：
- 每个编辑项的上下间距：源工程 res/layout 下该 Fragment 的布局 XML（Fragment 的 onCreateView / ViewBinding 引用的那个），看根节点的 android:padding*、android:layout_margin*；dp 数值照写成 vp，只写源端有的那几边；外壳容器的间距从承载列表的 Activity / Fragment 布局里取
来源：1 张卡，1 个应用
- case-6fc0687402faa0e4f9a5（组件岛Widget Island）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
