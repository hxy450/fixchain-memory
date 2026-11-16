# 源布局是带标题条背景和插图的图文卡时，目标页逐卡迁入标题条和插图、卡数一致

审的是：代码
触发（任一种）：
- 读到：静态说明页的布局 XML 由多张圆角卡组成：标题 TextView 带 android:background="@drawable/…" 的标题条，卡内或页首尾有 ImageView 的 android:src="@drawable/…" 插图；写错的样子：目标页只用 Text 拼成纯文字卡：没有 Image($r('app.media.…'))，标题只是普通粗体 Text、没有标题条背景，或者卡片数比源布局少
适用范围：依据安卓布局 XML 实现静态说明页、图文页（多张卡片、标题条背景、插图、写死的正文）时
做法：
- 先按每个源布局列出卡片数和每张卡的标题、正文、标题条背景 drawable、插图 drawable；目标页写同样数量、同样次序的卡
- 插图写成 Image($r('app.media.<插图名>'))，放在源布局里同样的位置；标题条照源 drawable 做成标题 Text 的背景（如 .backgroundImage($r('app.media.<标题条名>'))），不换成普通粗体文字
- 写完逐卡对照源布局：卡片数一致，每张插图和标题条背景都被页面引用到
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (src: PixelMap | ResourceStr | DrawableDescriptor | ImageContent): ImageAttribute：Image 组件的构造，src 传 $r('app.media.<名>') 这类资源引用（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageInterface）
- backgroundImage(src: ResourceStr | PixelMap, options?: BackgroundImageOptions): T：组件背景图（@since 18 的写法）；@since 12 的写法是 backgroundImage(src: ResourceStr | PixelMap, repeat?: ImageRepeat): T（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundImage）
- $r('app.media.<名>')：访问本模块 resources 下 media 资源的写法（出处：resource-categories-and-access.md，资源访问）
未核实：卡里没写修好时标题条在目标端用的是哪个接口；backgroundImage 是按声明给出的写法
来源：1 张卡，1 个应用
- case-f663597a71756594de10（骑行记录）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2
