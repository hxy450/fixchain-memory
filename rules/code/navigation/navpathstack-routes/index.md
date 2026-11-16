# NavPathStack 的路由名、出栈和返回刷新

agent 会看到什么：读到 Compose Navigation 的带参路由、popUpTo 回根或子页 pop 回原页；产物里 pushPathByName 的首参和 param、navDestination 按名字分发、pop / clear，以及返回原页后的刷新回调

## 规矩

- rule-2db019cc9b4c｜Compose 路由带 {参数} 占位符时，pushPathByName 首参写固定名，参数只走 param｜读到：Compose Navigation 用带 {参数} 占位符的路由模式注册目的地（composable("detail/{id}", arguments = listOf(navArgument("id")…))），另有函数把 id 拼进路由串再 navController.navigate(…)；写错：pushPathByName 的首参是模板字符串或字符串拼接（如 pushPathByName(`detail/${id}`, id)），同一个 id 既拼进名字又作为 param 传
- rule-8d9c3f44336a｜调用方传来动态目的地名时，改回固定名，navDestination 只按固定名精确匹配｜读到：调用方 pushPathByName 的首参是模板字符串（如 `detail/${id}`）；写错：navDestination 的 builder（pageMap）里用 name.startsWith('…/') 前缀分发；路由常量类里留着按 id 拼串的构造函数
- rule-4e8e2da7472b｜popUpTo 根且 inclusive 的回根导航，目标用 NavPathStack.clear()，不用 pop()｜读到：Compose Navigation 回调里 navController.navigate(root) { popUpTo(root) { inclusive = true } }；写错：完成回调里写 this.navPathStack.pop()，只退一层，回到已失效的详情页
- rule-2b28271b48db｜返回原页要做一次性动作时按挂载方式选回调，不依赖第二次 aboutToAppear｜读到：子页修改共享模型后 pop 回原页；原页是 Navigation(this.navPathStack) { … } 的首页内容或 NavPathStack 里的 NavDestination；写错：返回时的同步放在「第二次 aboutToAppear」分支里，或给 Navigation 首页内容挂 .onShown 刷新；pop 回来时这些都没执行，界面仍是旧值
- rule-6501f0282e19｜用条件渲染或下标切 tab 时，在 @Entry 的 onBackPress 里实现非起始 tab 返回回起始 tab｜读到：底部导航切 tab 用 popUpTo(startDestination) { saveState = true }，源注释说在其他底部 tab 按返回回到起始目的地；写错：@Entry 页没有 onBackPress，tab 切换注释写「popUpTo saveState 的状态保持由条件渲染承接」，非起始 tab 按系统返回直接退出
- rule-14652d349754｜pushPathByName 前先看目标页 onReady instanceof 的类并 import，不自造同形类｜读到：目标页 NavDestination 的 onReady 用 param instanceof <某参数类> 收窄，或工程里已有统一的路由参数类模块；写错：生产页在本文件里新建字段相同或相近的局部参数类，并 new 它传给 pushPathByName
- rule-6fa2f9ded329｜onReady 的参数可能是 JSON.parse 出的 DTO 时，不用 instanceof DTO 类判定｜读到：源端在 Compose 的 NavHost 导航里把整个 data class 数据对象交给目标页，目标页提交只用它的 id、name 等字段；写错：目标 onReady 里只写 if (param instanceof <DTO 类>) 才赋值，而这个 DTO 在工程里是 JSON.parse(body) as T 得到的普通对象
- rule-31cc886a2578｜来源页 pushPathByName 带 onPop 时，子页成功出栈写 pop(result)，不写裸 pop()｜读到：来源页用 pushPathByName(name, param, onPop) 打开子页，onPop 里按 instanceof 判 popInfo.result 的类型；写错：子页成功分支写完共享回传通道后裸 this.navPathStack.pop()，或 pop(...) 出去的实例类型和 onPop 里 instanceof 判的类型不一致
- rule-7eecd19f15c8｜子页只写共享回传通道时，来源页在 NavDestination.onShown 里读取，不只在 onPop 里读｜读到：子页成功后只把结果写进共享回传通道（AppStorageV2 槽位、单例一类，无回调无事件），再 pop()；写错：来源页只在 pushPathByName(..., onPop) 的回调里读共享通道，NavDestination 上没有 .onShown(...) 读取
- rule-34f720b77e28｜移交项写「同款」的其他 onPop 消费点时，改判型要一并 grep 修改｜读到：brief 或移交项列出某个 pushPathByName(..., onPop) 消费点的 instanceof 判型，并写「…同款」指向别的调用点；写错：只改了一处 onPop 里的 instanceof 类型，同款的其他 pushPathByName(..., onPop) 调用点仍判旧类型，和生产端 pop(result) 的类型对不上
- rule-885c09d62ed4｜源端回退失败时走带 popUpTo 清栈的导航，目标 fallback 也先清栈，不用通用 push｜读到：if (!navController.popBackStack()) XDestination.navigate(navController)，而该 navigate 带 popUpTo(navController.graph.id) { inclusive = true }；写错：目标回退函数在 pop 失败后调用通用的 push(fallbackRoute, …)，没先清栈；同文件里已有先 clear 再 push 的方法却没用，单页栈回退后栈深为 2
