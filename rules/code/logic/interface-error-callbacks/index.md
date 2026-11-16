# 应用接口的 on* 错误回调和它们的提示

agent 会看到什么：读到源实现类 @Override 基类（空默认实现）的多个 on* 错误回调、各自 showToast(R.string.…)，或操作的 errorCallback 只转给应用接口的错误回调；产物里子类只覆写规格点名的几个 on*、其余继承空实现，或页面桥的失败回调直接 showToast 资源键字面量

## 规矩

- rule-7b2f9bcd2bba｜实现应用接口子类时以源 @Override 全集核对，基类空默认的回调补覆写或登记缺口｜读到：源实现类 @Override 了基类的多个 on* 错误回调（基类是空默认实现），各自 showToast(R.string.…)；写错：目标子类（extends 空默认基类）只覆写规格点名的几个 `on*` 回调并接了对应 sink，其余错误回调继承空实现，引擎和控制器调用它们时静默
- rule-9e8c8a3df357｜页面桥接失败时走应用接口的错误回调，不在桥里用裸资源键 toast｜读到：源端拍照等操作的 errorCallback 只调应用接口的错误回调，由它 showToast 本地化提示；目标工程已有 toast(key) 先经 getStringByNameSync 解析的写法；写错：页面桥的失败回调里直接 showToast('…_…', true) 传小写下划线的资源键字面量，绕过应用接口的错误回调；或在调了错误回调之外又 toast 一次
