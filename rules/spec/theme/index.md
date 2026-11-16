# 主题、颜色与默认外观

读到 styles.xml / themes.xml 的主题继承（AppCompat、MaterialComponents、Material3、android:Theme.*）、?attr/ 主题属性、Color.* 常量，或源控件没写颜色和外观属性，规格里写主题色、控件默认外观和颜色映射时

## 触发族

- [TextView 和 Button 没写的外观属性](widget-default-appearance/index.md)（5 条）：读过的源布局里 TextView、Button 只写了文本、字号、背景，没写 textColor、textAppearance、textAllCaps、includeFontPadding 等；交回的规格里这个控件缺了主题或默认样式给的颜色、大小写、字重和行框高度
- [AppCompat / MaterialComponents 主题的语义色](library-theme-colors/index.md)（5 条）：读到 styles.xml / themes.xml 里应用主题继承 Theme.AppCompat.DayNight 或 Theme.MaterialComponents.*，控件没写颜色、颜色来自 colorPrimary 等主题属性，values-night 里可能有同名主题；规格写「零硬编码色值」「沿用 base」「DayNight → resources/dark」，没有主题色的浅深两态值
- [平台主题 android:Theme.* 提供的控件外观](platform-theme-appearance/index.md)（6 条）：读到源控件没写 android:background、textColor 等外观属性，应用主题 parent 链止于 android:Theme.Holo / Material / DeviceDefault；规格的转换决策行和决策台账写「Holo 下划线样式」「暗底白字」「待核」「查证回执」
- [Material3 组件的库默认外观](material3-defaults/index.md)（6 条）：读到源主题 parent 链到 Theme.Material3.*，界面用 MaterialToolbar、BottomNavigationView、MaterialAlertDialogBuilder、BottomSheetDialogFragment 或 Compose Material3 TopAppBar，没自己写尺寸、底色和留白；规格的设计系统节写「Material3 为基」「Material3 默认」，映射行只写 showAlertDialog / bindSheet
- [没写样式、外观由平台主题提供的控件](platform-theme-widget-look/index.md)（6 条）：源布局的 <SeekBar>、<ListView> 等没写 style、divider、thumb，或 ActionBar 不在布局里，Activity 主题的 parent 链止于 android:Theme.Holo 等平台主题，规格只写「直接映射」「List + ForEach」「标题栏 + 返回箭头」
- [继承按钮、只换背景的自定义控件](button-subclass-background/index.md)（4 条）：源码里自定义控件继承 Button / AppCompatButton / MaterialButton，只 setBackgroundResource 换背景（有的再 setEnabled 或 setAutoSizeTextTypeUniformWithConfiguration），规格写成「可点击 + 背景着色」、只抄字号区间，或把 setEnabled 直译成 .enabled(false)
- [由主题决定的颜色（?attr/ 引用、android:theme 覆盖、状态栏图标明暗）](theme-resolved-colors/index.md)（5 条）：读到源布局、主题里由主题决定的颜色：?attr/colorPrimary 这类主题属性、AppBarLayout / Toolbar 的 android:theme 覆盖、主题继承来的状态栏图标明暗；规格只写属性名、单个色值或只写底色，看不出引用类型，也没有昼夜两态的解析值
- [代码里的框架颜色常量（Color.GREEN、Color.RED）](framework-color-constants/index.md)（1 条）：读到源码 setTextColor(Color.GREEN) 等 android.graphics.Color 常量；规格的颜色映射按颜色名对到色值不同的应用色令牌（如「Color.GREEN → light_green」）
- [values-vNN 下另有同名定义的应用主题](values-api-theme-override/index.md)（4 条）：读到 manifest 的 android:theme 指向的应用主题在 res/values/ 和 values-v21 等 values-vNN 下各有一份同名 <style>（values/ 继承 Theme.Light、values-v21 继承 Theme.Material.*）；规格的主题行、ActionBar 行、按压反馈按 values/ 的父主题写
- [根部 MaterialTheme 注入的全局主题](root-material-theme-contract/index.md)（1 条）：读到 Compose 源端在根部用 MaterialTheme 注入色板、明暗模式和字号缩放，各页面都在读；规格的跨 feature 工件契约和对接点里没有主题项，只在数据流里写「共享至全部页面」
- [Ionic 应用的主题变量和全局 mode](ionic-theme-mode/index.md)（2 条）：读到 Ionic 源端的主题 CSS 里有 body.dark 覆盖块给 --ion-background-color 等页面级变量深色值，或 App.tsx 里 setupIonicReact({ mode: 'ios' }) 固定模式、页面用 IonCard、IonToolbar 而 tsx 只有少量 inline style；规格的设计令牌只列 accent 的浅深两值，或只按 DOM 顺序和 inline 字号写组件
- [外观全来自第三方 UI 库默认样式的组件](third-party-lib-default-style/index.md)（1 条）：读到源组件只引入第三方库的默认样式（如 swiper/css/navigation、swiper/css/pagination），没有主题变量或样式覆盖；实现映射只写「ArkTS Swiper + indicator + 自定义左右导航按钮」这类行为描述，没有库名、版本、默认颜色尺寸形状或样式出处
