# Swiper 默认分页点迁移时写成同径圆点只变颜色，不自造胶囊激活态

审的是：代码
触发（任一种）：
- 读到：源端 Swiper 用 pagination（如 pagination={{ clickable: true }}），只引入 swiper/css/pagination 默认样式；写错的样子：目标端激活点的 .width(...) 大于 .height(...)（胶囊形），非激活点的 backgroundColor 取了应用令牌，或分页点放在轮播下方的列流里而不是叠在轮播底部
适用范围：源端用 Swiper 默认分页点，目标端自建可点圆点时
做法：
- 激活和非激活都写成同一直径的圆点（width 等于 height，borderRadius 取一半），只换颜色
- 分页点叠在轮播底部，不占轮播下方的列流；直径、间距、颜色和距底偏移按库默认 CSS 取
针对本应用要查的：
- 分页点的直径、间距、激活与非激活颜色、距底偏移：源工程锁定版本的 swiper 包里 pagination 的 CSS，按分页点的 CSS 变量和规则找；读出各值写成目标端圆点的宽高、间距、颜色和偏移；例：卡里按 swiper 12.2.0 修好后是 8×8 圆点、激活 #007aff、非激活 rgba(0,0,0,0.2)、间距 8、距轮播底部 8
来源：1 张卡，1 个应用
- case-da00df033b66793baed0（Countdate）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 诊断
