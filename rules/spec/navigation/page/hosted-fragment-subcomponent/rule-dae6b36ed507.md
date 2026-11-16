# 功能索引写组件挂在哪些页时，每条都要有源码里的容器 id 和 replace/add 调用

审的是：规格
触发（任一种）：
- 读到：流水线模板或示例行里有「涉及页面：…, 主页(MiniBar)」「主页(MiniBar)常驻」这类通用说法；安卓源码里 Fragment 型组件只经 FragmentTransaction.replace / add 放进个别 Activity 布局的容器里，主 Activity 布局只有 ViewPager 与 Tab 栏；写错的样子：功能索引或规格的「涉及页面」、组件挂载关系里写了某组件挂在某页（如「主页(MiniBar)」「依赖 F001(MiniBar)」），但写不出这页源布局里承载它的容器 id，也找不到把它 replace/add 进去的调用
适用范围：功能索引和规格里填写「涉及页面」、共享组件挂载到哪些目标页面的条目
做法：
- 每条「组件→页面」都写出源端依据：宿主 Activity、布局里的容器 id、把组件放进去的 replace(containerViewId, fragment) 或 add(containerViewId, fragment) 调用在哪个类
- 源码里找不到容器和 replace/add 调用的页面不写进「涉及页面」，也不写依赖这条挂载的说法；模板示例行只当格式，不当源码事实
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- replace(@IdRes int containerViewId, Fragment fragment)：第一个参数是承载这个 Fragment 的容器 id；按这个 id 去布局 XML 里找到容器，就找到了宿主页面（出处：android.app.FragmentTransaction#replace）
- add(@IdRes int containerViewId, Fragment fragment)：同族接口：add 的第一个参数同样是容器 id；为 0 时不放进任何容器（出处：android.app.FragmentTransaction#add）
针对本应用要查的：
- Fragment 型共享组件的宿主页面：源工程的 Kotlin/Java 代码里搜传入这个 Fragment 的 replace(R.id.… / add(R.id.… 调用，再在布局 XML 里按那个 id 找容器所在的布局；容器所在的布局属于哪个 Activity（或父 Fragment），那个页面就是宿主；没有搜到调用的页面不算宿主
未核实：androidx.fragment.app.FragmentTransaction 的同名方法本机没有源码，参数含义按框架版 android.app.FragmentTransaction 写
来源：1 张卡，1 个应用
- case-3db1068ed462e12cf813（免费来电多多）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
