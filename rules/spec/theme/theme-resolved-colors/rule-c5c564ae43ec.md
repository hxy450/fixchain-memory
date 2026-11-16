# 页面规格写颜色时保留 ?attr/ 和 @color/ 的区别，不简写成属性名或只列色值

审的是：规格
触发（任一种）：
- 读到：源布局写 android:background="?attr/colorPrimary"，别处又有 @color/colorPrimary 写死的引用；写错的样子：页面规格或设计令牌写「背景 colorPrimary」或只列十六进制值，看不出是主题属性还是写死色
适用范围：页面规格、设计令牌里描述控件颜色来源时
做法：
- 写成「背景 ?attr/colorPrimary（主题属性，日夜两态，绑成对键）」或「背景 @color/colorPrimary（写死，单态常量）」，原样保留引用前缀
来源：1 张卡，1 个应用
- case-7af8ba0d85382021da91（Privacy Friendly 2048）：做法第 1 步 ← 建议 2
