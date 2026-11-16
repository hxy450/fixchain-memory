# MediaPlayer / ExoPlayer 播放器映射成 AVPlayer

agent 会看到什么：读到源端用 MediaPlayer 或 ExoPlayer / media3 播放（宿主 onPause / onStop 里不停播、Player.Listener 分 STATE_BUFFERING / STATE_READY、轮询 bufferedPosition、多卡共享一个实例）；规格或台账写「→ AVPlayer 行为等价」「→ Video 组件」，或以会新增播控卡片为由不做后台续播

## 规矩

- rule-56ce27d708c6｜宿主生命周期不停播放器时，规格的 AVPlayer 映射写明切后台续播并登 HARD-DIV/PD｜读到：宿主 Activity/Fragment 的 onPause、onStop、onDestroy 里不调用 MediaPlayer（或 ExoPlayer）的 pause/stop/release，只有显式退出或再次点击才停，播放会在退后台后继续到 onCompletion；写错：规格的跨栈映射行把「MediaPlayer 内联播放 → AVPlayer」判为「行为等价」，生命周期 AC 里没有「切后台继续播放至结束」，也没有 HARD-DIV 或 PD 登记
- rule-96b1bd9ac44d｜台账以「会新增播控卡片」为由把后台续播记成平台差异时，改记缺失功能并接入｜读到：安卓 MediaPlayer 播放在宿主 onPause/onStop 后继续，退后台播到结束；写错：决策台账或平台差异登记里写「接入 AVSession 会新增控制中心播控卡片」，据此不接 AVSession、不做后台续播
- rule-efa7103e0784｜源端播放器用到缓冲态、缓冲位或共享实例时，规格把 AVPlayer+XComponent 写成唯一路线｜读到：ExoPlayer / media3 的 Player.Listener 区分 STATE_BUFFERING / STATE_READY，轮询 bufferedPosition，Lifecycle ON_PAUSE / ON_RESUME 暂停恢复，feed 多卡共享一个 ExoPlayer；写错：转换决策写「ExoPlayer + PlayerView → Video 组件（或 AVPlayer + XComponent）」，理由写「Video 组件自带播放/缓冲状态回调」，三态由 onPrepared / onError / onLoading 驱动
