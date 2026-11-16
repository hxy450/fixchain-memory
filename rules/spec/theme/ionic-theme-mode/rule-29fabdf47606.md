# 源主题有 body.dark 覆盖块时，规格的设计令牌要列页面中性色的浅/深两值

审的是：规格
触发（任一种）：
- 读到：源主题 CSS 里有 body.dark / .ios body.dark / .md body.dark 覆盖块，给 --ion-background-color、--ion-text-color、--ion-card-background、--ion-item-background 等页面级变量深色值；写错的样子：规格的设计令牌段只有 accent 色的浅/深对照，没有页面背景、正文、卡片、列表项、分隔线、遮罩的深色值，却写「全量」「浅/深两套色值齐全」
适用范围：源端用主题 CSS 变量提供页面级中性色、目标靠 dark 资源限定符切换深浅时，规格里写设计令牌的那一节
做法：
- 完整读主题文件（含后半部分的深色覆盖块），页面级中性令牌（背景、正文、卡片、列表项、分隔线、遮罩）和 accent 一样各列浅值和深值
- 只列了 accent 时如实写「只含 accent」，不写「全量」「浅/深两套齐全」
针对本应用要查的：
- 页面级中性色的深色值：源工程主题 CSS 文件（定义 --ion-* 变量的那个）里 body.dark、.ios body.dark、.md body.dark 等选择器下的 --ion-* 变量；按平台模式分别读出各变量的深色值，和浅色块里同名变量配对
来源：1 张卡，1 个应用
- case-4b094d53d106bc8446de（Countdate）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
