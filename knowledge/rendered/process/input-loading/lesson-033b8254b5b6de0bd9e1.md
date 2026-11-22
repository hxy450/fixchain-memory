# 页面、控件、算法或实体基类由二进制三方库承载时，按依赖坐标取库制品核对真值，不按调用面推断或以原生组件近似

## 何时使用

规格提取与实现阶段，为 build.gradle 二进制依赖（AAR/jar）承载的界面、提示条与对话框、手势、算法输出或实体基类写映射决策、行为契约或自研等价实现，以及为它们登记占位时

## 适用情境

仓库内只有调用面：Activity extends 库类，布局根节点或 UI 快照只剩库的自定义 View 类名，应用侧只留 Style/Configuration 常量或 Builder 调用，实体 extends 库基类，常量或正则来自库类；行为、几何、动画、队列、手势阈值、字段集或输出字符串都在库内。规格或映射参考写成「Toast / 原生组件 / 自研 / 系统 intl 替代」并标 Auto，或写「库源不可见→默认样式即可对齐」；本机 Gradle 缓存可能还没有该制品。

## 例外与边界

- 决策台账里有带编号、经用户批准的范围裁剪或降级，明确该库功能不复刻

## 原因

目标端没有同名库时，写者只看得到应用侧的调用、常量与类名，便按名字、属性或常量反推：库内的队列与出队时机、动画时长与插值、dimens 与布局、截断与行距、手势阈值与惯性、字段集与 equals、序列化字面形态和文案阈值都会丢失。登记成“近似”“待视觉对齐”的占位没有真值可对齐，到交付也兑现不了。坐标与版本就写在构建脚本里，“仓库内无源码”是可补的材料缺口，不等于行为不可知。

## 做法

1. 从 build.gradle（含 gradle.properties、版本目录）读出库坐标与版本，按序取制品：Gradle 用户缓存 ~/.gradle/caches/modules-2/files-2.1/<group>/<artifact>/<version>/<文件 SHA-1 的十六进制，去掉开头的 0>/（构建时解包过的 aar 在 caches/transforms-3（更早是 transforms-2）或 caches/<Gradle 版本号>/transforms 下的 <哈希>/transformed/<artifact>-<version>/）；没有就用 Gradle 解析下载该依赖，或按坐标从 Maven 仓库（androidx、Material 组件在 Google Maven，其他库常见于 Maven Central；路径为 <group 的点换成斜杠>/<artifact>/<version>/，同目录常有 -sources.jar）、JitPack（https://jitpack.io/com/github/<owner>/<repo>/<version>/）、上游仓库对应版本 tag 获取，有 sources jar 时优先。
2. 解包后按库的职责取真值：UI 库读 res 的 layout、values（aar 里每个 values 限定目录合并成一个 values*.xml，dimens、styles、strings、integers 都在里面；限定目录名可能带构建时补的版本后缀，如 values-sw600dp-v13、values-night-v8）、anim/animator、drawable 及其限定目录（layout-land、values-sw600dp 等），并用 javap -p -c 或反编译读控件、管理器与 Builder 的测量、缺省参数、动画、队列与触摸分支；先列出库内全部视图类，再判断目标组件是否足够（图片查看器的缩放、平移、双击、惯性属于库行为，不是可省略的增强）。实体基类读字段集、类型、缺省值、equals/toString 与序列化规则；库里的常量与正则按库值迁移。 只有编译 jar、没有 sources jar 不等于不可核：用 javap -p -c -constants 读构造器缺省分支与 companion 常量（Kotlin 函数的缺省参数在 <名字>$default 合成方法里按掩码位赋值；companion 属性的存储字段在外部类上，对外部类读），本机未装 JDK 时用 Android Studio 自带的 jbr/bin/javap；动效与物理类库读更新与发射方法，确认参数的时间域（每帧还是每秒）、帧率归一化、重力与质量、阻尼、寿命与淡出，再写常量与步进。上游提醒或注释写“库源不可核”时先自己核一次。
3. 算法库（重复规则、相对时间、日期格式、文本拆分与序列化）用 JDK 小程序加载同版本 jar 跑代表输入（执行路径上调用 android.* 的库桌面 JDK 跑不了：SDK 里 android.jar 的 android.* 类只有抛 "Stub!" 的桩），把输出的字面形态（时区形态、行尾、文案模板、单位阈值与取整）写成契约；登记常量时同时登记它经库序列化后的字符串。系统 i18n/intl 只在与库输出对代表输入逐字一致时替代；库有自有阈值、模板或资源表时移植算法与资源。
4. 把真值写进规格映射行或组件头注释，注明库内文件、资源名或类方法与版本；映射行的依据只是仓库内调用行、README、单元测试或分析产物里的“建议”时，不标 Auto、不进跨栈硬映射基线，实现也不凭样式常量类自定时长、角度或间距。
5. 确实取不到时，在规格逐项列出缺失的库真值（队列时序、几何、手势、序列化格式、文案）及其影响，登记为阻塞或交用户改判；不写「默认样式即可对齐」，也不把这类占位的兑现交给视觉对齐步骤。派工给出 Android 源码路径时，一并给出库制品缓存路径与可解包提示。

来源支持：23 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1；平台 android-36（android.jar、data/res）；appcompat 1.8.0、core-ktx 1.9.0、material 1.12.0（aar、pom、module，字节码用 JBR 21.0.10 的 javap 读）；Gradle 缓存目录按 8.14.3、9.0.0 及 transforms-3 的现状核；Google Maven、Maven Central 按 2026-11-21 的线上状态核。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕Gradle 的模块缓存按 caches/modules-2/files-2.1/<group>/<artifact>/<version>/<文件的 SHA-1>/<artifact>-<version>.<扩展名> 存放：同一版本的 aar（或 jar）、pom、module、sources jar 各在一个以该文件 SHA-1 的十六进制命名的子目录里，按文件名找要往下多走一层；目录名去掉了十六进制开头的 0，SHA-1 以 0 开头的文件目录名不足 40 位（material 1.12.0 的 pom 的目录名是 39 位）
- 〔做法第 1、2 步〕构建时解包过的 aar 另存在 transforms 缓存：较早的 Gradle 在 caches/transforms-3（或 transforms-2）下，Gradle 8.14.2、8.14.3、9.0.0、9.5.0、9.8.0 在 caches/<Gradle 版本号>/transforms 下，路径为 <哈希>/transformed/<artifact>-<version>/。同一个库的同名 transformed 目录常有几份，完整解包的那份里有 jars/classes.jar（常还有 jars/lint.jar）、res/、R.txt、public.txt、AndroidManifest.xml、proguard.txt，其余几份只有部分内容。名字带 -runtime 的目录里只有 classes.dex（已转成 dex）或是空的，javap 读不了；同级的 <artifact>-<version>-runtime.jar 是 class 文件的 jar，-api.jar 里是生成的 R 类
- 〔做法第 1 步〕官方 Maven 仓库按 <group 的点换成斜杠>/<artifact>/<version>/<artifact>-<version>.<扩展名> 存放：androidx 和 Material 组件在 Google Maven（dl.google.com 的 android/maven2 下），同目录有 -sources.jar（appcompat 1.7.1、material 1.12.0 都有），<artifact>/maven-metadata.xml 列出这个库的可用版本，Google Maven 另有 <group 路径>/group-index.xml 列出这一组各库的版本；Maven Central（repo1.maven.org 的 maven2 下）同样按这个路径布局、有 maven-metadata.xml，没有 group-index.xml，许多纯 Java 库也发 -sources.jar（prettytime 3.2.7.Final 有）
- 〔做法第 1 步〕库的 pom 列出它直接依赖的库及版本和 scope（material 1.12.0 的 pom：activity 1.8.0、annotation 1.2.0、appcompat 1.6.1 等，scope 多为 compile，error_prone_annotations 为 runtime，kotlin-bom 以 import 放在依赖管理里），Gradle 的 .module 文件按发布变体列同样的依赖；行为落在被依赖的库里时，按这里的坐标和版本再取那个库
- 〔做法第 2 步〕aar 是 zip：根目录有 classes.jar、res/、R.txt、public.txt、AndroidManifest.xml、proguard.txt，常见还有 lint.jar、annotations.zip、baseline-prof.txt。res/ 下每个 values 限定目录合并成一个与目录同名的文件（res/values/values.xml、res/values-<限定>/values-<限定>.xml），dimens、styles、strings、integers、colors 都在里面，没有单独的 dimens.xml、styles.xml。限定目录名（values 目录也一样）带构建时补的最低版本后缀：密度和 large、xlarge 补 -v4，night 补 -v8，sw/w/h<N>dp 补 -v13，ldrtl 补 -v17，watch 补 -v20（如 drawable-hdpi-v4、values-sw600dp-v13、values-h720dp-v13、values-night-v8、layout-watch-v20）；横竖屏（land、port）、语言和地区、本来就带 vNN 的目录照原样（values-land、values-zh-rCN、values-v21、layout-v26），按源码里的目录名找时要带上后缀
- 〔做法第 2 步〕库的 classes.jar 里没有 R 类；字节码按字段名引用资源（例：getstatic androidx/appcompat/R$attr.editTextStyle:I），看到的是资源名而不是数字 id，资源名与 aar 的 res/、R.txt 对应
- 〔做法第 2 步〕JDK 的 javap 只靠编译出的 class 就能读：-p（-private）列出全部类和成员，-c 反汇编方法体，-constants 显示 final 常量的值，-s 打印内部类型签名，-l 打印行号和局部变量表，-v 打印附加信息，-cp 指定 jar；类名写全限定名，嵌套类写 Outer$Inner。Android Studio 自带的 JBR（JDK 21）在安装目录的 jbr/bin 下带 javap、java、javac
- 〔做法第 2 步〕Kotlin 带缺省参数的函数编译成两个方法：原方法和静态合成方法 <名字>$default(原参数…, int 掩码, Object)；$default 开头逐位检查掩码，值参数从 0 编号（扩展函数的接收者不占位），第 i 号参数对应掩码值 1<<i，该位为 1 就把这个参数换成缺省值（例：core-ktx 的 Bitmap.scale(width, height, filter = true) 编译成 scale$default，掩码 & 4 不为 0 时把 filter 设为 true），缺省值要在 $default 方法体里读
- 〔做法第 2 步〕Kotlin 的 companion object 编译成嵌套类 <外部类>$Companion，外部类上有 public static final 字段 Companion 指向它；companion 里声明的属性，存储字段是外部类上的 static final 字段（private 属性另生成 access$get<名字>$cp 访问器），companion 的方法在 $Companion 类里，所以常量的值要对外部类读；标了 @JvmStatic 的方法另在外部类上生成同名的静态方法（例：TextAppearanceSpanCompat.create 两处都有）
- 〔做法第 2 步〕动画资源里 android:duration 的单位是毫秒，android:interpolator 写在同一元素上。属性动画（res/animator，Animator）没写 duration 时为 300ms，没写 interpolator 时用 ValueAnimator 的缺省；代码里的 ValueAnimator 没有另设时长和插值器时，时长 300ms、插值器 AccelerateDecelerateInterpolator（setInterpolator(null) 得到线性）；Animator 实际播放时长是设定时长乘以系统的动画时长缩放（开发者选项，默认 1.0，设为 0 时动画关闭）。补间动画（res/anim，android.view.animation.Animation）没写 duration 时为 0ms，没写 interpolator 时用 AccelerateDecelerateInterpolator，它的时长不乘这个缩放
- 〔做法第 3 步〕Android SDK 里的 platforms/android-<N>/android.jar 只供编译：android.* 类（以及 org.json 等）的方法体都是抛 RuntimeException("Stub!") 的桩，编译期常量字段的值保留（如 Color.RED）；android-36 的 jar 里 java.* 类带真实方法体，但桌面 JDK 运行时用的是 JDK 自己的 java.*。库在代表输入的执行路径上调用了 android.* 的，用桌面 JDK 加载 jar 跑不出真实输出；只有执行路径上全是 JVM 类（java.*、kotlin.* 和库自己的类）的才能这样跑
- 〔做法第 3 步〕Java 的 String.split(regex) 等同 split(regex, 0)：结果末尾的空串全部丢掉（全由分隔符组成的串得到空数组）；开头有非零宽的匹配时结果第一项是空串；一处都不匹配时返回只含原串的数组（空串得到只含空串的数组）；limit 为负数时末尾空串保留。开头的零宽匹配：桌面 JDK 21 和 targetSdkVersion > 28 的安卓应用不产生开头空串，targetSdkVersion ≤ 28 的安卓应用仍产生（安卓为旧应用保留的兼容分支）
- 〔做法第 3 步〕@ohos.intl 的 RelativeTimeFormat.format(value: number, unit: string): string 只按调用方给的数值和单位出字符串，unit 只能是 year、quarter、month、week、day、hour、minute、second，选哪个单位、换单位的阈值和取整都由调用方定；构造选项 numeric 默认 always、style 默认 long；这个类 API 8 起有、API 20 起废弃，建议改用 Intl.RelativeTimeFormat。@ohos.intl 基于 CLDR 数据实现，文档写明结果随 CLDR 版本可能调整（API 12 对应 CLDR 42），不要对格式硬编码
- 〔做法第 3 步〕@ohos.i18n 的 System.is24HourClock(): boolean（API 9 起）读系统是否用 24 小时制
