# 布局 XML 上的外边距、内边距和尺寸

agent 会看到什么：读到布局 XML 元素（含容器自身）上的 android:layout_margin*、android:padding*、match_parent 加 margin、带 padding 的 ImageView、锚在兄弟控件上方的 marginBottom；产物里对应组件修饰链上的 .margin / .padding / .width / .height 漏写、数值不同、叠成两份或没扣边距

## 通用查法

### 布局 XML 元素带 margin / padding 时，逐个元素读出各边值写进对应组件的修饰链

审的是：代码
触发（任一种）：
- 读到：源布局 XML 的元素（含 FrameLayout、LinearLayout 等容器自身）写了 android:layout_margin*、android:layout_marginVertical、android:padding*；写错的样子：对应组件的修饰链里没有 .margin(...) / .padding(...)，或数值和 XML 不同
适用范围：按源布局 XML 转写页面、弹窗或列表项时，核对每个元素的外边距和内边距
做法：
- 在源布局 XML 里列出所有带 layout_margin* / padding* 的元素（叶子和容器都算），各边按 layout_margin 优先于 layout_marginVertical / Horizontal、它们又优先于单边值的次序读出
- 逐个在目标里找到对应组件写 .margin({ top: NN, … }) / .padding(...)，dp 数值照搬成 vp 数值，不自行折算或省略
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- layout_marginVertical 等同于 layout_marginTop 和 layout_marginBottom 取同一值；与它们同时写时 layout_marginVertical 优先，layout_margin 又优先于它：源端几个边距属性的取值次序（出处：Android SDK 平台资源 data/res/values/attrs.xml，ViewGroup_MarginLayout 的 layout_marginVertical（按应用的 compileSdk 取对应平台））
- margin(value: Margin | Length | LocalizedMargin): T，默认值 0：组件外边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.margin）
- padding(value: Padding | Length | LocalizedPadding): T：组件内边距，同样按边给值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- Margin = Padding = { top?: Length; right?: Length; bottom?: Length; left?: Length }：按边分别给值（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Padding / Margin）
- Length 为 number 时默认单位 vp：源端 dp 数值照搬（出处：ts-types.md，Length）
- width 和 height 设百分比时以父容器的 width 和 height 为基础值：百分比尺寸不扣除自己的 margin（出处：ts-universal-attributes-size.md，width / height 示例）
针对本应用要查的：
- 每个元素各边的外边距和内边距：源工程布局 XML 里这个元素的 android:layout_margin*、android:padding* 属性；写成 @dimen/… 引用的，到 res/values 下的 dimens 资源里按资源名找；按上面的优先次序取出各边的 dp 数值，照搬成 vp 写进对应的边
未核实：@dimen 引用在有 values-swNNNdp 等限定目录时取哪一份，族里规矩没查实
来源：2 张卡，2 个应用
- case-89e7732b8a374944c6b2（免费来电多多）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-bd76c218ac0773e443e3（android-train-ticket-vest7）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2

## 规矩

- rule-db53829e91dd｜源容器自身的 layout_margin，写在对应 Stack/Row/Column 的 .margin 上，不能漏｜读到：源 XML 的非叶子容器（如 FrameLayout）上写了 android:layout_marginTop 等外边距；写错：对应的 Stack / Row / Column 没写 .margin({ top: … })，只写了它子控件的边距
- rule-1cce83a254b1｜注释里记了尺寸和边距而修饰链没有应用时，按缺失补上｜写错：代码注释写着 mS16、mB20 这类边距或尺寸，对应组件的修饰链里没有 .margin(...) / .padding(...) / .width(...) 等对应调用
- rule-2c52e6cb971d｜重复 XML 元素抽成 @Builder 时，逐实例不同的 layout_marginTop 等作为参数传入｜读到：源布局 XML 里几个同类元素（如分组标题 TextView）各自写了不同的 android:layout_marginTop，按钮写了 android:layout_marginTop，装饰图写了 android:layout_marginVertical；写错：目标端把它们抽成没有边距参数的 @Builder，各实例都没有或都是同一个上间距；或按钮写成和 XML 不同的 .margin({ top: ... }) 数值
- rule-d04b90669108｜match_parent 加 layout_margin 不写成 100% 加 margin，尺寸要扣掉边距｜读到：容器或按钮 android:layout_width / layout_height="match_parent"，同时带 android:layout_marginHorizontal / layout_margin；写错：目标写成 .width('100%') / .height('100%') 再加 .margin(…)，居中后外边距对称溢出，真机上贴边、行间无留白
- rule-952fa2644a2a｜带 padding 的 ImageView 背景改纯色形状时，宽高取减去 padding 后的可见尺寸｜读到：ImageView 的 layout_width / layout_height 加 android:padding，背景是圆形 drawable，外面还有 android:layout_margin；写错：目标按 layout 尺寸画纯色圆（.width / .height / .borderRadius 按原尺寸），丢了 padding，可见圆垫偏大
- rule-bdbdd6243823｜宿主容器和共享组件根都写了同一来源的 padding 时，删掉宿主一侧｜读到：安卓宿主布局（承载 fragment 的 ViewPager）没有 padding，padding 写在 fragment 根 LinearLayout 上；写错：宿主的 TabContent 或容器 .padding(...) 和共享组件根 .padding(...) 取的是同一个边距资源，四边内边距叠成两份
- rule-8ac38daeb8b8｜锚在兄弟行上方的控件转 Stack 时，底距写兄弟行高加 padding 加自身 margin｜读到：TextView 带 app:layout_constraintBottom_toTopOf="@+id/…"（指向按钮行等兄弟控件）和 android:layout_marginBottom、android:layout_marginStart；写错：转成全高 Stack({ alignContent: Alignment.BottomStart }) 贴父容器底部，没有兄弟行的高度偏移，也没应用 marginStart / marginBottom；文字压在按钮上
- rule-a9ed457c9754｜marginEnd 转 margin 时各边用 LengthMetrics，或改 left/right｜读到：源布局写了 android:layout_marginEnd / layout_marginStart（映射参考示例写 .margin({ end: 10 })）；写错：.margin({ bottom: 16, end: 16 }) 这类对象里 start / end 和数字混用，编译报 number 不能赋给 LengthMetrics
- rule-616b62a16a9a｜item 和 Fragment 布局给了固定 dp 时，尺寸、颜色、圆角逐项照抄，不近似、不加分隔线｜读到：item 或 Fragment 布局 XML 给出固定尺寸：`android:layout_width` / `layout_height`、`android:minWidth`、`android:padding*`、圆角 shape 背景；写错：目标用近似值（如固定 `height(…)` 代替内容加上下 padding、圆角写成别的值），或多加了 XML 里没有的 `Divider`、列表左右 padding
- rule-e3a899b0962a｜注释写 minWidth/maxWidth 的元素代码却是 .width(N) 时，改成 constraintSize｜读到：规格或映射里写着该元素的 minWidth / maxWidth（源端是 android:minWidth、android:maxWidth 这类下限上限）；写错：代码注释写着 minWidth / maxWidth，同一个元素上却是 .width(N)，没有 .constraintSize(...)
- rule-afee259e0150｜配置驱动列表的各项不套统一间距，上下间距取源 Fragment 根布局｜读到：源端各 Fragment 按顺序加进同一个无间距容器，每项的间距写在各自根布局的 android:padding* / android:layout_margin* 上，外壳容器有一次四边间距；写错：目标给列表每一项统一套 .padding({ top: 10, bottom: 10 }) 一类对称间距，或没读源布局就自填间距值
