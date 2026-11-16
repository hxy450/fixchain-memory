# 源组件只引入 Swiper 默认 CSS 时，自建箭头和分页点按库默认样式写，不用应用令牌

审的是：代码
触发（任一种）：
- 读到：源组件 import 'swiper/css/navigation'、'swiper/css/pagination'，<Swiper navigation pagination={{ clickable: true }}> 上没有主题变量或样式覆盖；写错的样子：自建的导航按钮加了源端没有的底色 backgroundColor、圆角 pill、.shadow(...)，或颜色、尺寸取的是应用自己的 accent、卡片底色、阴影令牌
适用范围：源端（Web）组件用第三方 UI 库控件且只引入它的默认 CSS，目标端用 ArkUI 自建替代控件时
做法：
- 按源工程锁定的库版本（package.json 和 node_modules 里对应的 CSS）读出默认的颜色、尺寸、形状和定位，写成目标端的显式值
- 不用应用的 accent、卡片底色或阴影令牌代替：源端是透明底的箭头，目标端就不加底板、圆角和 .shadow(...)
针对本应用要查的：
- 库默认的主题色和导航箭头的形状、尺寸、底色：源工程 package.json（或锁文件）里该库的版本，再到 node_modules 里同版本库的 CSS（Swiper 是主 CSS 和 navigation、pagination 两份 CSS），按 --swiper-theme-color 等 CSS 变量和箭头的规则找；读出变量默认值和箭头的宽高、背景，写成目标端的颜色值和尺寸；例：swiper 12.2.0 下 --swiper-theme-color 是 #007aff，导航是 44px、透明底的 chevron
未核实：卡里 swiper 12.2.0 默认箭头是 44px，修复最后把 chevron 写成 64vp，两者怎么对应卡里没写清
来源：1 张卡，1 个应用
- case-da00df033b66793baed0（Countdate）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
