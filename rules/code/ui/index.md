# 界面

源端是布局 XML 里的 View 控件或 Compose 界面元素（文字、图片和自绘、布局容器、列表和翻页、弹窗和提示、点击和输入控件、动效、主题和颜色、窗口和系统栏、三方库的自定义 View），目标端是 ArkUI 组件和它的尺寸、样式、属性时

## 子主题

- [动效](animation/index.md)（21 条）：源端有 Animator 和它的 setDuration、动效起点的锚点位置、Compose 的 animateItem / animateContentSize / AnimatedContent、AnimatedVectorDrawable、LottieAnimationView，目标端有 animateTo、.animation、.transition 或 lottie 时
- [弹窗与浮层](dialog/index.md)（136 条）：源端有 AlertDialog、DialogFragment、BottomSheetDialog、PopupWindow、XPopup、Toast、Snackbar、上下文菜单，目标端有 openCustomDialog、CustomDialogController、bindSheet、bindPopup、Stack 里的遮罩浮层、showToast 时
- [图片和图形](graphics/index.md)（135 条）：源端有 ImageView、@drawable 位图和 shape、自定义 View 的 onDraw / Canvas / Paint、elevation 阴影、模糊，目标端有 Image、Canvas、backgroundColor、linearGradient、border、shadow、blur 时
- [点击、输入与控件](input/index.md)（141 条）：源端有 setOnClickListener、Compose clickable、EditText / TextField、CheckBox、Switch、SeekBar、ProgressBar、OnTouchListener、onKeyDown，目标端有 .onClick、TextInput、Checkbox、Toggle、Slider、Progress、.onTouch、手势、.onKeyEvent 时
- [布局与尺寸](layout/index.md)（174 条）：源端有布局 XML（LinearLayout、RelativeLayout、ConstraintLayout、FrameLayout、TableLayout，include / inflate 进来的布局、layout-land 等变体）、android:visibility，或 Compose 的 Row、Column、Box、自定义 Layout 和项目自己的 @Composable 组件，目标端有 Row、Column、Stack、共享 @Component 和 .width、.height、.margin、.padding、显隐条件时
- [列表、滚动与翻页](list/index.md)（132 条）：源端有 RecyclerView、ListView、ExpandableListView、Compose LazyColumn / LazyRow、ScrollView、ViewPager / TabLayout、PreferenceFragment，目标端有 List、ListItem、Grid、ForEach、LazyForEach、Repeat、Scroll、Swiper、Tabs、Refresh 时
- [文本与文案](text/index.md)（106 条）：源端有 TextView、Compose Text / TextStyle、strings.xml、getString / stringResource、String.format、DecimalFormat、Html.fromHtml、Spannable、contentDescription，目标端有 Text、Span、$r('app.string.…')、fontSize、lineHeight、maxLines、accessibilityText 时
- [主题、颜色与样式](theme/index.md)（68 条）：源端有主题和 style、?attr 颜色、@color 资源、Material 控件的默认外观、Compose MaterialTheme / colorScheme / contentColor、深浅色切换，目标端有 $r('app.color.…') 等资源引用、fontColor、backgroundColor、setColorMode 时
- [三方界面库](third-party-ui/index.md)（2 条）：源端界面由三方库渲染：Activity 继承库的基类（如 AppIntro2）、布局里是库的自定义 View 节点（如 ColorPicker）、用库的 PagerAdapter / ViewPager 子类填页，目标端要照库里的尺寸、动画和手势写 ArkUI 时
- [窗口与系统栏](window/index.md)（72 条）：源端有 Activity 的窗口标志、主题的全屏和系统栏颜色、fitsSystemWindows、WindowInsets、DisplayMetrics、屏幕方向、常亮、画中画和亮度，目标端有 window 的 setWindowLayoutFullScreen、setWindowSystemBarProperties、getWindowAvoidArea、expandSafeArea 时
