# 整页 ScrollView 内的 wrap_content WebView 转 ArkWeb：分别实现“高度跟随文档”和“Web 自身不滚”，锁 H5 滚动并对后加载内容复测

## 何时使用

界面实现或对齐修复阶段，把整页滚动容器内的 wrap_content WebView 转换为 ArkWeb，确定 Web 高度与滚动归属时

## 适用情境

安卓 WebView layout_height=wrap_content，位于整页 ScrollView 内，加载含图片等后续资源的远程 H5；目标用 Scroll 包裹 Web，要求滚动全部交给外层页面。

## 例外与边界

- Web 已设 layoutMode(WebLayoutMode.FIT_CONTENT)（API 11 起，Web 高度按前端页面高度自适应）时，“高度跟随文档”这一半由平台完成，不要再叠加 onPageEnd 测高或改回手动设高（这种模式下改高度属性也不起作用）；“Web 自身不滚”仍按做法第 1 步确认。用这种模式时注意它的限制：创建后不能切换模式，宽或高超过 7680px 要在创建时指定 RenderMode.SYNC_RENDER，否则白屏；不支持下拉到底部加载更多的网页。

## 原因

wrap_content 同时意味着高度等于内容、Web 不消费滚动。nestedScroll(PARENT_FIRST) 只决定父子滚动的先后，外层滚到边界后 Web 仍可内滚；onPageEnd 只触发一次，图片等后加载内容撑高文档后不会再测，固定高度或单次测高都会留下 Web 内部滚动区。来源中修复者读到了源布局并自述“自身永不内滚”，首轮只在 onPageEnd 测一次高并设 PARENT_FIRST，注释称会多次触发；用户随后报告资讯区单独滑动、有滚动条，第二轮加锁滚动与多次复测才解决（竞态时序为修复者推断）。

## 做法

1. 把两条约束分别实现：高度取文档高度并随内容变化更新；同时在 H5 侧锁定滚动（如注入脚本给 html/body 设 overflow:hidden）或用其他方式关闭 Web 自身滚动。nestedScroll(PARENT_FIRST) 不能代替不自滚。
2. 用 onPageEnd + scrollHeight 测高时，为后加载内容安排复测（如 0/1000/2500ms 取最大值）或持续跟踪；写“多次自适应”一类注释前先核对事件语义。

## 可选检查

- 真机把手指放在页底 Web 区域上下滑动，并在冷启动或图片晚到时检查 Web 是否单独位移、出现滚动条；某次加载恰好测准不能证明已等价于 wrap_content。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕onPageEnd 在网页加载结束时触发，只对主框架触发、不对子框架触发
- 〔原因 / 做法第 1 步〕NestedScrollMode.PARENT_FIRST 只规定父滚动组件优先响应滚动
- 〔做法第 1 步〕Web 的 nestedScroll 没设置时，各方向（scrollForward / scrollBackward 或上下左右四向）默认都是 NestedScrollMode.SELF_FIRST
- 〔做法第 1 步〕设备上：外层 Scroll 包裹的 Web 中，注入脚本给 html、body 设 overflow:hidden 时，手指在页底 Web 区域滑动带动外层整页，Web 自身没有单独位移
