# 源端靠 GZIPInputStream 抛异常判损坏时，目标在 gzopen 前先校验魔数 1f 8b

审的是：代码
触发（任一种）：
- 读到：源端用 `GZIPInputStream` 读压缩内容，catch 到异常就返回加载失败态；写错的样子：目标用 zlib 的 gzopen(path, 'rb') + gzread 直接解压、没校验格式，注释却写「损坏时抛错」；调用方只靠 catch 判损坏
适用范围：把源端以 GZIPInputStream 异常识别损坏的读取迁成 @ohos.zlib 的 GZip 读取时
做法：
- 解压前读出文件头两个字节，不是 0x1f、0x8b 就按损坏处理（返回失败态），是才走 gzopen(path, 'rb') + gzread
- 契约注释只写已核实的行为：gzopen 的 'rb' 对非 gzip 文件不抛错、按原样读出，损坏由魔数校验识别
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- gzopen(path: string, mode: string): Promise<void>：打开 .gz 文件读取解压（出处：鸿蒙 SDK 的 ets/api/@ohos.zlib.d.ts，GZip.gzopen）
- mode 为 'r' 或 'rb' 时自动检测并解压 gzip，非 gzip 格式直接读取原始数据：不会把非 gzip 或头损坏当异常（出处：js-apis-zlib.md，gzopen）
- GZIP_MAGIC = 0x8b1f；头两字节不符时构造函数抛 ZipException("Not in GZIP format")：源端损坏即异常的来源；按字节顺序是 1f、8b（出处：java.util.zip.GZIPInputStream#readHeader）
- 读取前校验魔数 1f 8b 后，损坏内容显示失败态：修好后的行为（出处：卡里修好并验证过）
- gzdopen(fd: number, mode: string): Promise<void>：同族接口：按文件描述符打开，mode 同 gzopen（出处：鸿蒙 SDK 的 ets/api/@ohos.zlib.d.ts，GZip.gzdopen）
未核实：非 gzip 直接读出原始数据的说法本机 API 23 的声明注释里没有，只在文档里；卡里说读到的是声明注释，可能出自更新的 SDK
来源：1 张卡，1 个应用
- case-3f05228d17f878067234（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 6、诊断；做法第 2 步 ← 建议 6；取值 4 ← 诊断
