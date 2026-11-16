# 依赖库里取不到源码的类、方法和常量

agent 会看到什么：读到源码 import 或 extends 依赖库（aar / jar，如粒子库的 Party、Emitter，库里的 Pattern 常量）里的类和方法而源码树里没有它的定义，规格可能要求行为等价；产物里自研的等价组件、正则或算法按配置面、记忆、单测或 AC 反推，注释写「库无源码」「不可核」「风险低」，没有 FWD-REF 和缺口登记

## 通用查法

### 源端用到依赖库里的类和常量而源码树里没有时，按坐标取库制品读出实现再移植

审的是：代码
触发（任一种）：
- 读到：源码 import 或 extends 二进制依赖（aar / jar）里的类、方法或 Pattern 常量，源码树里搜不到它的定义；规格可能写了「行为等价」；写错的样子：目标自写的等价组件、正则或算法按配置面、记忆、单测用例或 AC 反推，注释写「库无源码」「不可核」「风险低」，没有对照库制品，也没有 FWD-REF 或缺口登记
适用范围：源端行为来自二进制第三方依赖、目标端要自研等价实现时
做法：
- 从源工程构建脚本 dependencies 里读出这个库的 group:artifact:version，到 Gradle 用户缓存 modules-2/files-2.1/<group>/<artifact>/<version>/ 下找 -sources.jar、jar 或 aar；本地没有就取 jitpack 等发布仓库或上游同版本 tag
- 有源码就按被调用的类名、常量名读原文；只有 aar / jar 时 unzip 出 classes.jar，用 javap -c -p 反汇编被调用的方法和构造器缺省分支，照读出的判定、正则、常量和时间域写目标实现
- 取不到制品时在实现处标 FWD-REF，登记决策缺口或占位并列出未核项；不按配置面、单测用例或验收条文反推
针对本应用要查的：
- 这个依赖的坐标、版本和制品：源工程模块构建脚本的 dependencies 块和版本目录里该库的 group:artifact:version；Gradle 用户缓存 caches/modules-2/files-2.1/<group>/<artifact>/<version>/，或 transforms 目录里解包后的 classes.jar；按坐标找到 -sources.jar / jar / aar，在里面按被调用的类名找定义；只有编译 jar 时用 JDK 的 javap（没装 JDK 可用 Android Studio 自带 jbr 里的 javap），加 -constants 看常量。例：依赖 nl.dionsegijn:konfetti-core 2.0.5 时，反汇编 Confetti.update 可见 speed 是每帧位移、每帧加 0.02 / mass 的重力
来源：3 张卡，1 个应用
- case-44a53125e4f44a862c80（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-6984b2614fabe391f2e7（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2
- case-e9189514e875ef00f96f（omni-notes-hmos）：做法第 2 步 ← 建议 3

## 规矩

- rule-ac119318d162｜源方法定义在依赖库里取不到源码时，实现处标 FWD-REF 并登记缺口，不按验收条文反推｜读到：源类 extends 依赖库里的父类，被调用的方法在源码树里找不到 .java 定义；写错：目标自写了近似实现，源码理解笔记写「差异风险低」或「按 AC 行为反推」，实现处没有 `FWD-REF` 标记、决策台账里也没有这条缺口
- rule-ef4f666211b1｜源码调用的第三方 jar 在工程里没有源文件时，按坐标取发布版源码迁真实正则和常量｜读到：源码用到依赖 jar 里的 Pattern 常量或方法（如标签、链接识别），源工程里搜不到它的源文件；写错：目标按单元测试用例反推出 RegExp（锚定 ^、单字符可识别、用 \p{N}），注释称「契约」
- rule-519571190036｜规格要求从三方库工件提取时，本地缓存为空就去取 aar 反编译，取不到登记占位｜读到：规格或映射表写「HARD 行为等价」「实现期必须从库工件（jitpack aar 反编译或上游 tag）提取」「禁止凭印象」，源端只看得到库的配置调用链；写错：自研的等价组件或序列化器按配置面近似实现（如 parse 只用 startsWith 剥行首符号），注释写「库无源码」「按 spec 取值」或自称行为权威，没有反编译对照，也没登记占位
- rule-a8f01743f20a｜自研替代三方库动效或物理组件前，从库制品反汇编更新与发射方法，确认时间域、重力和寿命｜读到：源码 import 三方库的粒子或动效组件（如 Party、Emitter），只传速度、阻尼、发射器等部分参数；写错：目标组件常量凭记忆写（把每帧速度当每秒再除以 60、用固定下沉漂移代替重力、没有寿命淡出），文件头或占位登记写「仅 classes.jar、库默认值不可核」，交给真机视觉核验
- rule-697a5a8cf969｜源端用 konfetti-core 2.0.5 的 Party 时，目标粒子按库的每帧运动模型和缺省外观实现｜读到：import nl.dionsegijn.konfetti.core.Party / Emitter，Party(speed = …, maxSpeed = …, damping = …, emitter = Emitter(…).perSecond(…)) 没传 colors、shapes、size、timeToLive；写错：目标粒子组件把 speed 当每秒再除以 60（`speed / 60`）、用固定下沉漂移代替重力、尺寸写成固定长条、默认单色、没有 timeToLive 后的 alpha 淡出
