## 配置

配置用户名和邮箱

`git config --global user.name "你的用户名"`

`git config --global user.email "你的邮箱"`

这将设置全局用户名和邮箱，以便在提交时识别身份。

生成SSH密钥

`ssh-keygen -t rsa`

将生成的公钥添加到GitHub账户的SSH设置中。

## 操作

回退到某个 commit

`git log`

`git reset --hard 哈希值`