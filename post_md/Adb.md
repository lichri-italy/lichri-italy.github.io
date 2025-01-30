## 操作步骤

下载 [Adb 便携包](https://suanpersonale-my.sharepoint.com/:u:/g/personal/suan_suanpersonale_onmicrosoft_com/Ef9BMRkeAk9JntkCaMaHKh4BkEdp4tawMTbMxHNFDngVqQ?e=ACPWH0)

连接 adb
adb connect 127.0.0.1:58526

### 安装应用
adb install 安装包路径

### 卸载应用

查看手机应用包列表
adb shell pm list packages

查看特定应用的包名，回车后，启动你想要获取包名的应用
adb shell am monitor

删除命令
adb shell pm uninstall -k --user 0 应用包名