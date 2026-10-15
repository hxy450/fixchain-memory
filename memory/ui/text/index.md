# ui/text

文本展示与排版：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，Compose 行高到单行文本盒与多行行距的映射，多行末行省略的截断粒度，静态说明页的逐字文案与图文结构，Tab、页面标题、设置行等可见文案的逐字取值，以及字符串资源生成哪些语言限定目录，单行中间/开头省略的测量截断，setSpan 区间拆成 Span 时的着色范围，以及数值显示精度（复用基类格式化 getter 与品类精度不一致时的子类覆写），以及源端代码格式化文案的参数化字符串资源，代码内取资源字符串的接口与应用偏好语言，按 locale 的全大写变换（textAllCaps）；文案资源缺键时的专属新键、带原值移交与补值来源，带标记字符串资源（Html.fromHtml）的富文本与链接，语言目录与键集按源端镜像；Compose 字重到数值 fontWeight，可折叠正文的溢出测量与 overflow 默认值，android.R.string 系统文案的多语言落地；Button/TextView 自动字号的作用区与测量字体，单个符号字形当图形用时按可见几何绘制，资源字符串取得 string 后再按源端加工

[上一级](../index.md)

## 本级经验

- [Compose FontWeight 按数值字重写入 ArkUI：SemiBold、Light 等没有同名枚举成员时写 fontWeight(600/300)，编译修复不就近换成 Medium、Lighter](lesson-605038b091e03c26c005.lesson.md)
  - 时机：界面实现与主题排版阶段，把 Compose FontWeight 写成 ArkUI fontWeight 时；编译修复遇到 FontWeight 缺少某成员的报错时
  - 情境：源端 Text 或 TextStyle 用 FontWeight.SemiBold、Light、ExtraBold、Thin、ExtraLight、Black 或 FontWeight(数值)；ArkUI 的 FontWeight 枚举只有 Lighter、Normal、Regular、Medium、Bold、Bolder，写成 FontWeight.SemiBold 会报 “Property 'SemiBold' does not exist on type 'typeof FontWeight'”；fontWeight 属性同时接受 100–900 的数值。
- [Compose lineHeight 未配 lineHeightStyle 时，分开单行文本盒与多行行距，不直映为 ArkUI .lineHeight](lesson-2a2924aaebbfbea80780.lesson.md)
  - 时机：规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时
  - 情境：源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。
  - 例外：源 TextStyle 显式设置了 lineHeightStyle 时，不按本条的默认裁剪处理，按其设置推导单行盒高与行距
- [SpannableString.setSpan(start, end) 拆成 ArkUI Span 时按 end 为开区间逐字核对着色范围](lesson-eb59a95e5eb219c238b0.lesson.md)
  - 时机：界面实现阶段，把源端 setSpan 着色、加粗的文字拆成 ArkUI Text + Span 时
  - 情境：源端用 SpannableString.setSpan(span, start, end, flags) 按字符索引给一段文字着色，常见“固定前缀 + 动态值 + 后缀”的拼接，终点按前缀长度加动态值长度再加偏移计算。
- [Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 strings 资源的逐字值，不用枚举名、路由名或自拟英文](lesson-31ab9f59945e5f0259ea.lesson.md)
  - 时机：界面实现阶段，为 Tab 标签、页面/路由标题、设置入口行等可见文案取值并写入页面与路由表时；以及派发侦察或规格任务、确定导航与标题字段的形态时
  - 情境：源端可见文案经资源键间接引用（导航目的地的 label、配置路由的标题资源、顶栏 title），常与目的地枚举名或功能名不同（例：某目的地枚举为 Map，显示文案却是带前缀的另一个词；消息目的地的页面标题另取一个名称）；目标以硬编码字符串或自建资源表承载；上游 brief、页面规格或侦察清单给出了文案或只给了枚举名。
- [代码内取本模块字符串按数字 id 调 getStringSync($r(...).id)，不用 API 20 起弃用的 Resource 重载](lesson-22432022455bff6f849b.lesson.md)
  - 时机：界面实现阶段，把安卓命令式取字符串（getResources().getString，如自绘 View 里 drawText、measureText 的文案）改写为 ArkTS 代码内取值并选择 resourceManager 接口时；后续切片扩展已有取值写法时
  - 情境：源端在自绘 View 或代码里按当前资源配置取文案；目标需要在 ArkTS 中拿到纯字符串（Canvas 绘制、测宽、拼接），同一屏还有走声明式 $r 的组件文本；应用带多个 locale 资源目录，可能以应用偏好语言运行。
- [单个符号字形被当作图形用（如循环里按大字号生成 Html.fromHtml("&amp;#8226;") 作页码点）时，按源字体下的可见几何画图形](lesson-e1293913e4905dc3055c.lesson.md)
  - 时机：规格提取与界面实现阶段，转换用文字字形充当图形的控件（翻页圆点、指示点、分隔点等）时
  - 情境：源端在循环中逐个 new TextView、setText(Html.fromHtml("&amp;#8226;")) 或直接设 “•”“●”“★” 一类单字符，并用远大于正文的 setTextSize 作页码点等指示器；内容只有一个符号、无标签无链接；可见尺寸、步进与垂直位置取决于源字体（如 Roboto）的字形度量；规格或映射可能把“字符 + 字号”写成跨栈硬映射。
  - 例外：符号是正文的一部分（列表符号后接文字、行内分隔），随文字一起排版：按普通文本或富文本移植
- [单行 ellipsize=middle/start 用 ellipsisMode(CENTER/START)，与 Span 组合不满足时才测量截断](lesson-a184209501ba02cb62e7.lesson.md)
  - 时机：界面实现阶段，转换单行文本的省略位置（android:ellipsize="middle"/"start"、TextUtils.TruncateAt.MIDDLE/START）时
  - 情境：源 TextView 用 android:ellipsize="middle"（或 start）配合 lines=1、maxLines=1 或 singleLine 显示文件名等尾部有意义的文本，可能还有关键字 Span 高亮；映射参考只给 end → TextOverflow.Ellipsis 示例。
  - 例外：项目已批准以尾部省略作为平台差异
- [可折叠正文按 onTextLayout 溢出结果显示展开钮时，用文本测量比较限行与不限行高度，overflow 按默认 Clip](lesson-c61ac79c7db81729a544.lesson.md)
  - 时机：界面实现阶段，把 Compose 可折叠文本卡转换为 ArkUI 组件，确定是否显示展开按钮、折叠态 overflow 与文本加工时；占位复核阶段决定字符数近似是否保留时
  - 情境：源 Text 用 onTextLayout { didOverflowHeight / hasVisualOverflow } 决定是否显示展开钮，maxLines 在折叠与展开间切换且未设 overflow（Compose 默认 Clip），正文可能经 buildAnnotatedStringWithUrls 等加工，外层 toggleable/clickable 带按压反馈；ArkUI Text 没有同名排版回调，写者可能用字符数阈值近似。
- [可见文案改为资源引用时值取自源端原文：目标字符串表缺键就新建专属键并连同原值移交，补值者回查源布局，不用语义相近的现成资源或按键名自拟](lesson-4567f9f77f4280ec1747.lesson.md)
  - 时机：页面转换、切片实现与组收口阶段，源端文案在目标 string.json 中没有对应条目，或把页面字面量改成由他人单写的资源引用、由收口者补值时
  - 情境：源布局或源码给出页面专属文案（如空态“暂时没有常用的路线”、隐私弹窗“同意并继续/不同意”）或纯数字徽标序号（android:text="1"…"4"），目标字符串表没有对应键，共享资源文件由收口 agent 单写；工程里有语义相近的通用资源（“暂无数据”、他页“隐私政策”、“取消/确定”）可引用；交接可能只给键名不给值，显示容器可能是固定尺寸的小徽标。
  - 例外：纯数字等不需要翻译的序号可以保留字面量，不必新建资源
- [复用基类显示格式化 getter 前核对源端各字段的格式参数，精度不同就在子类覆写同一字段的全部分支](lesson-042445ba332611e04a80.lesson.md)
  - 时机：界面实现阶段，源端子类或调用处以不同于基类的小数位参数调用格式化函数（例：源端取值函数传 3 位小数、基类 getter 按 2 位格式化），目标准备复用基类 ViewModel 的显示 getter 时；修改同一显示字段的任一分支（静态值、无数据兜底、联动高亮值）时
  - 情境：多个详情页共用一个基类 ViewModel，基类显示 getter 用通用精度格式化；某一子类的静态字段与源端联动代码使用不同精度，子类尚未覆写对应 getter。
- [多行省略正文含拉丁单词时两端末行截断粒度可能不同：先试 wordBreak(BREAK_ALL)，仍不一致才测量截断](lesson-836a5414b52f0e062f1f.lesson.md)
  - 时机：规格提取阶段为带 maxLines(N) + TextOverflow.Ellipsis（或 android:ellipsize）的多行正文写转换决策，以及界面实现阶段落实折叠态末行时
  - 情境：源端多行正文以 maxLines + Ellipsis 折叠，正文含拉丁单词或长英文串；目标用 .maxLines() + .textOverflow({ overflow: TextOverflow.Ellipsis })，默认 wordBreak 为 BREAK_WORD；映射参考只记 ellipsize → textOverflow 的 API 对应；项目可能要求完整复刻源端可观察行为。
  - 例外：项目允许平台差异、不要求逐字复刻末行时，直接使用内置行为，不引入运行期测量；正文是纯 CJK 文本：按 enums.d.ts，ArkUI 默认可在任意两个 CJK 字符间换行，不会出现整词丢弃
- [字符串语言目录与键集按源端实际存在的 values-&lt;语言&gt; 镜像：不合成译文、不缩减语言、限定词粒度照源，源 locale 缺键回落 base](lesson-b58df29f032cc6a8c9d6.lesson.md)
  - 时机：规格提取与资源迁移阶段，确定要迁移哪些 values-* 语言目录及其目标限定词、目标生成哪些语言限定字符串目录及各键取值、源 locale 缺键如何处理时
  - 情境：Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。也包括源端有多个 values-xx（如 es/fr/it/pt/ru/zh/zh-rTW）并提供应用内语言切换，规格或主会话却自定“默认只迁 values + values-zh”，并以“项目决策优先”覆盖资源 skill 的“全部转换”硬规则；部分语言目录键集不全，skill 要求键集一致并自动补译。也包括源端只有仅语言限定的 values-zh，skill 正文写“values-zh-rCN 或 values-zh → zh_CN 或 zh”并要求最少生成 zh_CN，而详细映射表写 values-zh→zh、values-zh-rCN→zh_CN。
  - 例外：规格或任务明确要求本轮新增语言或补译时，按其要求生成；源端引用 android.R.string.* 等框架字符串：译文由系统按设备语言提供，见 lesson-ff19b09146b57d0f91a8
- [有效样式 textAllCaps 为 true 时按当前 locale 调 toLocaleUpperCase，不用只转 ASCII 的 textCase](lesson-cce58a1538fedfda3695.lesson.md)
  - 时机：界面实现或返修阶段，把安卓 textAllCaps（含按钮样式默认的全大写）移植为 ArkUI 文本，确定取字符串方式与 locale 标签，或给多个页面的按钮统一做大小写变换时
  - 情境：安卓按钮或文本的有效样式 textAllCaps=true（显式声明，或来自 AppCompat、MaterialComponents 与框架 Material 按钮默认样式），AllCapsTransformationMethod 按当前 locale 大写，资源串多为首字母大写（Yes/No、New Game）；应用带含非 ASCII 或非拉丁字母的多语言资源（de 的 ü、tr 的 i/İ、ru 的西里尔字母），也可能以只有语言码的应用偏好语言运行；目标按钮参数常是 Resource/ResourceStr，要自己取字符串做大写，并把 resourceManager 配置的 locale（下划线分隔、子标签可能为空，如 fa_Arab_）转成 BCP 47 标签。也包括工程里已有按 locale 大写的私有实现，其他页面又用 textCase 另写一套。
  - 例外：有效样式的 textAllCaps 为 false：源主题为 Theme.Material3.*（按钮文字样式 LabelLarge 不大写，material 1.12 values.xml 的 TextAppearance.M3.Sys.Typescale.LabelLarge 设 textAllCaps=false）或 Holo 主题按钮（android-36.1 styles_holo.xml 的按钮样式不设 textAllCaps）时默认不大写，先沿 style 链核 textAllCaps 的有效值
- [源文本经 AnnotatedString、Html.fromHtml 或带标记资源加工时，按富文本移植，样式、链接与点击一并落地](lesson-57a52be767730880cbba.lesson.md)
  - 时机：界面实现阶段，把源端 Compose Text、TextView 或对话框正文译成 ArkUI Text 时
  - 情境：源组件先调用工具函数（如按正则识别 URL、附加 LinkAnnotation 的函数）生成 AnnotatedString 再交给 Text；目标页面规格和验收条目只写了空值隐藏、折叠展开等布局行为。也包括 View 体系以 Html.fromHtml、setMessage(resId) 或 android:text 引用带 &lt;b&gt;/&lt;i&gt;/&lt;a&gt; 标记或 CDATA 的字符串资源，并用 LinkMovementMethod 让链接可点；目标准备用 Text($r(...)) 直接显示，或在正文外另起链接行。
  - 例外：Html.fromHtml 只产出单个符号实体（如 &amp;#8226;）、无标签无链接，在循环里按远大于正文的字号逐个生成作页码点等图形时，这是用字形画图形而不是富文本，按 lesson-e1293913e4905dc3055c 处理
- [源端在 Button 子类或带 style 的 TextView 上开启自动字号时，契约写出作用区（控件尺寸减内边距）与测量字体，不只抄字号区间](lesson-ba9454c2e0408bd1f228.lesson.md)
  - 时机：规格提取或界面实现阶段，把源端 setAutoSizeTextTypeUniformWithConfiguration 或 autoSizeTextType 的自动字号写成目标映射契约或 Text 自适应字号时
  - 情境：源端在继承 Button/AppCompatButton/MaterialButton 或带 style 的 TextView 上调用 setAutoSizeTextTypeUniformWithConfiguration（或布局写 autoSizeTextType），可能同时换了背景；规格行只写了字号区间与“在块内自适应”。
- [源端在代码里格式化的含固定措辞文案（SimpleDateFormat、String.format、拼接）也建参数化字符串资源并用 $r 传参，不写模板字符串](lesson-d442eb6e9aab4d77db18.lesson.md)
  - 时机：界面转换阶段，为源端在代码里动态生成的可见文案（日历年月标题、带单位的数量等）选择文本来源并登记字符串资源时
  - 情境：Android 源在 Kotlin/Java 里用 SimpleDateFormat、String.format 或拼接生成带中文单位或固定措辞的显示文本（如 yyyy年M月），不在 strings.xml 中；目标工程约定可见文案走 $r('app.string.*')，模块 string.json 已有 %s 参数化条目。
  - 例外：文本只由纯数字或数据值构成（如日期格子的 day.toString()）
- [源端对资源字符串做 toLowerCase 等加工时，目标用 getStringSync 取得 string 后照样加工，不以 Resource 限制删掉](lesson-b82514d933248d147e85.lesson.md)
  - 时机：界面与服务实现阶段，迁移源端 getString(R.string.x) 后接字符串加工（toLowerCase、拼接、格式化）的文案时；以“平台不支持”为由准备删掉加工时
  - 情境：源端先取资源串再做 toLowerCase 等加工后显示或拼接；目标里 $r('app.string.x') 得到的是 Resource 对象，不能直接调用字符串方法，代码内可经 resourceManager.getStringSync 取得 string。
- [源端引用 android.R.string.* 系统文案时按设备语言本地化落地：新建应用字符串就为工程已有的每个语言目录补框架译文，不只写 base 英文](lesson-ff19b09146b57d0f91a8.lesson.md)
  - 时机：页面实现阶段，为源端 stringResource(android.R.string.ok)、@android:string/cancel 一类系统字符串选择目标文案来源并新建应用字符串键时
  - 情境：源码或布局引用 android.R.string.ok、cancel 等框架字符串，它们不在应用 strings.xml 中，由系统按设备语言提供译文；目标工程已有多个语言限定目录（可能区分简繁）；转换者准备新增一个应用键（如 button_ok），只在 base 写英文值。
- [源端文字尺寸只乘文字缩放倍率、几何另乘画布比例时，字号与行距按源公式落成 vp，只让 bounds、padding 等几何乘画布比例](lesson-4c494b9f89c7e9db2b55.lesson.md)
  - 时机：实现按设计稿宽度缩放的预览、画布或动态布局渲染，统一缩放函数将同时作用于字号与几何时；为同一渲染新增测量或原生绘制路径时
  - 情境：源端动态文本字号由 dp 值乘文字倍率得到（例：fontSize.dpF × dynamicTextScale × fontSizeScale），行距同样按 dp；只有节点宽高、位置、padding、背景按根尺寸与设计宽度之比缩放；目标预览用画布比例（例：renderWidth / document.width）统一换算几何。
- [说明类静态页按源布局逐卡迁移：文案逐字取自源 XML，标题条背景与插图一并迁入](lesson-0197307e63e8d848ba02.lesson.md)
  - 时机：界面实现阶段，依据源布局 XML 生成规则、说明、注意事项一类静态图文页时
  - 情境：源静态页由多张卡片组成，标题条使用 drawable 背景，正文是写在布局 XML 里的长文案，卡内或页首尾有插图；规格只要求“展示说明并可返回”，不复述内容。
