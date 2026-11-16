# 交付报告里的交互和入口

agent 会看到什么：交付报告、转换报告里的「已实现交互」、按决策留成占位的入口、跳板 Activity（onCreate 里 startActivity 再 finish）的写法

## 规矩

- rule-861d17f8dc4f｜交付报告的「已实现交互」按源端调用逐条列，不只写概括｜读到：源文件里有多处 setOnClickListener、currentItem 等交互调用；写错：交付报告的「已实现交互」只写「tab 切换 + Swiper 横滑联动」这类概括，没按源端行号和调用逐条列出对应的目标实现
- rule-6830457939e2｜入口按决策留成占位时，交付总结逐项列出未实现的入口，不报「占位符 0、可交付」｜读到：决策或巡检单把某些入口标为范围外，要求「保留路由合同或明确不可用反馈」；写错：代码里这些入口是「暂不可用」Toast、无响应或合规链接 kind 兜底，交付报告却写「TODO/占位符/FWD-REF 0、可交付」，没列出这些入口
- rule-01c3861e0a45｜跳板 Activity 的转换报告写明各分支实际目标、要求调用方直达，改成点击后跳转须标为行为改变｜读到：源 Activity 的 onCreate 或 initView 开头无条件 startActivity 到别的页并 finish()；写错：转换报告把它写成可见页、点击后才 replacePathByName，并用「对应 Android 启动后 finish」之类的说法带过；或报告里没写实际目标页，也没要求调用方直接路由过去
- rule-2c060cedd4ad｜偏离规格指定的组件映射时，转换报告逐项写交互差异，不写「行为等价」｜读到：规格或 render 契约指定了组件映射（如 stickyHeader → ListItemGroup StickyStyle.Header）；写错：转换报告或回执写「行为等价」「等价实现」，而代码换了规格指定的结构（如把吸顶内容移到 List 外）；没逐项写拖动起点、点击命中、测量口径的差异
