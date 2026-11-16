# Swiper 的当前页和选中同步

agent 会看到什么：读到 ViewPager2 的 setCurrentItem / currentItem、onPageSelected 和 tab 点击切页；产物里 Swiper 的 .index(...)、SwiperController.changeIndex、.onChange 回写，以及父子组件之间 selectedIndex 的同步

## 规矩

- rule-073136e45b5e｜源端延后 setCurrentItem 定初始页时，Swiper 用 .index 绑状态，不调 changeIndex｜读到：源端装好数据后用 `view.post { … setCurrentItem(index, false) }`（或 `doOnLayout`）延后定位 `ViewPager2` 的初始页；写错：目标在 `onReady` 或 `aboutToAppear` 里给列表赋值后立即调用 `swiperController.changeIndex(index, false)`，而 `Swiper` 在列表非空的 if/else 分支里才创建；声明的初始页状态没有绑到 `.index(...)`
- rule-31931e3936ee｜源端按持久化选中项恢复页并在切页时回写的，Swiper 要按它设 index、在 onChange 里回写｜读到：ViewPager2 容器在列表加载完成的观察者里按持久化的选中项算出下标再 setCurrentItem，OnPageChangeCallback.onPageSelected 里把当前项写回持久化；写错：Swiper 的 .index(...) 绑定的下标停在初值 0，加载后没按持久化选中项重算；.onChange(...) 里只按新页拉数据，没有调用写回当前选中项的接口
- rule-ba03b680f99e｜Tab 点击后 setCurrentItem 切页，目标用 changeIndex 切、onChange 回写｜读到：底部 Tab 的 onClick 只改选中态，observe 回调里调 ViewPager2 的 setCurrentItem(it, false) 切页；写错：Swiper 只写了 .index(选中态变量)，没有绑定 SwiperController，点击处理不驱动 Swiper，也没有 .onChange 回写选中态
- rule-10e679437cfa｜自绘 tab 加受控 Swiper 时双向都接：onChange 更新高亮，tab 项 onClick 写回 index｜读到：源端用普通 TextView 当 tab，Fragment 代码里有 tv….setOnClickListener { viewPager2.currentItem = N }，onPageSelected 只切选中样式；写错：目标 Swiper 只接了 .index(状态) 和 .onChange 更新高亮，@Builder 的 tab 项只有 Text 和选中样式、没有 .onClick
- rule-7e0f6253df80｜规格写列表随轮播当前项过滤时，Swiper 接 onChange 更新选中项，列表按它过滤｜读到：页面规格写列表内容随轮播当前项变化（如「待办为当前选中项的未完成项」），UiState 含选中项的 id 字段；写错：Swiper 上没有 .onChange(...)，ViewModel 没有选中项字段和切换方法，列表直接显示全部数据
- rule-415c69b79a5e｜源端首播靠 onPageSelected 时，目标对初始项显式延迟播放并与 onChange 去重｜读到：源端 `setCurrentItem(index, false)` 后由 `onPageSelected` 里 `postDelayed(…)` 启动当前页播放；写错：目标只在 `Swiper` 的 `onChange` 里启动播放，初始项靠命令式定位去间接触发 `onChange`，或初始项另起一个不和 `onChange` 去重的播放
- rule-459c2e57addb｜父子双向同步选中索引时，子组件回调父级前先比较目标与当前选中，同一项不重复回调｜读到：源端 selectItem 遇到同一项直接 return、不回调父级；写错：子组件的 @Event 选中回调不比较目标索引与当前 selectedIndex，父级改了 selectedIndex 再传回时又触发回调，形成回环
- rule-66314833cb31｜源端「装载后默认选中首项」迁成一次性初始化，@Param 数组更新只按 selectedIndex 同步｜读到：源码只在 initData 一次性取完分类数据后 selectItem(0) 并回调父 ViewPager，翻页时父级只调 setSelect(position) 同步选中；写错：子组件监听 @Param 数组的 @Monitor 回调里先把初始化标志置 false，再走「初始选中」，固定选中第 0 项并 @Event 回调父级
