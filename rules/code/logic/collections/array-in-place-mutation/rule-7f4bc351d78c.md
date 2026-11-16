# 源端把同一个 List 引用交给另一对象再就地 remove 时，目标保持同一引用，不用 slice 拷贝

审的是：代码
触发（任一种）：
- 读到：源端把一个 getter 返回的 List 直接传给另一个对象的 setter（没有 new ArrayList<>(...)），后续任务对这个 List 调 contains / remove 就地修改；写错的样子：目标写成 .slice() 或 [...list] 拷贝后再赋值，或对拷贝出来的副本 splice，源端共享引用、就地删除的数据流被切断
适用范围：源端在对象之间共享集合引用、后续代码依赖就地修改结果时
不适用的情形：源端显式 new ArrayList<>(...) 拷贝的，目标才拷贝
做法：
- 目标直接赋同一个数组引用（a.list = b.list），后续删除用 splice 作用在这个数组本身上
- 写完后逐个核对目标里的 .slice() 和 [...x]，每个都要对应源端的一次真实拷贝
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- slice(start?: number, end?: number): T[]：返回数组一段的拷贝，不改原数组（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，Array.slice）
- splice(start: number, deleteCount?: number): T[]：在原数组上删除元素，返回删掉的元素（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，Array.splice）
- public ArrayList(Collection<? extends E> c)：源端的拷贝构造：新建一个含相同元素的列表；只有见到它（或类似的拷贝）时目标才拷贝（出处：java.util.ArrayList#ArrayList(Collection)）
来源：1 张卡，1 个应用
- case-44a53125e4f44a862c80（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；例外 1 ← 建议 3
