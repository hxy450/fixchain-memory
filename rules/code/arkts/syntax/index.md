# 组件语法与装饰器

交回的 .ets 里有 @Builder / @BuilderParam、build() 里的组件写法、@ComponentV2 的 @Param / @Local / @Event 成员、.stateStyles，或构建报 10905102、10905203 这类错误时

## 触发族

- [@BuilderParam 插槽的传参和默认值](builder-param/index.md)（4 条）：读到子组件声明的 @BuilderParam 插槽、父组件要传的成员 @Builder 或 10905102 一类编译报错；产物里写成 content: this.someBuilder 方法引用、箭头函数默认值、箭头函数体里直接实例化自定义组件，或测试把直传写法定成契约
- [build() 和 @Builder 里的组件语法](builder-syntax/index.md)（2 条）：产物里组件语法写在不带 @Builder 的普通方法里，或 build() / @Builder 的组件树压成一行、if 块后带分号、条件分支不带花括号
- [V2 组件的成员装饰器和成员名](v2-member-decl/index.md)（2 条）：@ComponentV2 struct 里声明 @Param / @Local / @Event 成员：装饰器带没带括号、成员名是否撞上 width、position 等通用属性
- [.stateStyles 的写法和 10905203 报错](state-styles/index.md)（3 条）：构建日志报 10905203 '.stateStyles' doesn't conform standard；产物里 .stateStyles 的状态值写成键值对象或 this. 引用的成员 @Styles，以及修这个报错时改动的范围
