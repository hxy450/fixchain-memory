# Ionic 应用的主题变量和全局 mode

agent 会看到什么：读到 Ionic 源端的主题 CSS 里有 body.dark 覆盖块给 --ion-background-color 等页面级变量深色值，或 App.tsx 里 setupIonicReact({ mode: 'ios' }) 固定模式、页面用 IonCard、IonToolbar 而 tsx 只有少量 inline style；规格的设计令牌只列 accent 的浅深两值，或只按 DOM 顺序和 inline 字号写组件

## 规矩

- rule-54c620e38342｜Ionic 应用设了全局 mode 时，规格写入各组件该 mode 的 host 样式，不只列 inline｜读到：源 App.tsx 里 setupIonicReact({ mode: 'ios' }) 固定了模式；页面用 IonCard、IonCardHeader（IonCardSubtitle + IonCardTitle）、IonToolbar + IonButtons，tsx 里只有少量 inline style（如 fontSize）；写错：规格只按 DOM 顺序和 inline 字号写组件（如「副标题 1.2rem + 主标题 2.8rem」），把 IonCard 决策成「Column 卡片（borderRadius + padding）」，没写渲染顺序、大写、字重、字距、阴影、工具栏内距；样式来源只列应用自己的 css
- rule-29fabdf47606｜源主题有 body.dark 覆盖块时，规格的设计令牌要列页面中性色的浅/深两值｜读到：源主题 CSS 里有 body.dark / .ios body.dark / .md body.dark 覆盖块，给 --ion-background-color、--ion-text-color、--ion-card-background、--ion-item-background 等页面级变量深色值；写错：规格的设计令牌段只有 accent 色的浅/深对照，没有页面背景、正文、卡片、列表项、分隔线、遮罩的深色值，却写「全量」「浅/深两套色值齐全」
