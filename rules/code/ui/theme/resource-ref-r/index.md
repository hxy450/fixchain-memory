# 组件属性里的 $r 资源引用

agent 会看到什么：读过的派工或改写前的代码要求尺寸、颜色走 $r('app.float.…') 一类资源引用；交回的代码里属性参数写成 $r(...)、裸的 'app.类型.名' 字符串或数值常量

## 通用查法

### 组件属性要不要写 $r，按鸿蒙 SDK 里该属性的参数类型定

审的是：代码
触发（任一种）：
- 读到：派工或主题说明要求尺寸、颜色走 $r('app.float.…') / $r('app.color.…')，或改写前的代码用 $r(...) 引资源；写错的样子：属性参数写成 $r(...) 而声明只收 number（如 .blur($r(…))），或写成没有 $r 包裹的 'app.float.…' 字符串
适用范围：ArkUI 页面里给组件属性传资源引用或数值时
做法：
- 到鸿蒙 SDK 的 ets/component 下该组件的 d.ts（通用属性在 common.d.ts 的 CommonMethod）按属性名找签名，看参数类型及它展开的类型别名里有没有 Resource
- 有 Resource（如 Length、ResourceColor）的写 $r('app.类型.名')，不写裸的 'app.类型.名' 字符串；只收 number 的写数值常量
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare function $r(value: string, ...params: any[]): Resource；value 格式是 'belonging.type.name'：只有经 $r 才解析成资源（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
- declare type Length = string | number | Resource：尺寸参数收资源；也收 string，所以裸资源键编译不报错、却不当资源解析（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Length）
- declare type ResourceColor = Color | number | string | Resource：颜色参数收资源，裸资源键同样静默失效（出处：鸿蒙 SDK 的 ets/component/units.d.ts，ResourceColor）
- blur(value: number, options?: BlurOptions): T：例：模糊半径只收 number，传 $r 编译报错（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.blur）
针对本应用要查的：
- 这个属性的参数类型：鸿蒙 SDK 的 ets/component 下该组件的 d.ts，通用属性在 common.d.ts 的 CommonMethod，按属性名找方法签名；参数类型或它展开的类型别名（units.d.ts 里的 Length、ResourceColor 等）里有 Resource 就写 $r(...)，没有就写数值常量
来源：2 张卡，2 个应用
- case-0ac442a09e1e8ee36a8a（DeepAI全能PPT）：做法第 2 步 ← 建议 4
- case-ca8dec09be8655edbb02（组件岛Widget Island）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-3e14962732e7｜资源引用写成没有 $r 包裹的 'app.float.…' 字符串时，改回 $r(...)，批量替换用单引号脚本并读回｜读到：改写前的原行是 $r('app.float.…') 这类资源引用；写错：改写后成了 .margin({ top: ('app.float.dp_89') }) 这类没有 $r 包裹的资源键字符串（'app.类型.名字'），编译照样通过
- rule-b07a1082ae31｜派工要求尺寸走 $r 时，blur、Swiper.itemSpace 仍写数值常量，不传 $r｜读到：派工或主题说明写「颜色、尺寸全部绑定资源」「尺寸经 $r('app.float.*')」；同布局已有页面写的是 .blur(<数值常量>)、.itemSpace(<数值>)；写错：页面里写成 .blur($r('app.float.…')) 或 .itemSpace($r('app.float.…'))
