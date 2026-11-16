# 选项色值和素材按源数据源迁入资源，不在 color.json 里追加按截图估的色

审的是：资源
触发（任一种）：
- 读到：源 ViewModel 数据源里列出颜色值（含渐变两端）和 R.drawable 位图素材；写错的样子：目标 resources/base/element/color.json 里追加了源数据源里没有、按截图估的色值；边框等位图素材没有迁进 resources/base/media
适用范围：为选项列表准备目标端颜色和图片资源时
做法：
- color.json 里的选项色照源数据源的值写（渐变方案写两端色）；位图素材从源 res/drawable* 原样迁到 resources/base/media，文件和源资源名一一对应
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- media 目录放图片、音频、视频等非文本格式的文件，目录下只支持文件：位图素材的落点（出处：resource-categories-and-access.md，资源组目录）
- 修复迁入了源端全部原始位图素材，替换按截图估的色块：修好后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 选项素材对应的源位图：源 ViewModel 里引用的 R.drawable 名字，到源工程 res/drawable*、res/mipmap* 下按同名文件找；按密度目录取同名文件拷到 resources/base/media（或对应密度的限定词目录），保持文件名
来源：1 张卡，1 个应用
- case-cdf2347c2ca354b68924（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；取值 2 ← 诊断
