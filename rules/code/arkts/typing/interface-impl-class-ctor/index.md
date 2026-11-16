# 接口的实现和类的构造写法

agent 会看到什么：产物里把没 implements 的类实例或箭头函数对象字面量传给 interface 形参、新类写 constructor(public x)，构建日志报 arkts-no-structural-typing / arkts-no-ctor-prop-decls

## 规矩

- rule-2913941b5ac9｜把已有类实例交给接口参数时，写 implements 该接口的适配类再传，不靠结构兼容｜读到：目标参数类型是新声明的接口（`interface` 只声明方法签名），手头的对象是没有 `implements` 它的独立 class；工程里已有 class … implements … 的适配写法；写错：直接把这个类实例传给接口参数（编译报 `arkts-no-structural-typing`），或改用箭头函数属性的对象字面量实现该接口
- rule-dd871ba54e05｜只含方法签名的依赖接口，传 implements 它的具名类实例，不用箭头函数对象字面量｜读到：依赖接口（`interface`）里只声明方法签名；修编译错的参考对 `arkts-no-untyped-obj-literals` 只给「赋给类型变量」的修法；写错：把箭头函数属性的对象字面量（`{ name: () => … }`）直接作实参传给要该接口的方法，或先赋给标了该接口类型的变量再传
- rule-e076a2729758｜按编译报错新写类时不用 constructor(public x)，改字段声明加构造体赋值｜写错：新类写成 `constructor(public id: number, …) {}` 这类构造参数属性
