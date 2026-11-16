# 挂在宿主 Activity 里的 Fragment 子组件

agent 会看到什么：源码经 FragmentTransaction 的 add / replace / addToBackStack 把 Fragment 放进宿主 Activity 的容器，页面元数据标 page_type=sub_component，规格把它推成 NavDestination 全屏页、写不出承载它的容器，或宿主没登记各 Tab 的沉浸和避让

## 规矩

- rule-dae6b36ed507｜功能索引写组件挂在哪些页时，每条都要有源码里的容器 id 和 replace/add 调用｜读到：流水线模板或示例行里有「涉及页面：…, 主页(MiniBar)」「主页(MiniBar)常驻」这类通用说法；安卓源码里 Fragment 型组件只经 FragmentTransaction.replace / add 放进个别 Activity 布局的容器里，主 Activity 布局只有 ViewPager 与 Tab 栏；写错：功能索引或规格的「涉及页面」、组件挂载关系里写了某组件挂在某页（如「主页(MiniBar)」「依赖 F001(MiniBar)」），但写不出这页源布局里承载它的容器 id，也找不到把它 replace/add 进去的调用
- rule-57266036280c｜meta 标 sub_component 且源端壳内压栈打开的页面，规格不推荐 NavDestination 全屏页｜读到：meta.page_type=sub_component；源码用 hide + add + addToBackStack 在宿主 Activity 内容区打开这个 Fragment；写错：页面规格备注推荐「实现为 NavDestination 全屏页」，转换表写 NavDestination 标题栏；或 handback 宣称这些子页将实现为 NavDestination
- rule-6f16a5cb40fc｜子组件规格被标为不需沉浸时，宿主规格逐个 Tab 登记是否用全屏背景｜读到：子页面元数据 page_type=sub_component，自动标 needs_immersive_safearea=false；宿主元数据 page_type=full_screen_page、needs_immersive_safearea=true；写错：宿主规格里没有逐个 Tab 登记内容是否用全屏背景、是否延伸到状态栏，也没写由宿主还是子组件负责避让
- rule-399e1dd83ab4｜规格把 Activity/Fragment 生命周期和事务语义写成独立验收条目，不只写一行等价｜读到：源码有 replace + addToBackStack、popBackStackImmediate 后换新实例、popBackStack、finish()，以及 onActivityCreated → init、onDestroyView、onStop 等回调；写错：规格只写「navPathStack ← 各个切换 Fragment 的方法 等价」「onResume → onPageShow」「onPause → onPageHide」一行，没有视图销毁重建、finish 与 popBackStack 的区别、同名页能否复用
