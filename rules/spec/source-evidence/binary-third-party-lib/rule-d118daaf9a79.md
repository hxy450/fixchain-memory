# UI 由三方库渲染时，规格先取库制品写真值，取不到就登记缺库真值，不写默认样式可对齐

审的是：规格
触发（任一种）：
- 读到：源码只有 extends 三方库类（如 extends AppIntro2）、壳布局或调用代码；UI 快照只剩库的自定义 View 类名（如 com.appeaser.sublimepickerlibrary.SublimePicker、com.larswerkman.holocolorpicker.ColorPicker）；依赖里有该库坐标和版本；写错的样子：页面规格的转换决策写「三方库内部 UI 不可见 → 原生组件自研 / 二选一」「默认样式即可对齐」「源码不在本仓库 → 无 anchor」，没有库内几何和交互，也没有缺库真值的阻塞项
适用范围：规格提取阶段，页面或控件的整块 UI 由三方开源库（AAR）提供时
做法：
- 按依赖坐标和版本取库制品（本机 Gradle 依赖缓存没有，就让 Gradle 解析依赖，或按版本从 jitpack / GitHub 下载），解包 res/layout、res/values、res/drawable 并反编译 classes.jar，把几何和交互真值写进页面规格
- 取不到时在规格里写明「缺库真值」并登记阻塞，不写无证据的替代裁定
- 自检转换决策表：每个「自研 / 近似 / 替代」项的源证据必须是库内文件和位置，不是仓库里调用该库的行或分析笔记里的「建议」；缺证据的行不进跨栈硬映射基线
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 返修时把库 AAR 解包反编译后逐项重建（选择器、取色器、引导页底栏和翻页动画、图片查看器手势），与源端一致：库真值只能从制品里拿到（出处：卡里修好并验证过）
针对本应用要查的：
- 库制品的位置：源工程模块构建脚本 dependencies 里的坐标；本机 Gradle 依赖缓存的 modules-2/files-2.1/<group>/<artifact>/<version>/ 下的 .aar，或解包后的 transforms 目录里 <artifact>-<version>/res；缓存里有就直接解包；没有就解析依赖或按版本下载后解包，读 res/values 里的尺寸颜色、res/layout 的结构，反编译 classes.jar 看绘制和手势
未核实：生成环境能否联网或运行 Gradle 解析依赖，卡里没有记录
来源：1 张卡，1 个应用
- case-74b07cb94daa311f36b1（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 1 ← 诊断
