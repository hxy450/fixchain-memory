# 移除已登记的页面或弹窗

agent 会看到什么：收口或返修回执写「已移除」「Removed …」某个页面或弹窗文件；ui-manifest 仍记为 verified，feature-index、ui-plan、placeholder-registry 和迁移报告没同步，也没引台账决策

## 规矩

- rule-e64e4b033f5b｜确需退役已登记页面时，先取台账决策，并在同一改动里同步各清单和迁移报告｜读到：收口或返修回执写「已移除」「Removed …」某个页面或弹窗文件；写错：ui-manifest 仍记为 verified，feature-index、ui-plan、placeholder-registry 和迁移报告都没同步，也没有引用台账决策；主线程直接标记完成，迁移报告写「已移除」
