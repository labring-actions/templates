本模板用来定时备份帕鲁私服中的存档，备份保存在 `/palworld/backups` 目录下。

需要填写两个参数：

### 1. APP_NAME

这是你的帕鲁私服应用名称，你需要在 Sealos 桌面打开「应用管理」，在应用列表中找到你的帕鲁私服应用名字，就是我红框圈出来的部分，复制这个名字作为 APP_NAME 的值。

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-29-16-25-r1LlVk.jpg)

### 2. INTERVAL

你希望每隔几小时备份一次，这里就填几。比如，如果你想每 5 个小时备份一次，这里就填 5。

填写好参数以后，点击右上角的「部署应用」开始部署，完结撒花。

你可以点击 CronJob 的「详情」进入定时任务的详情页面：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-31-17-34-z1O8Hc.jpg)

在这里你可以暂停定时任务，也可以修改定时任务，爱咋咋的！

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-31-17-34-36vlam.jpg)

---

## 查看存档备份

**这一步非常重要！！！为了防止别人能访问你的文件管理器，一定要修改密码！！！**

在「应用管理」界面进入 palworld 应用的详情页面，然后点击我用红框框出来的外网地址：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-27-16-09-6edDbv.png)

打开文件管理器后，输入用户名密码登录，默认的用户名是 `admin`，默认密码也是 `admin`。登录之后，先点击 "Settings":

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-27-16-12-LSucr2.jpg)

然后点击 "User management"，再点击 admin 最右边的铅笔按钮：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-27-16-26-LtKvG4.jpg)

在 "Password" 输入框中填入你的新密码，然后将 Language 的值改为「中文（简体）」：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-27-16-27-aWTOJm.jpg)

最后点击右下角的 save 即可。

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-27-16-27-bgXwUj.jpg)

现在回到主界面，你会看到这里有个 backups 文件夹，这个文件夹里都是你的备份，你可以随意下载转存：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting6@main/uPic/2024-01-31-17-33-DlfaDp.jpg)