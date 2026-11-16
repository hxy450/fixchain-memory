# Web Swiper 组件的分页点和导航箭头

agent 会看到什么：读到源端（Web）的 Swiper 组件带 pagination、navigation，只 import 'swiper/css/…' 默认样式、没有 --swiper-theme-color 或样式覆盖；产物里自建分页点和导航箭头的形状、颜色（是否用了应用 accent 和令牌）、叠放位置和箭头素材

## 规矩

- rule-587df277b2ae｜源组件只引入 Swiper 默认 CSS 时，自建箭头和分页点按库默认样式写，不用应用令牌｜读到：源组件 import 'swiper/css/navigation'、'swiper/css/pagination'，<Swiper navigation pagination={{ clickable: true }}> 上没有主题变量或样式覆盖；写错：自建的导航按钮加了源端没有的底色 backgroundColor、圆角 pill、.shadow(...)，或颜色、尺寸取的是应用自己的 accent、卡片底色、阴影令牌
- rule-9065c095d883｜源端 color 只绑在部分元素上时，只给这些元素用 accent，库控件留库默认主题色｜读到：源组件的 color={...} 只出现在部分 IonButton 上，Swiper 本身没有 color 属性或主题变量；写错：目标端把应用 accent 用在导航箭头或分页激活点上（fillColor(...)、backgroundColor(...) 传的是 accent），或注释把 accent 写成导航前景色
- rule-084e3ec890ed｜Swiper 默认分页点迁移时写成同径圆点只变颜色，不自造胶囊激活态｜读到：源端 Swiper 用 pagination（如 pagination={{ clickable: true }}），只引入 swiper/css/pagination 默认样式；写错：目标端激活点的 .width(...) 大于 .height(...)（胶囊形），非激活点的 backgroundColor 取了应用令牌，或分页点放在轮播下方的列流里而不是叠在轮播底部
- rule-3dec23cc4041｜源 Swiper 带 pagination 时，分页点叠在轮播容器内底部，不做成容器外单独一行｜读到：源 Swiper 启用 pagination（如 pagination={{ clickable: true }}）；写错：目标分页点是 Stack / Swiper 外面单独的一行 Row，或整个 Stack 改成 alignContent: Alignment.Bottom
- rule-b6543ab4ef5d｜缺合规 chevron 符号而改选图标时，新增线性 chevron 素材，不借用圆形箭头｜读到：源端导航是 Swiper navigation 的默认 chevron 箭头，没有自定义图标；写错：目标端导航按钮的 Image($r(...)) 引的是带圆圈的箭头素材，或注释写明因符号名未验证、为规避风险改选了已有素材
