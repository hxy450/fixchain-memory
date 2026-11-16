# 加载、失败、空态和不可用等页面状态

agent 会看到什么：读到规格、UiState 或决策台账分出 loading、failed、空态、定位不可用、Result 联合；交回的 ViewModel 只有 isLoading / items，页面用 items.length === 0 出空态，或数据层失败时 return []

## 规矩

- rule-96ffa0e6d7cc｜页面规格列了加载、失败、空态和问候语时，ViewModel 和页面要逐项有落点｜读到：页面规格写了问候语按时间段显示、loading / failed（含重试）/ 空态（含创建按钮）面板，UiState 含 loading、failed 字段；写错：ViewModel 只有数据字段和 loadData / refresh，没有 isLoading、isFailed；页面没有加载、失败面板和重试按钮，空态只有文字没有创建按钮，标题固定不随时间问候
- rule-9c0d4afcc3dc｜附近列表的 ViewModel 状态要分出定位不可用、失败、真空数据和有内容，空态文案只绑真空数据｜写错：ViewModel 对外只有 `isLoading` / `errorMessage` / `items` 几个字段，没有定位不可用的状态；页面用 `items.length === 0` 出「附近无内容」的空态
- rule-dde6d9cebc72｜数据层的 return [] 只代表有效查询成功返回空，坐标未知、未授权、定位失败用 Result 联合单独返回｜读到：规格或决策台账写着「失败保持显式错误与最近成功数据、不伪造空成功」、选定显式 `Result` 联合类型，或要求未知坐标标 `known=false`、定位拒绝与失败分为不同分支；写错：数据层在坐标未知、未授权或定位失败时 `return []`，调用方把它当作成功的空列表
