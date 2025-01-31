## 安装步骤

配置 [office 版本自定义工具](https://config.office.com/deploymentsettings)

安装 office

`setup /download config.xml`

`setup /configure config.xml`

KMS 激活

`cd C:\Program Files\Microsoft Office\Office16`

`cscript ospp.vbs /sethst:kms.03k.org`

`cscript ospp.vbs /act`

注意：如果你安装的是32位版本，那么启动命令第一个要改成：cd C:\Program Files (x86)\Microsoft Office\Office16

### 注意

要删除以前的许可证和缓存的帐户信息：点击下载 [OLicenseCleanup.zip](https://download.microsoft.com/download/e/1/b/e1bbdc16-fad4-4aa2-a309-2ba3cae8d424/OLicenseCleanup.zip) 文件，管理员运行 OLicenseCleanup.vbs。