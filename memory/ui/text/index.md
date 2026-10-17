# ui/text

文本展示与排版：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，Compose 行高到单行文本盒与多行行距的映射，多行末行省略的截断粒度，静态说明页的逐字文案与图文结构，Tab、页面标题、设置行等可见文案的逐字取值，以及字符串资源生成哪些语言限定目录，单行中间/开头省略的测量截断，setSpan 区间拆成 Span 时的着色范围，以及数值显示精度（复用基类格式化 getter 与品类精度不一致时的子类覆写），以及源端代码格式化文案的参数化字符串资源，代码内取资源字符串的接口与应用偏好语言，按 locale 的全大写变换（textAllCaps）；文案资源缺键时的专属新键、带原值移交与补值来源，带标记字符串资源（Html.fromHtml）的富文本与链接，语言目录与键集按源端镜像；Compose 字重到数值 fontWeight，可折叠正文的溢出测量与 overflow 默认值，android.R.string 系统文案的多语言落地

[上一级](../index.md)

## 本级经验

- [Compose FontWeight 按数值字重写入 ArkUI：SemiBold、Light 等没有同名枚举成员时写 fontWeight(600/300)，编译修复不就近换成 Medium、Lighter](lesson-605038b091e03c26c005.lesson.md)
  - 时机：界面实现与主题排版阶段，把 Compose FontWeight 写成 ArkUI fontWeight 时；编译修复遇到 FontWeight 缺少某成员的报错时
  - 情境：源端 Text 或 TextStyle 用 FontWeight.SemiBold、Light、ExtraBold、Thin、ExtraLight、Black 或 FontWeight(数值)；ArkUI 的 FontWeight 枚举只有 Lighter、Normal、Regular、Medium、Bold、Bolder，写成 FontWeight.SemiBold 会报 “Property 'SemiBold' does not exist on type 'typeof FontWeight'”；fontWeight 属性同时接受 100–900 的数值。
- [Compose 可折叠正文（onTextLayout 的 didOverflowHeight 决定展开钮、maxLines 折叠）迁 ArkUI：用文本测量比较限行与不限行高度判定溢出，overflow 按源默认 Clip，其余加工与交互逐项落实](lesson-c61ac79c7db81729a544.lesson.md)
  - 时机：界面实现阶段，把 Compose 可折叠文本卡转换为 ArkUI 组件，确定是否显示展开按钮、折叠态 overflow 与文本加工时；占位复核阶段决定字符数近似是否保留时
  - 情境：源 Text 用 onTextLayout { didOverflowHeight / hasVisualOverflow } 决定是否显示展开钮，maxLines 在折叠与展开间切换且未设 overflow（Compose 默认 Clip），正文可能经 buildAnnotatedStringWithUrls 等加工，外层 toggleable/clickable 带按压反馈；ArkUI Text 没有同名排版回调，写者可能用字符数阈值近似。
- [SpannableString.setSpan(start, end) 拆成 ArkUI Span 时按 end 为开区间逐字核对着色范围](lesson-eb59a95e5eb219c238b0.lesson.md)
  - 时机：界面实现阶段，把源端 setSpan 着色、加粗的文字拆成 ArkUI Text + Span 时
  - 情境：源端用 SpannableString.setSpan(span, start, end, flags) 按字符索引给一段文字着色，常见“固定前缀 + 动态值 + 后缀”的拼接，终点按前缀长度加动态值长度再加偏移计算。
- [Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 strings 资源的逐字值，不用枚举名、路由名或自拟英文](lesson-31ab9f59945e5f0259ea.lesson.md)
  - 时机：界面实现阶段，为 Tab 标签、页面/路由标题、设置入口行等可见文案取值并写入页面与路由表时；以及派发侦察或规格任务、确定导航与标题字段的形态时
  - 情境：源端可见文案经资源键间接引用（导航目的地的 label、配置路由的标题资源、顶栏 title），常与目的地枚举名或功能名不同（如 Map 目的地显示“Mesh Map”、Messages 目的地的页面标题为“Conversations”）；目标以硬编码字符串或自建资源表承载；上游 brief 或页面规格已给出、或可从 strings.xml 解析出逐字值。
- [maxLines + Ellipsis 截断粒度两端不同：单行用户内容加 wordBreak(BREAK_ALL)，多行末行写明差异，确需字符级一致才测量截断](lesson-836a5414b52f0e062f1f.lesson.md)
  - 时机：规格提取阶段为带 maxLines(N) + TextOverflow.Ellipsis（或 android:ellipsize、singleLine）的单行标题或多行正文写转换决策，以及界面实现阶段落实单行省略位置与折叠态末行时
  - 情境：源端多行正文以 maxLines + Ellipsis 折叠；目标用 .maxLines() + .textOverflow({ overflow: TextOverflow.Ellipsis })，默认 wordBreak 为 BREAK_WORD；映射参考只记 ellipsize → textOverflow 的 API 对应；项目可能要求完整复刻源端可观察行为。也包括工具栏标题、笔记标题、分类名等单行用户内容：源端 Toolbar 标题或 singleLine TextView 由 TextUtils.ellipsize 按字符省略，目标写成 maxLines(1) + Ellipsis 而未设 wordBreak。也包括源控件是自带截断算法的三方 TextView 子类（布局声明了库命名空间且无 android:ellipsize），省略规则由库决定。
  - 例外：项目允许平台差异、不要求逐字复刻末行时，直接使用内置行为，不引入运行期测量
- [代码内经 resourceManager 取字符串、数组、复数、颜色一律传 $r(...).id，与声明式 $r 同一解析路径，不用 Resource 重载](lesson-22432022455bff6f849b.lesson.md)
  - 时机：界面实现阶段，把安卓命令式取字符串（getResources().getString，如自绘 View 里 drawText、measureText 的文案）改写为 ArkTS 代码内取值并选择 resourceManager 接口时；后续切片扩展已有取值写法时；为字符串数组、复数、颜色等其他取值方法写新文件或新辅助函数时
  - 情境：源端在自绘 View 或代码里按当前资源配置取文案；目标需要在 ArkTS 中拿到纯字符串（Canvas 绘制、测宽、拼接），同一屏还有走声明式 $r 的组件文本；应用带多个 locale 资源目录，可能以应用偏好语言运行。
- [分开单行文本盒与多行行距，不把 Compose lineHeight 同名直映为 ArkUI .lineHeight](lesson-2a2924aaebbfbea80780.lesson.md)
  - 时机：规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时
  - 情境：源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。
  - 例外：当前源端的 LineHeightStyle、字体内边距或已有明确契约要求固定行盒时，保留该契约，不默认改成自然高度。
- [动态布局文本的字号、行距按源端 dp × 文字倍率落成 vp，只有 bounds、padding、背景等几何乘设计画布比例](lesson-4c494b9f89c7e9db2b55.lesson.md)
  - 时机：动态或灵活组件的渲染实现阶段，把源端动态布局文本的字号、行距换算成 ArkUI 预览、测量或原生绘制尺寸时
  - 情境：源端动态文本以 fontSize.dpF × dynamicTextScale × fontSizeScale 设字号、以 lineSpacing.dpF 设行距，只有节点宽高、位置、padding、背景按根尺寸与设计宽度之比缩放；目标预览用 renderWidth / document.width 一类画布比例统一换算几何。
- [单行 ellipsize=middle/start 在目标 TextOverflow 没有同名成员时实现测量式中间截断，不降级为尾部省略](lesson-a184209501ba02cb62e7.lesson.md)
  - 时机：界面实现阶段，转换单行文本的省略位置（ellipsize），而目标 TextOverflow 枚举没有对应成员时
  - 情境：源 TextView 用 android:ellipsize="middle"（或 start）配合 lines=1/maxLines=1 显示文件名等尾部有意义的文本，可能还有关键字 Span 高亮；ArkUI Text 的 TextOverflow 只有尾部 Ellipsis 等模式，映射参考只给 end → Ellipsis 示例。
  - 例外：项目已批准以尾部省略作为平台差异
- [可能为空的 TextView 迁 Text 时保留一行高：Android 空文本仍占一行字体高，ArkUI 空 Text 高为 0](lesson-6668f8800d3ddaaf52ed.lesson.md)
  - 时机：界面实现阶段，为可能显示空串的标题、正文预览、附件文字条确定渲染条件与行高时
  - 情境：源 TextView 高为 wrap_content，文本可能为空（无标题、空正文、名称缺失），或为 visibility=invisible、setVisibility(INVISIBLE)；相邻元素（日期行、正文起始行）依赖它的占位定位；目标准备写 if (text !== '') 条件渲染，或用 Visibility.Hidden 后直接绑定可能为空的串。
  - 例外：源端该 TextView 为 GONE，或文本为空时代码将其设为 GONE
- [可见文案改为资源引用时值取自源端原文：目标字符串表缺键就新建专属键并连同原值移交，补值者回查源布局，不用语义相近的现成资源或按键名自拟](lesson-4567f9f77f4280ec1747.lesson.md)
  - 时机：页面转换、切片实现与组收口阶段，源端文案在目标 string.json 中没有对应条目，或把页面字面量改成由他人单写的资源引用、由收口者补值时
  - 情境：源布局或源码给出页面专属文案（如空态“暂时没有常用的路线”、隐私弹窗“同意并继续/不同意”）或纯数字徽标序号（android:text="1"…"4"），目标字符串表没有对应键，共享资源文件由收口 agent 单写；工程里有语义相近的通用资源（“暂无数据”、他页“隐私政策”、“取消/确定”）可引用；交接可能只给键名不给值，显示容器可能是固定尺寸的小徽标。
  - 例外：纯数字等不需要翻译的序号可以保留字面量，不必新建资源
- [复用基类的显示格式化 getter 前核对精度：品类精度不同（如 ETF 三位小数）时在子类覆写全部相关 getter，同一字段的各分支用同一精度](lesson-042445ba332611e04a80.lesson.md)
  - 时机：界面实现阶段，把源端十字光标、高亮联动等显示接入目标页面，决定复用基类 ViewModel 的格式化 getter 还是在子类覆写时；修改同一显示字段的任一分支（静态值、无数据兜底、高亮值）时
  - 情境：多个品类详情页共用一个基类 ViewModel，基类显示 getter 用通用精度格式化（如 formatPrice 保留两位）；某一品类的静态字段与源端联动代码使用不同精度（如 getPrice(..., 3)），子类尚未覆写对应 getter。
- [字符串语言限定目录与键集按源端实际存在的 values-&lt;语言&gt; 镜像：源端有几种语言就迁几种，限定词粒度照源（values-zh→zh），单语源不合成译文，源 locale 缺键保持缺失、回落 base](lesson-b58df29f032cc6a8c9d6.lesson.md)
  - 时机：规格提取与资源迁移阶段，确定要迁移哪些 values-* 语言目录及其目标限定词、目标生成哪些语言限定字符串目录及各键取值、源 locale 缺键如何处理时
  - 情境：Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。也包括源端有多个 values-xx（如 es/fr/it/pt/ru/zh/zh-rTW）并提供应用内语言切换，规格或主会话却自定“默认只迁 values + values-zh”，并以“项目决策优先”覆盖资源 skill 的“全部转换”硬规则；部分语言目录键集不全，skill 要求键集一致并自动补译。也包括源端只有仅语言限定的 values-zh，skill 正文写“values-zh-rCN 或 values-zh → zh_CN 或 zh”并要求最少生成 zh_CN，而详细映射表写 values-zh→zh、values-zh-rCN→zh_CN。 也包括 i18n 审计按“base 文件集合与每个语言目录一致”报缺项，补齐脚本把 base 下 color、float、boolean、integer 等非文字资源文件整份复制进语言目录。
  - 例外：规格或决策明确要求本轮新增本地化语言；此时按批准的译文来源生成，并在报告中注明源端没有该语言；源端引用 android.R.string.* 等框架字符串：译文由系统按设备语言提供，按系统字符串的经验为已有语言补框架译文（必要时补地区目录）
- [源端 textAllCaps（含 Button 与 AlertDialog 按钮样式默认的全大写）必须显示为全大写，按资源原样不是可接受的降级：取资源字符串后按当前 locale toLocaleUpperCase（Resource 参数先 getStringSync），封装成共享 allCaps 复用；textCase(UpperCase) 只转拉丁字母，不用它代替](lesson-cce58a1538fedfda3695.lesson.md)
  - 时机：界面实现或返修阶段，把安卓 textAllCaps（含按钮样式默认的全大写）移植为 ArkUI 文本，确定取字符串方式与 locale 标签，或给多个页面的按钮统一做大小写变换时
  - 情境：安卓按钮或文本靠 textAllCaps（AllCapsTransformationMethod 按当前 locale 大写）显示全大写，资源串多为首字母大写（Yes/No、New Game）；应用带含非 ASCII 或非拉丁字母的多语言资源（de 的 ü、tr 的 i/İ、ru 的西里尔字母），也可能以只有语言码的应用偏好语言运行；目标按钮参数常是 Resource/ResourceStr，要自己取字符串做大写，并把 resourceManager 配置的 locale（下划线分隔、子标签可能为空，如 fa_Arab_）转成 BCP 47 标签。也包括工程里已有按 locale 大写的私有实现，其他页面又用 textCase 另写一套。
- [源端在代码里格式化的含固定措辞文案（SimpleDateFormat、String.format、拼接）也建参数化字符串资源并用 $r 传参，不写模板字符串](lesson-d442eb6e9aab4d77db18.lesson.md)
  - 时机：界面转换阶段，为源端在代码里动态生成的可见文案（日历年月标题、带单位的数量等）选择文本来源并登记字符串资源时
  - 情境：Android 源在 Kotlin/Java 里用 SimpleDateFormat、String.format 或拼接生成带中文单位或固定措辞的显示文本（如 yyyy年M月），不在 strings.xml 中；目标工程约定可见文案走 $r('app.string.*')，模块 string.json 已有 %s 参数化条目。
  - 例外：文本只由纯数字或数据值构成（如日期格子的 day.toString()）
- [移植文本组件时先确认显示的是原始字符串还是加工后的富文本（Compose AnnotatedString、Html.fromHtml、带标记的字符串资源），样式、链接识别与点击要落到目标端；Html.fromHtml 只产出单个符号实体、按大字号逐个生成作页码点等图形时不算富文本，按源字体下的可见几何绘制图形](lesson-57a52be767730880cbba.lesson.md)
  - 时机：界面实现阶段，把源端 Compose Text、TextView 或对话框正文译成 ArkUI Text 时
  - 情境：源组件先调用工具函数（如按正则识别 URL、附加 LinkAnnotation 的 buildAnnotatedStringWithUrls）生成 AnnotatedString 再交给 Text；目标页面规格和验收条目只写了空值隐藏、折叠展开等布局行为。也包括 View 体系以 Html.fromHtml、setMessage(resId) 或 android:text 引用带 `&lt;b&gt;`/`&lt;i&gt;`/`&lt;a&gt;` 标记或 CDATA 的字符串资源，并用 LinkMovementMethod 让链接可点；目标准备用 Text($r(...)) 直接显示，或在正文外另起链接行。也包括循环中逐个 new TextView、setText(Html.fromHtml("&amp;#8226;")) 并 setTextSize(35) 作翻页圆点：内容只有一个符号，可见尺寸、步进与垂直位置取决于源字体（Roboto）的字形度量。
- [系统文案（android.R.string.*、DialogPreference 默认按钮）建专属键补各语言框架译文，不借同名应用串](lesson-ff19b09146b57d0f91a8.lesson.md)
  - 时机：页面实现阶段，为源端 stringResource(android.R.string.ok)、@android:string/cancel 一类系统字符串选择目标文案来源并新建应用字符串键时；以及源偏好对话框、AlertDialog 未显式声明按钮文案，为目标弹窗按钮选择文案来源时
  - 情境：源码或布局引用 android.R.string.ok、cancel 等框架字符串，它们不在应用 strings.xml 中，由系统按设备语言提供译文；目标工程已有多个语言限定目录（可能区分简繁）；转换者准备新增一个应用键（如 button_ok），只在 base 写英文值。 也包括源偏好 XML 的 ListPreference、EditTextPreference 未声明 positiveButtonText/negativeButtonText，按钮文案由框架默认（@android:string/ok、cancel）提供，而应用自身恰有 ok、cancel、confirm 等同名或近义键。
- [说明类静态页按源布局逐卡迁移：文案逐字取自源 XML，标题条背景与插图一并迁入](lesson-0197307e63e8d848ba02.lesson.md)
  - 时机：界面实现阶段，依据源布局 XML 生成规则、说明、注意事项一类静态图文页时
  - 情境：源静态页由多张卡片组成，标题条使用 drawable 背景，正文是写在布局 XML 里的长文案，卡内或页首尾有插图；规格只要求“展示说明并可返回”，不复述内容。
