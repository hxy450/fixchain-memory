# 源 Activity 和业务基类生命周期回调里的刷新和副作用

agent 会看到什么：读到源页面只在 onCreate、onNewIntent 里刷新（没有 onResume 刷新），或业务基类的 onPostCreate / onResume 里先 findViewById 判空、instanceof 或标志位守卫再做淡入等副作用；规格把它映射成 onActive / 回到前台即刷新，或在基类副作用表里写成无条件表项

## 规矩

- rule-3f6a333c4596｜源页面只在 onNewIntent 里刷新时，规格不把它映射成 onActive｜读到：源页面只在 onCreate 和 onNewIntent（先 super.onNewIntent 再刷新）里刷新，没有 onResume 刷新；写错：规格把「onNewIntent 刷新」映射成「页面 onActive / 回到前台即刷新」，验收条目写成「源:…onNewIntent → 标:…onActive」
- rule-5f8440e2402b｜基类副作用带 findViewById 判空等守卫时，规格连条件一起写并逐个子类按布局判定｜读到：安卓业务基类的 onPostCreate / onResume 里先 findViewById(R.id.x)，if (view != null) 才执行淡入等副作用；或用 instanceof、标志位守卫；写错：规格的基类副作用表把它写成无条件表项（「某子类继承 → 进页 250ms 淡入」），没写守卫条件，也没给每个子类「生效 / 不生效」的布局证据
