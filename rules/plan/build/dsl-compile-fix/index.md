# 编译修复改动的 stateStyles / @Styles 写法

agent 会看到什么：编译修复改了 .stateStyles 或 @Styles 这类 d.ts 里类型是 any 的 UI DSL 写法，编译门报告对这处只写构建 PASS，没列成需打开页面验证的项

## 规矩

- rule-6bd8c0441952｜编译修复改了 stateStyles、@Styles 这类 DSL 写法时，报告列为需打开页面验证并写明入口｜读到：编译修复改了 .stateStyles 或 @Styles 的写法，这类 UI DSL 构造在 d.ts 里的类型是 any；写错：编译门报告对这处改动只写构建 PASS，没有列成「需打开页面验证」的项，也没写页面入口
