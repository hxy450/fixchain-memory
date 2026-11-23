# 源为 Ionic/Web 组件库时，先取组件 mode 样式与库默认 CSS，再合并应用 css 与 inline style；库控件不套应用 accent

## 何时使用

规格提取与界面实现阶段，把 Ionic 卡片、卡片头、工具栏、按钮等组件，或第三方 Web UI 库控件（如 Swiper 的 navigation/pagination）自建为 ArkUI 控件，确定渲染顺序、颜色、形状、尺寸与位置时

## 适用情境

源为 Ionic React/Angular 或其他 Web 应用：以 setupIonicReact({mode:'ios'}) 一类配置固定组件模式，tsx 只写少量 inline style，其余视觉由 node_modules/@ionic/core 中各组件 <组件>.<mode>.css 的 :host 规则决定；或组件只引入第三方库默认 CSS（swiper/css/navigation、swiper/css/pagination），没有主题变量覆盖；组件的 color 属性只绑定在部分子元素上。目标用 Column/Text/Image 手写对等结构。

## 例外与边界

- 源工程用应用 css 或 CSS 变量显式覆盖了对应属性时，按覆盖后的值取
- 读哪一套 <组件>.<mode>.css 取决于源端实际生效的 mode：本条的来源是用 setupIonicReact({mode:'ios'}) 一类配置固定了 mode；源工程没有固定 mode 时，先确认源应用在它运行的平台上实际用的是哪个 mode，再取那个 mode 的样式，不默认读 ios。
- 把 CSS 的 letter-spacing（px）写成 Text 的 letterSpacing 时，传纯数字会按 fp 解释、随系统字体大小变化，CSS 的 px 不随它变；要保持源端的固定字距，写成带 vp 单位的字符串。

## 原因

Web 组件的外观大多来自组件库按模式注入的 host 样式或库默认 CSS，tsx 里看不到；只转写 DOM 顺序与 inline 字号会漏掉渲染顺序（Ionic iOS 的 card-header 为 flex-direction: column-reverse，标题在副标题之上）、text-transform、字重、字距、阴影与内边距。自建库控件时套用应用 accent、卡片底色或阴影令牌，或为避开图标符号风险借用形态不同的素材，颜色与形状就偏离源端。

## 做法

1. 规格提取时，对页面用到的每种组件读取源工程锁定版本的 CSS：Ionic 读 node_modules/@ionic/core/dist/collection/components/<组件>/<组件>.<mode>.css 的 :host 规则，第三方库读其默认 CSS 与 CSS 变量（如 Swiper 的 --swiper-theme-color、--swiper-navigation-size、pagination bullet 尺寸与 bottom 偏移）；把渲染顺序、text-transform、font-weight、letter-spacing、阴影、圆角、内边距与默认色写进规格。
2. 实现时按“组件 mode host 样式或库默认 → 应用 css → inline style”三层合并出最终样式再写 ArkUI，inline style 只覆盖它声明的属性；容器 flex-direction 为 *-reverse 时按渲染序而非 DOM 序排列子组件，并在注释写出所依据的 CSS 规则。
3. 逐个核对源中 color/accent 属性实际绑定到哪些元素，只给这些元素用应用主题色；库控件保留库默认色（例：swiper 12.2.0 的 --swiper-theme-color 为 #007aff）。
4. 因符号校验或素材可用性改选图标时只换实现手段、不换视觉形态：缺合规的线性 chevron 就新增与源一致的素材，不借用语义相近的圆形箭头；分页点按库默认的同径圆点只变颜色，不自造胶囊激活态。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、2 步〕Text 的 textCase 应用没有另设时为 TextCase.Normal；TextCase.UpperCase 把文本全部显示为大写（对应 text-transform: uppercase）
- 〔做法第 1、2 步〕FontWeight.Bold 等同数值 700（对应 font-weight: 700）
- 〔做法第 1、2 步〕Text 的 letterSpacing 传 number 时单位是 fp（随系统字体大小变化，CSS 的 px 不随它变），应用没有另设时为 0；取负值时文字被压缩
- 〔原因 / 做法第 2 步〕Ionic 的 iOS 模式下 card-header 的 flex-direction 是 column-reverse：DOM 里写在后面的 IonCardTitle 显示在 IonCardSubtitle 上方（卡里没记 @ionic/core 版本）
- 〔做法第 1 步〕Ionic 的 iOS 模式下 card-subtitle 默认 uppercase、font-weight 700、letter-spacing 0.4px，card-title 默认 font-weight 700（卡里没记 @ionic/core 版本）
- 〔做法第 1 步〕Ionic 的 iOS 模式下 ion-card 默认圆角 8px、阴影 0 4px 16px rgba(0,0,0,.12)（卡里没记 @ionic/core 版本）
