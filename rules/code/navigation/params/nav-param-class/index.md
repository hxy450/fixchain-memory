# NavDestination 路由参数类的定义、导出和取用

agent 会看到什么：产物里 pushPathByName / replacePathByName 传的参数类和接收页 onReady 里对 pathInfo.param 的 instanceof 判定：参数类定义在哪个文件、有没有 export、发送页是不是自建同形类、路由层或页面之间谁 import 谁、字段名是否照源端路由参数（routerLink、;id=），以及 onReady 赋值之前就拿参数去 subscribe

## 规矩

- rule-668c7fde68ea｜路由参数类的字段名照源路由参数名写，不另起名｜读到：源端路由带参数，如模板里 [routerLink]=['/路径', 值]、矩阵参数 ;id=，规格写明「;id= 语义保留」；写错：参数类字段改成了别的名字（如 id 写成 userId），发送方赋 param.userId，接收方读的是 obj.id
- rule-8a5f88801993｜pushPathByName 的参数用发送页自建的同形类时，改为 import 目标页导出的参数类｜读到：目标页 NavDestination 的 onReady 里 context.pathInfo.param as Object 之后 instanceof 自己的参数类取参；写错：发送页 pushPathByName / replacePathByName('页面名', new P(...)) 里的 P 是本文件 class P 定义的同形类，不是从目标页所在文件（或共享模型）import 进来的
- rule-e02096ac8fb7｜接收页 onReady 里 instanceof 判定的路由参数类没有 export 时，直接 export 它｜写错：NavDestination 页面里 class P { … } 前面没有 export，onReady 里却用 context.pathInfo.param 再 instanceof P 判定
- rule-709b4cfce30e｜路由层要构造或多页共用的路由参数类，放进不导入页面的叶子模块，路由层不导入页面｜读到：规格或切片对接点写明页面依赖路由封装：页面的 NavPathStack 接收路由层定义的参数类型，页面经路由封装的 push(route, param) 导航和返回；写错：路由封装或服务层文件里出现 `import { …Param } from '../pages/…'`，参数类定义在页面 .ets 里并 export
- rule-8bfc9ed91d72｜订阅键取自路由参数时，在 NavDestination.onReady 赋值之后订阅，并确认有生产者｜写错：aboutToAppear 里用还没赋值的路由参数作键调 subscribe(...)（参数在 onReady 才赋值），订阅键恒为空串；页面里没有任何发该键事件的生产调用
