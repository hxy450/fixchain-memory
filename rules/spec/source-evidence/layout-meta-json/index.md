# 页面的源码布局和合成的 meta.json

agent 会看到什么：读到页面类用 ViewBinding / DataBinding（.databinding 包里的绑定类、android:onClick="@{…}"），多模块里有同名布局 XML；合成的 meta.json 里 layout_sources 指向别的模块，clickable_elements 是 []、navigation_targets 为 {}

## 规矩

- rule-7eb8f458e264｜多模块有同名布局时，按页面类所在模块和它用的绑定类定源码布局，不按布局名解析｜读到：多模块安卓工程里几个模块各有同名的 Fragment/Activity 类和同名布局 XML；页面类 import 的 ViewBinding 绑定类在本模块包名下的 .databinding 包里；写错：meta.json 的 layout_sources 或规格的「源码布局」指向另一个模块的同名布局；只手工改了已发现的几页，其余同名布局没复核
- rule-730970f5713d｜合成 meta.json 时 DataBinding 点击要计入 clickable_elements，不写空数组｜读到：源布局用 DataBinding 点击 android:onClick="@{page::方法}"，跳转写在 Fragment 代码里；写错：合成的 meta.json 里 clickable_elements 是 []、节点 clickable=false、navigation_targets 为 {}，也没标「未知」
- rule-ba83b5d41405｜RecyclerView 页面的规格要把全部 item 布局登记进必读的布局清单｜读到：源页面主体是 RecyclerView，Adapter 用 addItemType / onCreateViewHolder 引用多个 item 布局；写错：meta.json 的 recycler_item_layouts 为空，layout_sources 里没有 item 布局，页面规格只列 Adapter 源码锚点
