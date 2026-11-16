# GridView / ListView 的滚动和按压态

agent 会看到什么：读到源 GridView / ListView 没改 listSelector、scrollbars、overScrollMode，条目高由内容量出、没有固定行高；页面规格只写列数和间距，或写「网格不滚动、一屏全可见」

## 规矩

- rule-040c6a91b00c｜列表/网格页规格写明按压态、滚动条、越界效果的主题来源，以及会不会滚动｜读到：源 GridView / ListView 没改 listSelector、scrollbars、overScrollMode；Activity 主题在多个 values-vNN/styles.xml 里定义；写错：页面规格只写了列数和间距，没写条目按压态、滚动条、越界效果来自哪个主题和框架默认，也没写会不会滚动
- rule-3db595935c9c｜验收写「网格不滚动、一屏全可见」时，先按源端格高算总高再定｜读到：源 GridView / ListView 没有固定行高，条目高由内容量出（getView 未设固定高的 LayoutParams）；写错：规格或验收条目写「网格不滚动」「典型屏全可见」，没有按源端格高和行距算出的总高做依据
