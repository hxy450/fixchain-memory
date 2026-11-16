# ArkTS 语法与工程

交回的 .ets 里有 @Builder、@BuilderParam、@ComponentV2 成员、.stateStyles、Record 和对象字面量，或构建日志报 arkts-* 和组件语法错误，或涉及 BuildProfile、HAR 模块和跨文件导入时

## 子主题

- [构建与模块](build/index.md)（18 条）：源端有 BuildConfig 字段，或交回的代码涉及 BuildProfile、HAR 模块、跨模块和跨文件的 import / export、新建的常量类文件，或为修编译错误改过文件时
- [组件语法与装饰器](syntax/index.md)（11 条）：交回的 .ets 里有 @Builder / @BuilderParam、build() 里的组件写法、@ComponentV2 的 @Param / @Local / @Event 成员、.stateStyles，或构建报 10905102、10905203 这类错误时
- [类型约束](typing/index.md)（12 条）：交回的代码里有 Record、索引签名、无类型的对象字面量、implements 和构造写法、process.getEnvironmentVar 这类可选值，或构建报 arkts-no-* 类型错误时
