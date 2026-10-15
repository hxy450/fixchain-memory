# arkts/decorators

ArkUI V2 自定义组件的成员声明：装饰器是否带括号、状态成员名与组件通用属性方法的冲突

[上一级](../index.md)

## 本级经验

- [@ComponentV2 成员装饰器裸写，只有 @Provider()、@Consumer()、@Monitor('path') 这类带参装饰器写括号](lesson-8b145360b447a10d52ef.lesson.md)
  - 时机：界面实现阶段，在 @ComponentV2 自定义组件里声明状态字段与 @Event 回调时
  - 情境：组件要向宿主暴露交互回调与状态参数；派工或 skill 只列出装饰器名单，写者准备凭记忆给装饰器补括号；生成期不编译。
- [自定义组件的成员名不与 CommonMethod 通用属性方法同名（如 position、width、height、animation）](lesson-c1968bdf112ed3e6b259.lesson.md)
  - 时机：规格提取阶段为组件状态接口表命名 @Local/@Param 变量，或界面实现阶段在自定义组件 struct 中声明成员时
  - 情境：把源端事件或模型的字段名（如播放进度事件的 position）直接转写成组件成员；规格的状态接口表就是实现的成员表，实现者按表照写。 也包括为新建组件声明尺寸参数或动画实例字段（width/height、animation），或按另一处先写好的调用点参数名声明 @Param。
