# 收尾闸报全屏页缺 Layer 3 时，grep 到宿主实际避让才可标沉浸豁免 false

审的是：代码
触发（任一种）：
- 读到：沉浸检查结果报某全屏页未发现任何安全区响应，修复方式为 windowTopPadding，仅确无前景避让需求才可标 false；写错的样子：页头加了 needs_immersive_safearea=false 豁免注释（理由如「原生标题栏自动避让」「壳层统一处理」），而本页和宿主都没有 windowTopPadding
适用范围：收尾阶段处理沉浸检查器报出的 Layer 3 缺失
做法：
- 只有 grep 到宿主确实给本页加了 .padding({ top: windowTopPadding })，或真机确认无遮挡，才标 needs_immersive_safearea=false；否则删掉豁免注释，在本页顶栏补避让
来源：1 张卡，1 个应用
- case-b3c176b95cabcc03a434（jerboa）：做法第 1 步 ← 建议 4
