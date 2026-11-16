# 交接摘要与移交项

交回的交接摘要、契约摘要、计划或 TODO 里转述源端方法的行为，或者上游交接、子代理回执写明某项交给别的任务、主线程或后续切片承接时

## 触发族

- [源端回调和计算入口的全部产出](source-callback-outputs/index.md)（4 条）：源端一个结果回调（LiveData observe）或计算入口同时给出几项：成功、失败分支各自的跳转、finish、Toast、本地标记，或一组下游字段；计划、TODO 占位或修复报告里只写了其中几项
- [移交来的焦点获取项](focus-handoff/index.md)（1 条）：移交登记写「焦点获取细节归 Slice N」，接手方报告记为完成，而 .onKeyEvent 仍挂在原子组件上、没有获焦代码
- [子代理交给主线程处理的子任务](main-thread-subtasks/index.md)（1 条）：子代理回执写某些子任务「跳过、由主线程处理」，主线程宣布 Stage 完成时没有逐项勾销，模板残留还在
- [上游指派的全局动作（如 registerFont）](global-actions/index.md)（1 条）：上游交接写明某个全局动作由某任务落地，拆分或重派后的各段派工都没有这项要求，也没写由哪一段承接
- [契约摘要里的资源读取函数](contract-summary/index.md)（1 条）：Base 代码里资源读取函数的注释写着「横屏取另一个值，运行期须经读取函数按方向取」，契约摘要只列了 export function 的签名，没带使用约束
- [子任务回执里要带给下一方的事项（交接项、Host-side 项、decision_gaps）](subtask-return-carryover/index.md)（3 条）：子任务回执、worker 信封或组件头注里写着「写权不属本批（交接项）」、Host-side 项（要宿主补的调用）、decision_gaps 和跨文件注入项；之后的移交登记、下游派工、接线切片派工或给 closer 的摘要里没有这些项，也没点名负责方
- [Base 回执里共享 helper 的已知限制](base-helper-limits/index.md)（1 条）：Base 阶段交回的回执风险写共享 helper 的返回值有前提（依赖单连接、串行执行语义）、可能不准，调度只记 Base 完成就派下游，派工里没要求核实或替换这个 helper，基础契约里也没写它的限制
