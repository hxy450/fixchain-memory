# forward-ref-uncertain 占位解除时附核验证据，不以「共享件已定型」为由删标记

审的是：计划与派工
触发（任一种）：
- 读到：代码或占位登记里有 FWD-REF … kind=forward-ref-uncertain 标记，指向一处渲染效果没核验过的写法；写错的样子：收敛时删掉了 FWD-REF 标记或把登记行关掉，理由写「共享件已由另一切片定型」，没附截图、dump 或等价单测
适用范围：收敛阶段解除 forward-ref-uncertain 一类不确定占位时
做法：
- 解除前在登记行附上核验证据（截图、dump 或等价单测）及结论；拿不到证据的保留 FWD-REF 标记和登记行
来源：1 张卡，1 个应用
- case-0e3ff99e6b2aa8afcfff（Jetsnack）：做法第 1 步 ← 建议 5
