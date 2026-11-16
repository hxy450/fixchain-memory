# Compose PullToRefreshBox 下拉刷新

agent 会看到什么：读到 Compose 源端用 PullToRefreshBox(isRefreshing, onRefresh)，默认 M3 指示器，包住的范围可能是加载条和 TabRow + Pager 整体；规格的转换决策写「PullToRefreshBox → Refresh { List }」「官方下拉刷新 / 标准映射」，或让每个 Tab 各放一个 Refresh

## 规矩

- rule-e38c8c9fc903｜规格映射 PullToRefreshBox 时，写明 M3 指示器外观和内容不随下拉移动｜读到：源端 `PullToRefreshBox(isRefreshing, onRefresh)` 用默认 M3 指示器；写错：转换决策表只写「PullToRefreshBox → Refresh { List } / 官方下拉刷新 / 标准映射」，没写指示器外观，也没写内容不随下拉移动
- rule-6f0c60f9939f｜PullToRefreshBox 包住整个 Tab 区时，规格照原范围映射，不拆成每个 Tab 一个 Refresh｜读到：源端一个 `PullToRefreshBox` 包住加载条和 `TabRow` + Pager 整体；写错：转换决策表写「PullToRefreshBox → Refresh 包裹 List」，或者规格让每个 Tab 各放一个 Refresh
