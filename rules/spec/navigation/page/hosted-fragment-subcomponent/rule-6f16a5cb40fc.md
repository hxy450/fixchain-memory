# 子组件规格被标为不需沉浸时，宿主规格逐个 Tab 登记是否用全屏背景

审的是：规格
触发（任一种）：
- 读到：子页面元数据 page_type=sub_component，自动标 needs_immersive_safearea=false；宿主元数据 page_type=full_screen_page、needs_immersive_safearea=true；写错的样子：宿主规格里没有逐个 Tab 登记内容是否用全屏背景、是否延伸到状态栏，也没写由宿主还是子组件负责避让
适用范围：Tab 宿主承载多个子组件页、子组件规格按 page_type 自动跳过沉浸处理的情形
做法：
- 在宿主规格里加一张逐个 Tab 的登记：是否全屏背景延伸到状态栏、状态栏文字颜色、顶部避让由宿主还是该 Tab 实现
来源：1 张卡，1 个应用
- case-06c7df8f8d85e13580ac（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 4
