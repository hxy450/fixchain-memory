# 页面、控件、算法或实体基类由二进制三方库承载时，按依赖坐标取库制品核对真值，不按调用面推断或以原生组件近似

## 何时使用

规格提取与实现阶段，为 build.gradle 二进制依赖（AAR/jar）承载的界面、提示条与对话框、手势、算法输出或实体基类写映射决策、行为契约或自研等价实现，以及为它们登记占位时（目标端没有该库的同名移植或等价库时）

## 适用情境

仓库内只有调用面：Activity extends 库类，布局根节点或 UI 快照只剩库的自定义 View 类名，应用侧只留 Style/Configuration 常量或 Builder 调用，实体 extends 库基类，常量或正则来自库类；行为、几何、动画、队列、手势阈值、字段集或输出字符串都在库内。规格或映射参考写成「Toast / 原生组件 / 自研 / 系统 intl 替代」并标 Auto，或写「库源不可见→默认样式即可对齐」；本机 Gradle 缓存可能还没有该制品。前提是目标端没有该库的同名移植或等价库，库的行为要靠自研、原生组件或系统接口承接。

## 例外与边界

- 决策台账里有带编号、经用户批准的范围裁剪或降级，明确该库功能不复刻
- 按库真值改写近似实现时，应用侧调用显式给出的参数、按钮与文案、回调照应用侧保留，库缺省值只补应用没有显式给出的项；不因库的默认形态增减应用侧给出的入口

## 原因

目标端没有同名库时，写者只看得到应用侧的调用、常量与类名，便按名字、属性或常量反推：库内的队列与出队时机、动画时长与插值、dimens 与布局、截断与行距、手势阈值与惯性、字段集与 equals、序列化字面形态和文案阈值都会丢失。登记成“近似”“待视觉对齐”的占位没有真值可对齐，到交付也兑现不了。坐标与版本就写在构建脚本里，“仓库内无源码”是可补的材料缺口，不等于行为不可知。

## 做法

1. 从 build.gradle（含 gradle.properties、版本目录）读出库坐标与版本，按序取制品：本机 ~/.gradle/caches/modules-2/files-2.1；没有就用 Gradle 解析下载该依赖，或按坐标从 Maven 仓库、JitPack（https://jitpack.io/com/github/<owner>/<repo>/<version>/）、上游仓库对应版本 tag 获取，有 sources jar 时优先。
2. 解包后按库的职责取真值：UI 库读 res 的 layout、values（aar 里每个 values 限定目录只有一份合并后的文件，如 res/values/values.xml、res/values-large-v4/values-large-v4.xml，dimens、styles、strings、integers 都在里面）、anim/animator、drawable 及其限定目录（layout-land、values-sw600dp 等），并用 javap -p -c 或反编译读控件、管理器与 Builder 的测量、缺省参数、动画、队列与触摸分支；先列出库内全部视图类，再判断目标组件是否足够（图片查看器的缩放、平移、双击、惯性属于库行为，不是可省略的增强）。实体基类读字段集、类型、缺省值、equals/toString 与序列化规则；库里的常量与正则按库值迁移。 只有编译 jar、没有 sources jar 不等于不可核：用 javap -p -c -constants 读构造器缺省分支（Kotlin 缺省参数在参数表末尾带 DefaultConstructorMarker 的合成构造器里）与 companion 常量（const val 落在外层类上；非 const 的值只在 static {} 的字节码里，-constants 不印），本机未装 JDK 时用 Android Studio 自带的 jbr/bin/javap（DevEco Studio 自带的 jbr 没有 javap）；动效与物理类库读更新与发射方法，确认参数的时间域（每帧还是每秒）、帧率归一化、重力与质量、阻尼、寿命与淡出，再写常量与步进。上游提醒或注释写“库源不可核”时先自己核一次。
3. 算法库（重复规则、相对时间、日期格式、文本拆分与序列化）用 JDK 小程序加载同版本 jar 跑代表输入，把输出的字面形态（时区形态、行尾、文案模板、单位阈值与取整）写成契约；登记常量时同时登记它经库序列化后的字符串。系统 i18n/intl 只在与库输出对代表输入逐字一致时替代；库有自有阈值、模板或资源表时移植算法与资源。
4. 把真值写进规格映射行或组件头注释，注明库内文件、资源名或类方法与版本；映射行的依据只是仓库内调用行、README、单元测试或分析产物里的“建议”时，不标 Auto、不进跨栈硬映射基线，实现也不凭样式常量类自定时长、角度或间距。
5. 确实取不到时，在规格逐项列出缺失的库真值（队列时序、几何、手势、序列化格式、文案）及其影响，登记为阻塞或交用户改判；不写「默认样式即可对齐」，也不把这类占位的兑现交给视觉对齐步骤。派工给出 Android 源码路径时，一并给出库制品缓存路径与可解包提示。

来源支持：23 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源和源码；androidx.viewpager:viewpager 1.0.0；androidx.appcompat:appcompat 1.7.1；com.google.android.material:material 1.12.0；com.squareup.okhttp3:okhttp 4.10.0（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕aar 包内的代码是 classes.jar（只有编译后的类，包里不带源码），资源在 res/ 下；res 的每个 values 限定目录只有一份合并后的文件：不带限定符的目录是 res/values/values.xml，带限定符的目录是同名文件（如 res/values-large-v4/values-large-v4.xml），dimens、styles、strings、integers 都合在这一份里，没有单独的 dimens.xml、styles.xml
- 〔做法第 2 步〕javap -constants 只给带常量值属性的 static final 基本类型和 String 字段印出取值（如 androidx ViewPager 的 MAX_SETTLE_DURATION = 600）；在静态初始化里赋值的 static final 字段（如 ViewPager 的 sInterpolator）只印声明、不印值，取值要用 -c 看 static {} 的字节码
- 〔做法第 2 步〕Kotlin 伴生对象里的 const val 编译成外层类上带取值的 public static final 字段（javap -constants 在外层类上印出值），Companion 类本身没有这个字段；伴生对象里非 const 的 val 编译成外层类的 private static final 字段，取值只在外层类 static {} 的字节码里
- 〔做法第 2 步〕Kotlin 带缺省参数的构造器会另编出一个合成构造器，参数表末尾多一个 int 位掩码和一个 kotlin.jvm.internal.DefaultConstructorMarker；缺省值在这个合成构造器里按位掩码分支算出，然后调用主构造器；主构造器的字节码里看不到缺省值
- 〔做法第 2 步〕DevEco Studio 6.1.0.850 自带的 JetBrains Runtime（21.0.8）的 bin 目录里有 java、javac，没有 javap
- 〔适用情境 / 做法第 2 步〕androidx.viewpager 1.0.0 的 ViewPager：快划翻页要同时满足拖动距离大于 25dp、抬手速度大于 400dp/s（两者在初始化时乘屏幕密度换成像素和像素/秒）；平滑滚动和抬手归位的时长按距离和速度算，上限 600 毫秒，插值函数为 f(t) = (t−1)^5 + 1
- 〔适用情境 / 做法第 2 步〕androidx.viewpager 1.0.0 的 ViewPager 抬手定页：距离和速度都过快划阈值时按速度方向定（速度大于 0 取左侧可见页，否则取它右边一页）；没过阈值时取 左侧可见页 + (int)(页内偏移 + 截断量)，截断量在左侧可见页不小于当前页时为 0.4、否则为 0.6，即拖向相邻页时相邻页露出至少 60% 才翻过去，否则回到原页；结果再夹在已加载页的范围内
- 〔适用情境 / 做法第 2 步〕Swiper 不设 curve 时动画曲线是 interpolatingSpring(-1, 1, 328, 34) 弹簧曲线，此时切换动画时长只由曲线参数决定，duration（默认 400，单位 ms，小于 0 按默认）不起作用；要让 duration 生效须设成别的曲线
- 〔适用情境 / 做法第 2 步〕android-36.1 平台资源：主题链上没有另设 backgroundDimAmount 时，基础主题 Theme 的暗化比例为 0.6；Theme 的 windowCloseOnTouchOutside 为 false，Theme.Dialog 另设为 @bool/config_closeDialogWhenTouchOutside，其值为 true
- 〔适用情境 / 做法第 2 步〕宽度为 WRAP_CONTENT 的窗口（浮动对话框）测量时，屏宽大于 config_prefDialogWidth（android-36.1 平台资源中为 320dp）就先按这个宽度试排；内容放不下（测得 MEASURED_STATE_TOO_SMALL）再按（该宽度 + 屏宽）/ 2 试一次，仍放不下才按整个可用宽度排
- 〔适用情境 / 做法第 2 步〕对话框最小宽度：android-36.1 平台资源 dialog_min_width_minor = 95%、dialog_min_width_major = 65%；appcompat 1.7.1 的 *.Dialog.Alert、*.Dialog.MinWidth 主题把 android:windowMinWidthMinor / Major 设为 abc_dialog_min_width_minor / major，不带限定符的目录下 95% / 65%，values-large 下 80% / 55%，values-xlarge 下 72% / 45%；应用主题没有另设 windowMinWidthMinor / Major 时取这些值
- 〔适用情境 / 做法第 2 步〕appcompat 1.7.1 的 Base.V7.Theme.AppCompat.Light.Dialog（Theme.AppCompat.Light.Dialog 的底）设 windowIsFloating、backgroundDimEnabled、windowCloseOnTouchOutside 都为 true，窗口底是 abc_dialog_material_background：drawable-v21 下为四边各 inset 16dp 的白色矩形，圆角取 ?attr/dialogCornerRadius，即 abc_dialog_corner_radius_material = 2dp（watch 限定下是没有 inset 和圆角的白底）；应用主题没有另设 android:windowBackground、dialogCornerRadius 时按此绘制
- 〔适用情境 / 做法第 2 步〕material 1.12.0 的 Theme.MaterialComponents.Light.Dialog 经 Base.V14.Theme.MaterialComponents.Light.Dialog.Bridge 继承到 Platform.MaterialComponents.Light.Dialog，后者的 parent 是 Theme.AppCompat.Light.Dialog，窗口几何沿用 appcompat 的对话框主题；Base.V14.Theme.MaterialComponents.Light.Dialog 设 colorPrimary = @color/design_default_color_primary（#6200EE），应用主题没有另设 colorPrimary 时对话框里取这个色
- 〔适用情境 / 做法第 2 步〕material 1.12.0 的 Widget.MaterialComponents.Button.TextButton 文字色是选择器 mtrl_text_btn_text_color_selector：可用时为 ?attr/colorPrimary（alpha 1.00），不可用时为 ?attr/colorOnSurface（alpha 0.38），可勾选且未勾选时为 colorOnSurface（alpha 0.60）；样式没有另设 android:textColor 时按此
- 〔适用情境 / 做法第 2 步〕CustomDialogController 不设对应项时：遮罩色 maskColor 为 0x33000000（约 20% 不透明的黑，安卓平台基础主题暗化为 0.6），autoCancel 为 true（点遮罩关闭），背板圆角 32vp，弹窗宽度默认最大 400vp
- 〔做法第 2 步〕appcompat 1.7.1 的 AppCompat 主题没有另设 homeAsUpIndicator 时，返回箭头是 abc_ic_ab_back_material：24dp × 24dp 矢量（viewport 24 × 24），android:autoMirrored="true"（RTL 下自动镜像），android:tint="?attr/colorControlNormal"，pathData 为 M20,11L7.8,11l5.6,-5.6L12,4l-8,8l8,8l1.4,-1.4L7.8,13L20,13L20,11z
- 〔做法第 2 步〕Image 的 matchTextDirection 不设时为 false，图片在 RTL 语言环境下不镜像；设为 true 才镜像翻转（参数为 AnimatedDrawableDescriptor 时不生效）
- 〔做法第 2 步〕TextView 没有另设 lineSpacingExtra / lineSpacingMultiplier 时额外行距为 0、行距倍数为 1.0；setLineSpacing(add, mult) 对除最后一行外的每一行把行高乘 mult 再加 add，add 的单位是像素
- 〔做法第 2 步〕Text 的 lineSpacing 不设时行间距为 0，设小于 0 的值按 0；API 20 起的 LineSpacingOptions.onlyBetweenLines 不设时为 false，此时首行上方和尾行下方也有行间距（安卓只加在最后一行以外的各行）；lineHeightMultiple（API 22 起）把行高设为倍数 × 字高，取有效值时 lineSpacing、lineHeight 不生效
- 〔做法第 3 步〕intl.RelativeTimeFormat 的 format(value, unit) 只把调用方给的数值和单位本地化，unit 限 year、quarter、month、week、day、hour、minute、second，不按时间差自动挑单位、不做阈值取整；numeric 不设时为 always（输出 “1 day ago” 这类数值形式，auto 才输出 “yesterday”），style 不设时为 long；该接口 API 20 起废弃
- 〔做法第 2、3 步〕java.lang.String 的 split(regex) 参数按正则解释，等同 split(regex, 0)，结果末尾的空串都被去掉；输入开头的零宽匹配只在应用运行于或 targetSdk 为 28 及以下时产生开头空串
- 〔做法第 2 步〕安卓的 java.util.regex 以 ICU 为后端，预定义字符类总按 Unicode 解释：\s 是 \p{IsWhite_Space}，\d 是 \p{IsDigit}（含非 ASCII 数字），\w 是 [\p{alpha}\p{gc=Mark}\p{digit}\p{gc=Connector_Punctuation}\p{Join_Control}]；UNICODE_CHARACTER_CLASS 标志在安卓上会抛 IllegalArgumentException
