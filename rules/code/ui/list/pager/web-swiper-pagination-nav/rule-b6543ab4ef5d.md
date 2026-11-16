# 缺合规 chevron 符号而改选图标时，新增线性 chevron 素材，不借用圆形箭头

审的是：代码
触发（任一种）：
- 读到：源端导航是 Swiper navigation 的默认 chevron 箭头，没有自定义图标；写错的样子：目标端导航按钮的 Image($r(...)) 引的是带圆圈的箭头素材，或注释写明因符号名未验证、为规避风险改选了已有素材
适用范围：因符号名校验或素材可用性要替换源端图标时
做法：
- 只换实现手段、不换视觉形态：没有合规的 chevron 符号就在 resources/base/media 新增与源一致的线性 chevron SVG（描边色取库默认主题色），用 Image($r('app.media.…')) 引用
来源：1 张卡，1 个应用
- case-da00df033b66793baed0（Countdate）：做法第 1 步 ← 建议 3、诊断
