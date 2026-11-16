# 列表条目和行内按钮的点击

agent 会看到什么：读到 adapter 的 onItemClickListener、addOnItemTouchListener 的 onSingleTapUp、行内按钮调远端接口；产物里 ForEach 条目上的 .onClick 和行内按钮请求在途时的防重

## 规矩

- rule-9babcec8b152｜列表迁移时逐项接上源端条目点击行为，ForEach 条目要有真的 .onClick，注释不算｜读到：源端 adapter 的 onItemClickListener，或 RecyclerView.addOnItemTouchListener 的 onSingleTapUp 里对条目做了事（如把条目内容 setText 回填到输入框）；写错：ForEach 条目的 Row / Column 只有样式链，没有 .onClick，上方注释却写着「点击回填输入框」
- rule-de9fdfaf0aac｜列表行的远端提交按钮按条目 ID 维护在途集合，在途时显示加载态、不再发请求｜读到：源端 Adapter 里每行的按钮调用远端接口，成功后只改当前 bean 的字段再 `notifyDataSetChanged()`；写错：目标端点击处理只在「已完成」标记为真时才返回，请求在途时可重复提交；同页别的按钮已有 busy 锁，这个按钮的 `onClick` 没沿用
- rule-53485dc2dfd1｜列表会整表重建时，ForEach 条目闭包按唯一字段 findIndex 定位当前行，不用 indexOf(row)｜读到：源端 ListActivity.onListItemClick(ListView, View, int position, long id) 或 onItemClick 按 position 从当前数据表取行，加载函数每次 new 一张新表；写错：条目 .onClick 闭包捕获行对象 row，处理函数里用 indexOf(row) 或 ForEach 生成时的 index 到当前数组里定位，再按这个位置取行
