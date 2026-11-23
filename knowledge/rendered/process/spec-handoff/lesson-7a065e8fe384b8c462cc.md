# 规格或派工与写前读到的源码、主题或映射参考冲突或遗漏时，按源端可观察行为实现并回报规格分歧；只有决策台账中带决策 ID 的取舍才例外，source-notes 登记与转述不算批准

## 何时使用

页面或数据层实现阶段，规格或派工给出的容器、样式、类型写法、槽位或验收条目与写前读到的源码、主题或映射参考不一致，或验收条目没有列出源码里可见的行为时；重构或模块迁移阶段，规格清单要求改变已与源端一致的现有行为时

## 适用情境

实现者同时读到规格或派工与源布局、源码、主题文件、映射参考或 SDK 声明，规格的具体写法（含验收条目里的列表范围、过滤条件、容器类型、要求新建的槽位、所引源布局、列举顺序、启动去向）与源端可观察行为或参考映射不符，或验收条目漏掉了源码对展示内容的加工；规格对该处只有概括性理由或没有提及。也包括规格的 gap 条目写着“源端是 X、规格要求 Y、按规格实现”，而现有目标实现已与源端一致。派工声明“规格为权威”、规格条款（取值、方向、数量等）与源码运行语义矛盾而已有实现恰好符合源码时同样适用。也包括巡检或修复单的修法与决策台账总则（如核心流程必须真实可用）、工程硬性条款或源端行为冲突，修复者写前同时读到了双方。 也包括上游审计或规格写入了源码没有的防护属性（如“有界去重队列”），或摘要漏写源码里的分支（手势专用的动画时长、一次性引导），而实现者写前手里同时有源码。

## 例外与边界

- 决策台账中有带决策 ID（如 D-、PD-）的条目明确声明与源端不同的取舍（验收条目带决策锚点或 decision_ref），此时按该决策实现，并在报告里写明与源码的差异；规格或派工里的转述值、锚点仍指向源码而 decision_ref 为空的条目不算决策
- 按源端实现时，目标组件不写的属性会带出目标平台自己的默认表现，不等于和源端一致：如 NavDestination 不设 hideTitleBar 时显示系统标题栏，Button 不设 type 时 API 18 起为圆角矩形、之前为胶囊，animateTo 不写 duration 时为 1000ms；源端没有或取值不同的，显式关掉或写成源端的值。

## 原因

规格、派工和映射参考是对源端行为的二手概括，可能写错容器、取值范围或顺序，也可能漏掉可见行为。实现者已读到相反输入，却以符合规格或验收项未列为由保留差异，就会把概括错误落实到代码；重构时同样可能把已正确的行为改偏。这里的偏差是转述错误覆盖已确认的源端语义，而非明确批准的行为取舍。例外条款若只写“规格或决策记录写明取舍”，转述成另一个字面值的验收条目也会被当成决策；“标注差异”又会被读成目标相对源端的收敛写进笔记即可保留。

## 做法

1. 写码前对冲突点逐一取舍：先查决策台账有无带决策 ID 的条目覆盖该差异；没有就以源端可观察行为为准实现（规格只有概括性理由，或把源资源值转述成另一个字面值、锚点仍是源码时同样如此）；涉及 API 签名的以本地 SDK 声明为准。验收条目标注了源码出处时，打开该出处核对。
2. 源码里有、验收条目没写的可见行为，不能据此判定可删：按源码实现；做不了就登记占位，并在报告未决项里写明降级。
3. 在转换或迁移报告里列出与规格不同的每一处及依据，供规格阶段回改；不要为了与规格一致而删掉已确认的源端语义，也不要在注释写“交验证复核”后仍按规格值改掉已符合源码的实现。
4. 重构或模块迁移默认保持现有行为：现有实现已与源端一致、只有规格清单不同时，改规格或登记决策，不按清单改代码行为；真机验证也按源端期望断言，不把“符合当前规格”当作通过依据。
5. 执行巡检或修复单时同样对照台账与工程硬性条款：修复单把某项失败语义扩大成阻断核心功能等与台账冲突的要求时，按台账与源端行为实现，并在回执里标出与修复单的分歧。
6. 上游审计或规格加入源码没有的属性（去重、条数上限、点击清空）或漏写源码分支时，同样以源码为准实现，在交接里写明冲突；确需目标侧保护的另列为适配策略，说明对可见结果的影响后交负责方确认。
7. “标注差异”只记录规格与源码的分歧，实现仍按源端；目标相对源端少了可见行为（弹窗个数、回调次数、Toast）时不属于可标注的差异，要么按源端实现，要么作为待批决策写入台账或 handback 的 decision_gaps 等待裁决，source-notes 与注释里的登记不算批准。

来源支持：33 张卡 · 已知 16 次迁移（部分未记录） · 已知 15 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；android-36 的平台资源；com.google.android.material 1.4.0、1.14.0；androidx.appcompat 1.1.0、1.8.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕NavDestination 的 onBackPressed 只在与 Navigation 绑定的导航控制器中有内容时生效；按返回键时回调，返回 true 表示由页面自己处理返回，返回 false 回退到上一页
- 〔适用情境 / 做法第 1 步〕NavDestination 不设 hideTitleBar 时默认显示系统标题栏
- 〔适用情境 / 做法第 1 步〕Text 的 fontWeight 传 number 时取值 [100, 900]、间隔 100，不设时为 400
- 〔适用情境 / 做法第 1 步〕FontWeight 枚举中 Medium 为 500 字重、Bold 为 700 字重，没有 600 字重的成员，600 只能传数值
- 〔适用情境 / 做法第 1 步〕Button 不设 type 时，API 18 及之后默认 ButtonType.ROUNDED_RECTANGLE，API 18 之前默认 ButtonType.Capsule
- 〔适用情境 / 做法第 1 步〕material 1.14.0 中 Widget.MaterialComponents.Button 启用态底色取 ?attr/colorPrimary、文字色取 ?attr/colorOnPrimary；禁用态底色为 12% 不透明度的 colorOnSurface，文字为 38% 不透明度的 colorOnSurface
- 〔适用情境 / 做法第 1 步〕material 1.4.0、1.14.0 的小组件圆角 mtrl_shape_corner_size_small_component 为 4dp；appcompat 1.1.0、1.8.0 的 Base.Widget.AppCompat.Button 最小高度 48dip、最小宽度 88dip
- 〔适用情境 / 做法第 1 步〕TableLayout 每列的宽度取该列所有行单元格测量宽度的最大值
- 〔适用情境 / 做法第 1 步〕RelativeContainer 的子组件要有唯一 id 才能被其他子组件引用为锚点，父容器的标识默认为 __container__
- 〔适用情境 / 做法第 6 步〕animateTo 的 AnimateParam.duration 单位是毫秒，不写时为 1000
- 〔适用情境 / 做法第 6 步〕Curve.FastOutSlowIn 是 cubic-bezier(0.4, 0.0, 0.2, 1.0)，与安卓 @android:interpolator/fast_out_slow_in 的控制点（0.4, 0, 0.2, 1）相同
- 〔做法第 1 步〕java.time.LocalDate#compareTo 依次比较年、月、日；Kotlin 里 date >= today 经 compareTo 判断，对同一天也成立
- 〔做法第 1 步〕javax.crypto.Cipher#doFinal 在解密模式且要求去填充时，去填充失败抛 BadPaddingException；分组密码在加密模式下未要求填充且输入总长不是块长整数倍，或算法无法处理所给输入时，抛 IllegalBlockSizeException
- 〔做法第 1 步〕org.json 的 JSONObject.getString 对 JSON null 返回字符串 "null"（JSON null 解析为 JSONObject.NULL，再按 String.valueOf 转成字符串），对数字返回其字符串形式，只有键不存在时抛 JSONException
- 〔做法第 1 步〕JSONObject.getJSONArray 在键不存在或值不是 JSONArray（含 JSON null）时抛 JSONException，不会读成空数组
- 〔做法第 1 步〕JSONObject.getInt 对小数取 intValue() 截断，对数字字符串按 (int) Double.parseDouble 截断
- 〔做法第 1 步〕JSONObject.put(name, null) 删除该键已有的映射，输出里没有这个键；JSONStringer 输出字符串时在 '/' 和 '\' 前加反斜杠，'/' 输出为 \/
- 〔做法第 1 步〕android.os.FileUtils.buildValidFatFilename 把 FAT 文件名里的非法字符换成 "_"，名称为空、"." 或 ".." 时返回 "(invalid)"，结果截到 255 字节
- 〔做法第 1 步〕SliderOptions.step 是滑块步长，默认 1，取值范围 [0.01, max - min]，设成小于 0 或大于 max 的值时按默认值处理
- 〔做法第 1 步〕accessibilityLevel 默认 "auto"；取 "no" 时该组件不被无障碍服务识别，取 "no-hide-descendants" 时组件及其子组件都不被识别
- 〔做法第 1 步〕HitTestMode.Transparent：自身和子节点都响应触摸测试，同时不阻塞兄弟节点和祖先节点的触摸测试
- 〔适用情境 / 做法第 1 步〕桌面显示的应用名和图标优先取 module.json5 中 mainElement 指向的入口 UIAbility 的 label、icon；入口 UIAbility 没设 label 或 icon 时才取 app.json5 的
- 〔适用情境 / 做法第 1 步〕ApplicationContext.restartApp 重启应用并拉起指定 UIAbility，重启时不触发 onDestroy；应用不在界面顶层时抛 16000053，目标不属于本应用或不是 UIAbility 时抛 16000063，两次重启间隔不足 3 秒时抛 16000064
