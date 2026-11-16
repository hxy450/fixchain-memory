# 派工里的服务卡片规格（form_config）

agent 会看到什么：源 res/xml 的 appwidget-provider 写了 targetCellWidth / targetCellHeight、minResizeWidth、maxResizeWidth、resizeMode；台账或派工里的 supportDimensions、defaultDimension 是默认假设，没写出自源的哪一项，没有 resizable，已批的静态预览没带进派工

## 规矩

- rule-ed9295c371aa｜派工定 form_config 规格时按源 appwidget-provider 换算，写上 resizable 和预览｜读到：源 res/xml 的 appwidget-provider 写了 targetCellWidth / targetCellHeight、minResizeWidth、maxResizeWidth、resizeMode；写错：台账或派工里写默认假设的 supportDimensions（如 1*2/2*2/2*4）和 defaultDimension，没写出自源的哪一项；没有 resizable；台账已批的静态预览没带进派工
