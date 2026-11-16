# process.getEnvironmentVar 读出的可选配置

agent 会看到什么：读到改写前的代码是 process.getEnvironmentVar('X') || '' 这类带缺省的回退链；产物里 const v = process.getEnvironmentVar('X') 之后直接读 v.length 或 Number(v)，没有 || '' / ?? '' 或判 undefined

## 规矩

- rule-d160a32dfae4｜getEnvironmentVar 读可选配置时，先兜空串再读 .length 或做 Number()｜读到：改写前的代码是 `process.getEnvironmentVar('X') || ''` 这类带缺省的回退链；写错：改成 `const v = process.getEnvironmentVar('X')` 后直接读 `v.length` 或 `Number(v)`，没有 `|| ''` / `?? ''` 或判 undefined
