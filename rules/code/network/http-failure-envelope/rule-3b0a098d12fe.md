# 分页加载的单元测试要注入失败信封，断言返回 false 且 hasMore、游标不变

审的是：代码
触发（任一种）：
- 读到：源端分页方法失败时设错误、return false，成功路径才改 hasMore/游标；写错的样子：测试里 mock 的 HttpClient 只返回 status 200 的信封，没有用例覆盖 status !== 200 时 loadMore 的返回值和状态
适用范围：目标端带 hasMore、游标等分页状态、走永不 reject 信封客户端的方法的自测
做法：
- 注入一个失败信封（如 { status: 500, message: … }），断言方法返回 false、error 等于信封 message、hasMore 和游标保持调用前的值
来源：1 张卡，1 个应用
- case-7cb7554a3696dcbc7647（real-estate-hmos）：做法第 1 步 ← 建议 3
