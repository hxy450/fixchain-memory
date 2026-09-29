# arkts/decorators

ArkUI V2 自定义组件的成员声明：装饰器是否带括号、@BuilderParam 默认值的写法、状态成员名与组件通用属性方法的冲突

[上一级](../index.md)

## 本级经验

- [V2 组件成员装饰器裸写（@Local/@Param/@Once/@Event），@BuilderParam 的默认值只引用 @Builder 函数或方法](lesson-8b145360b447a10d52ef.lesson.md)
  - 时机：界面实现阶段，在 @ComponentV2 自定义组件里声明 @Event 回调、@BuilderParam 插槽和状态字段时
  - 情境：组件要向宿主暴露交互回调、提供带空默认的可选内容插槽；派工或 skill 只列出装饰器名单，写者准备凭记忆给装饰器补括号，或用箭头函数作插槽默认值；生成期不编译。
- [自定义组件的状态成员不与组件通用属性方法同名（position、width、height、id、visibility、enabled、zIndex、opacity 等）](lesson-c1968bdf112ed3e6b259.lesson.md)
  - 时机：规格提取阶段为组件状态接口表命名 @Local/@Param 变量，或界面实现阶段在自定义组件 struct 中声明成员时
  - 情境：把源端事件或模型的字段名（如播放进度事件的 position）直接转写成组件成员；规格的状态接口表就是实现的成员表，实现者按表照写。
