# SlidingUpPanelLayout 上拉面板

agent 会看到什么：读到布局 XML 里 SlidingUpPanelLayout（带 umanoPanelHeight）包着历史 RecyclerView 和下拉指示图；产物里指示图是没有 .onClick 的装饰 Image，没有展开收起的 @State、历史 List 和 ListItem 的回填点击

## 规矩

- rule-d8e0e94cf646｜SlidingUpPanelLayout 包着历史列表时，目标实现展开收起和点击回填，指示图不当装饰｜读到：布局 XML 里 SlidingUpPanelLayout（带 umanoPanelHeight）包着历史 RecyclerView 和一个下拉指示图；写错：指示图只写成没有 .onClick 的 Image 当装饰，没有展开、收起的 @State 和历史 List，或 ListItem 没有回填的 .onClick
