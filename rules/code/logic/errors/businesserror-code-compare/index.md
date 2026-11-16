# BusinessError.code 的错误码判别

agent 会看到什么：读到 d.ts 里接口写着 @throws { BusinessError } 加数值错误码（如 geoLocationManager 的 3301100）；产物里 catch 中用 (error as BusinessError).code === 某个常量分派错误分支

## 规矩

- rule-682c5991b3f9｜按 BusinessError.code 分派错误码分支时，先 Number(code) 归一再比较，不直接 ===｜读到：d.ts 里接口写着 @throws { BusinessError } 加数值错误码（如 geoLocationManager 的 3301100 定位开关关闭），@ohos.base 的 BusinessError.code 声明为 number；写错：catch 里写 (error as BusinessError).code === 某个 number 常量，没有归一；新增分支照抄已有的这种 === 判别
