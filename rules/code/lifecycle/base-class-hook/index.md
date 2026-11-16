# 派工要求承接的基类横切钩子

agent 会看到什么：读到派工写某页承接基类的淡入等钩子，源基类里是 findViewById(R.id.x) 判空后才执行；产物里页面加了 .opacity(...) 加 .onAppear / onShown 的淡入或别的基类横切副作用

## 规矩

- rule-2be090d604a8｜接到基类横切钩子义务时先在源布局 grep 守卫 id，不成立就不实现并登记差异｜读到：派工写「某页承接基类淡入钩子」，源基类里是 findViewById(R.id.x) 判空后才执行；写错：页面里加了 .opacity(...) + .onAppear / onShown 的淡入或其他基类横切副作用，而源子类布局里没有基类守卫的 id
