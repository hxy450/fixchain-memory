# onClick 回调的事件参数

agent 会看到什么：读到映射参考或别处回调里的 event.stopPropagation()；产物里 .onClick((event: ClickEvent) => …) 调了 stopPropagation

## 规矩

- rule-5c84d35b8dc8｜onClick 的 ClickEvent 没有 stopPropagation，不照搬别处的这一行｜读到：交互映射参考把 stopPropagation() 列在触摸事件一节，注明只停止 Touch 事件；或 rg 到别处回调里的 event.stopPropagation() 行（结果行看不出回调的事件类型）；写错：写成 .onClick((event: ClickEvent) => { event.stopPropagation() })，或给原本无参的 onClick 加上 ClickEvent 参数去调 stopPropagation
