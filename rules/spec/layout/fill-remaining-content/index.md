# 排在固定高度兄弟之后的填满内容区

agent 会看到什么：读到 Compose Column 里排在搜索栏、分隔线之后、用 fillMaxSize 或 LazyColumn 占满的内容区；规格把它写成「全屏」「全屏居中」

## 规矩

- rule-75e74e383392｜规格描述排在固定高度兄弟之后的内容区时，写「占其后的剩余高度」，不写「全屏」｜读到：Compose Column 里内容区排在搜索栏、分隔线之后，用 fillMaxSize 或 LazyColumn 占满；写错：规格把这个内容区（如无结果的居中提示）写成「全屏居中」「全屏 Column」
