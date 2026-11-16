# 列表 Adapter 的 item 布局和绑定时的改写

agent 会看到什么：源端列表 Adapter 有多个 viewType、在 onBindViewHolder / afterBindViewHolder 里改写行视图（setVisibility、改配按钮外观）或运行时 inflate 别的布局，页面清单、转换报告或占位登记只顾到了共享行组件的默认样子

## 规矩

- rule-e9e0b2087218｜列表页的源布局清单要列全各类 item 布局和动态 inflate 的布局｜读到：列表页源码的 Adapter 有多个 viewType，holder 运行时 inflate 或 addView 别的布局；写错：页面 meta.json 的 layout_sources 只列了部分类型（如推广项）的布局，recycler_item_layouts 为空，没交付普通项 item 布局和它动态 inflate 的预览布局
- rule-31973d69b937｜当场补不齐的源端行为登记成占位，不只在转换报告里写「保真缺口」｜读到：源端有明确行为（如宿主绑定时改写行内视图），目标共享组件缺对应入参；写错：转换报告里写「已知保真缺口（非占位）」，占位登记里没有这一项，也没人接手
- rule-d95dbd3bed0b｜共享组件缺覆盖参数、本任务又不能改它时，登记跨文件交接，不把占位记为已闭合｜读到：源端子类 adapter 改配了按钮外观，共享行组件不在本任务的写盘范围内；写错：占位登记把 P-S… 记为已闭合，没有登记给共享组件作者的交接项，按钮外观仍是默认
