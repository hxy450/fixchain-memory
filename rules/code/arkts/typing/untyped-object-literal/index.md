# 没有声明类型的对象字面量

agent 会看到什么：产物里对象字面量直接作实参、返回值、路由参数或类型（return { … }、{ id: item.id }、Array<{ … }>），构建日志报 arkts-no-untyped-obj-literals / arkts-no-obj-literals-as-types

## 规矩

- rule-ec3d1592ec6e｜对象字面量作实参、返回值或回调返回值时，落到已声明的 class/interface｜写错：`.map((item) => ({ … }))` 或没标返回类型的箭头函数里 `return { … }`，或用 `{ … } as T` 充当返回值
- rule-dcbf24ea08ad｜路由参数和 @State 集合元素类型用显式类，不写 { id } 和 Array<{…}>｜写错：`@State xs: Array<{ id: number; … }>` 这类用对象字面量声明的类型
- rule-93c5460160bd｜编译修复把路由载荷的 Record 或对象字面量类型改成具名接口时，字段名取自调用方和目标页解析｜读到：构建日志报 arkts-no-obj-literals-as-types 或 arkts-no-any-unknown，路由表里目标页的载荷类型是 Record<string, string> 或对象字面量类型；写错：新写的 interface 字段名在各调用方 pushPathByName 的参数和目标页 pathInfo.param 的解析里都找不到，源 Activity 的 Intent extra 键里也没有
