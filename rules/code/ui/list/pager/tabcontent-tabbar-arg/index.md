# TabContent 的 .tabBar 参数

agent 会看到什么：产物里 TabContent 上 .tabBar(...) 传的是 { title: '…' } 这类不在任何重载里的对象字面量（编译报 10505001 No overload matches this call），还是字符串、@Builder、TabBarOptions

## 规矩

- rule-df82c3d7f0b6｜tabBar 传了 { title } 等自造对象时，改用字符串、@Builder 或 TabBarOptions｜写错：TabContent 上写 .tabBar({ title: '…' }) 这类不在任何重载里的对象字面量，编译报 10505001 No overload matches this call
