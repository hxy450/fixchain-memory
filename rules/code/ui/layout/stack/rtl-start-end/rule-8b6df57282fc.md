# 第三方容器内部是否随 RTL 镜像，读它的 onLayout 定，不由外层 Start/End 推断

审的是：代码
触发（任一种）：
- 读到：源布局里第三方自定义容器（如 getbase 的 FloatingActionsMenu）带 android:layout_gravity="bottom|end"、layout_marginEnd，内部子项由容器自己排；写错的样子：目标端把容器内部的子项（按钮列、标签）也整体随方向镜像，或整体不镜像，代码和注释里没有依据容器的 onLayout
适用范围：源应用清单 android:supportsRtl="true"，迁移第三方容器类控件时
做法：
- 读第三方容器的 onMeasure/onLayout（只有编译产物时反编译），看子项排列是否读 getLayoutDirection / isLayoutRtl
- 内部不随方向镜像的：外层位置照 Start/End 写 start/end 随方向镜像，内层容器写 .direction(Direction.Ltr) 固定从左到右，需要按当前方向取物理一侧时用 i18n.isRTL 判断
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- direction(value: Direction): T：组件的布局方向（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.direction）
- Direction.Ltr（从左到右）、Direction.Rtl（从右到左）、Direction.Auto：固定内层不镜像用 Direction.Ltr（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Direction）
- export function isRTL(locale: string): boolean：判断当前是不是 RTL（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，i18n.isRTL）
- 外层 padding end 随方向镜像、内层 Column 固定 Direction.Ltr：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 第三方容器内部排子项时是否读布局方向：Gradle 缓存里该库的 aar/jar（多半只有 class）或库的源码包，按容器类的 onLayout、onMeasure 找；子项坐标只按左/右算、不读 getLayoutDirection / isLayoutRtl 的，就是内部不镜像
未核实：i18n.isRTL 最新一段注释把参数说成「输入字符」，早先几段说是 locale，传什么参数未核；卡里环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-927e26bb7b18f83f2f38（omni-notes-hmos）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断；取值 4 ← 诊断
