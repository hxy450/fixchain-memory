# 计划里的网络层任务

agent 会看到什么：源工程有 Retrofit Service、BuildConfig.BASE_URL、鉴权拦截器，计划的网络层任务只写「HTTP 请求封装」，规格产物里没有 API 清单

## 规矩

- rule-2dad1dcd0865｜计划里的网络层任务没有 API 清单作依据时，先产出清单再派基础设施实现｜读到：源工程有独立的网络模块（Retrofit Service、BuildConfig.BASE_URL、鉴权拦截器、统一响应壳），流程要求先产出 API 清单（spec/baseline/api-inventory/）；写错：规格产物里没有 API 清单；计划的网络层任务只写「网络层 (HTTP 请求封装)」，没有基址、接口路径、响应壳（成功码、message/data 字段）、鉴权头和网络权限
