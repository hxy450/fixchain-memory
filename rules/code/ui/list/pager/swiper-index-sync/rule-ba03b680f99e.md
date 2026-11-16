# Tab 点击后 setCurrentItem 切页，目标用 changeIndex 切、onChange 回写

审的是：代码
触发（任一种）：
- 读到：底部 Tab 的 onClick 只改选中态，observe 回调里调 ViewPager2 的 setCurrentItem(it, false) 切页；写错的样子：Swiper 只写了 .index(选中态变量)，没有绑定 SwiperController，点击处理不驱动 Swiper，也没有 .onChange 回写选中态
适用范围：安卓用 ViewPager / ViewPager2 加底部 Tab 命令式切页，迁成 ArkUI Swiper 加自定义底栏时
做法：
- 声明 controller: SwiperController = new SwiperController()，写 Swiper(this.controller)；Tab 点击处理里调 this.controller.changeIndex(index)
- Swiper 上写 .onChange((index: number) => { 选中态 = index })，页面变化时回写底栏选中态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (controller?: SwiperController): SwiperAttribute：Swiper 的构造，传入控制器才能用代码切页（出处：鸿蒙 SDK 的 ets/component/swiper.d.ts，SwiperInterface）
- changeIndex(index: number, useAnimation?: boolean)：SwiperController 切到指定页，useAnimation 默认 false 即无动画（@since 12）（出处：鸿蒙 SDK 的 ets/component/swiper.d.ts，SwiperController.changeIndex）
- changeIndex(index: number, animationMode?: SwiperAnimationMode | boolean)：同一方法 @since 15 的重载，true 等同 DEFAULT_ANIMATION，false 等同 NO_ANIMATION（出处：鸿蒙 SDK 的 ets/component/swiper.d.ts，SwiperController.changeIndex）
- onChange(event: Callback<number>): SwiperAttribute：当前显示的子页索引变化时回调，参数是新索引（出处：鸿蒙 SDK 的 ets/component/swiper.d.ts，SwiperAttribute.onChange）
- changeIndex(value: number): void：同族接口：TabsController 切到指定页签，越界时用 0（出处：鸿蒙 SDK 的 ets/component/tabs.d.ts，TabsController.changeIndex）
- changeIndex(index: number, useAnimation?: boolean): void：同族接口：IndicatorComponentController 切换指示器索引（出处：鸿蒙 SDK 的 ets/component/indicatorcomponent.d.ts，IndicatorComponentController.changeIndex）
未核实：这一支修复只经过构建验证，观察截止前没有真机回归；只用 .index(状态变量) 是否一定不切页，卡里没证实；卡里的环境是 API 24（6.1.1），本机用 API 23 的声明核实
来源：1 张卡，1 个应用
- case-646efd504782bd3dec69（android-panorama-map-vest7）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
