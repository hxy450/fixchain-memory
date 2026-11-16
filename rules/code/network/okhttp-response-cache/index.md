# OkHttp 缓存迁成 rcp ResponseCache

agent 会看到什么：读到 OkHttp 的 Cache(dir, 容量)、CacheControl.Builder 的 maxAge / maxStale 或缓存拦截器；产物里 rcp.ResponseCache 的 CacheConfiguration.maxSize、Cache-Control 头里的指令，以及 cache.set 外面的 catch

## 规矩

- rule-7a228d1ef4a7｜OkHttp Cache 的 MiB 容量迁到 rcp CacheConfiguration.maxSize 时按字节传｜读到：OkHttp 的 Cache(dir, N MiB) 提供自动 HTTP 缓存，容量常量按 MiB 写；写错：rcp.ResponseCache 的 CacheConfiguration.maxSize 直接传 MiB 数（如 maxSize: 200），ResponseCache.set 报 item is too long for cache limits，缓存计数一直为 0
- rule-7e0d654591be｜OkHttp 的 maxStale 迁成 max-stale，不用 stale-while-revalidate 代替｜读到：OkHttp 的 CacheControl.Builder().maxAge(7, DAYS).maxStale(30, DAYS) 控制图片缓存；规格写「7 天 max-age / 30 天 max-stale」；写错：目标缓存头写成 `public, max-age=604800, stale-while-revalidate=2592000`，max-stale 被换成别的指令
- rule-122dd0733424｜ResponseCache.set 的失败不要空 catch 吞掉，至少把错误信息记进日志｜写错：拦截器或缓存封装里 await cache.set(...) 外面是空的 catch {}，缓存写入失败没有任何日志
