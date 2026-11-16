# getColorSync 取到的 ARGB 颜色的拆分和插值

agent 会看到什么：读到颜色端点取自 resourceManager.getColorSync(...)（32 位 ARGB 数）或 color.json 的 '#AARRGGBB'，规格要求按 fraction 插值或混色，工程里可能已有按 >>> 24、& 0xFF 拆通道的混色工具；产物里页面各自用 slice(1, 3) / parseInt / padStart 拆拼颜色

## 规矩

- rule-51c985178289｜颜色端点是 32 位 ARGB 或 #AARRGGBB 时，插值按 A/R/G/B 位移拆分，不用 slice(1,3)｜读到：颜色端点取自 resourceManager.getColorSync(...)（32 位 ARGB 数），或 color.json 里的 8 位值 '#AARRGGBB'；规格要求按 fraction 插值或混色（折叠顶栏、状态过渡、按压态）；写错：插值或混合函数用 slice(1, 3) / slice(3, 5) / slice(5, 7) 当 R / G / B 拆，再 padStart(6) 拼回 6 位串，把 alpha 字节当成红色
- rule-6bc3127bb1c9｜工程里颜色产出和解析共用一种格式，复用已有 ARGB 混色工具，不在页面各自手写拆分｜读到：工程的公共主题或工具模块里已有 ARGB 混色函数（按 `>>> 24`、`& 0xFF` 拆通道），或多个页面都要对 getColorSync 取到的颜色做插值；写错：页面里各自手写颜色拆分和拼接（slice( / parseInt( / padStart(），没有复用公共的混色工具，也没注明输入输出格式
