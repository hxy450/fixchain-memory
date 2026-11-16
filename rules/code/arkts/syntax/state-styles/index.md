# .stateStyles 的写法和 10905203 报错

agent 会看到什么：构建日志报 10905203 '.stateStyles' doesn't conform standard；产物里 .stateStyles 的状态值写成键值对象或 this. 引用的成员 @Styles，以及修这个报错时改动的范围

## 规矩

- rule-66bd2ae4a55b｜.stateStyles 的状态值写成「名称: 值」键值对象时，改成点号开头的内联样式块或 @Styles 引用｜读到：构建日志报 10905203 '.stateStyles' doesn't conform standard，要给 .stateStyles 换一种写法；写错：写成 `.stateStyles({ pressed: { backgroundColor: $r(…) } })`：状态值的花括号里是「属性名: 值」，不是以点号开头的属性方法调用
- rule-43c9f7b80a45｜同文件有多个 struct 时，stateStyles 用内联样式块或全局 @Styles，不引用成员的｜读到：构建日志对 .stateStyles 报 10905203 '.stateStyles' doesn't conform standard，报错的文件里除页面外还有别的 struct（如页内弹窗组件）
- rule-ed8936c7fd52｜编译修复只改构建日志报错的那一处，没报错文件里的同型写法原样保留｜读到：构建日志的报错（如 10905203 '.stateStyles' doesn't conform standard）只指向某个文件的某一行，别的文件里有同型写法但没报错；写错：改动里连日志没报错的文件中同型的 .stateStyles 写法也改了（报告里称「潜伏同型」），原来的 @Styles 方法留着不再使用
