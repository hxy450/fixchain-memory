# V2 组件的成员装饰器和成员名

agent 会看到什么：@ComponentV2 struct 里声明 @Param / @Local / @Event 成员：装饰器带没带括号、成员名是否撞上 width、position 等通用属性

## 规矩

- rule-d0a1c25c7ba8｜V2 组件里 @Event、@Local、@Param 等裸写，不带括号；只有工厂装饰器带括号｜读到：派工或规格写「装饰器锁 V2（@ComponentV2 / @Local / @Param / @Event / …）」，组件要向宿主暴露交互回调；写错：@ComponentV2 组件里写出 @Event()、@Local()、@Param() 这类带空括号的成员装饰器；编译报 Expected 2 arguments, but got 0
- rule-b99ccbb01a61｜自定义组件的 @Param / @Local / 私有成员不与 width、position 等通用属性同名｜读到：调用点按 `({ width: …, height: … })` 给新组件传尺寸；工程已有的 Lottie 组件把实例存为 animationItem；写错：组件里声明 @Param width / @Param height，或 private animation: AnimationItem | undefined
