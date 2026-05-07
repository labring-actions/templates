## 雾锁王国私服部署

直接打开这个链接：

+ [https://bja.sealos.run/?openapp=system-template%3FtemplateName%3Denshrouded](https://bja.sealos.run/?openapp=system-template%3FtemplateName%3Denshrouded)

> 没错，你看到的就是 Sealos 的应用模板，这些模板可用于快速创建和部署网站和各种应用程序。你可以在模板市场中找到各种类型的模板，这些模板不仅包含了前端项目，还包含了后端和其他各类应用的部署，具体可参考 [Sealos 模板市场相关文档](https://sealos.run/docs/guides/templates/)。

接下来你只需要设置一下私服的名称（SERVER_NAME）和密码（SERVER_PASSWORD），然后点击右上角的「去 Sealos 部署」。

> 如果您是第一次使用 Sealos，则需要注册登录 Sealos 公有云账号，登录之后会立即跳转到模板的部署页面。

跳转进来之后，点击右上角的「部署应用」开始部署，部署完成后，直接点击应用的「详情」进入该应用的详情页面。

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-21-20-07-dOxIba.png)

等待应用变成 Running 状态，然后点击日志按钮查看日志，只要出现了下面的日志，便是启动成功了：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-11-23-AY81c6.png)

启动成功后，你可以关闭或者最小化「应用管理」App，然后回到「模板市场」的 enshrouded 应用界面，拉到最下面的「Others」，你会看到有一个类型叫「Service」的资源，它的描述部分有一个字段是这样写的：`15637:30813/UDP`，15367 后面的端口就是公网端口，比如这里的公网端口就是 30813。

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-11-28-8IDC6P.png)

那么你这个私服的地址就是 `bja.sealos.run:30813`

## 登录游戏

### 前提条件

1. 首先您需要在本地下载安装 Steam 客户端。
2. 其次需要[在 Steam 商店中购买雾锁王国](https://store.steampowered.com/app/1203620/Enshrouded/?l=schinese)，并下载至本地。

### 收藏私服

1. 打开 Steam 登录账号，在 Steam 客户端内选择「查看」，再选择「游戏服务器」。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-11-49-amM7Mj.png)

2. 在「游戏服务器」弹窗中，点击「收藏」，然后点击右下角的「+」按钮。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-11-50-0v2Zwj.png)

3. 在弹窗内输入雾锁王国私服的公网域名和端口（例如我上面部署的私服地址就是 `bja.sealos.run:30813`）。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-11-51-8pur3u.png)

4. 添加完成后，即可以在「游戏服务器」的「收藏」中看到对应的服务器。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-11-51-khAYmU.png)

### 加入游戏

1. 在「库」中找到雾锁王国(Enshrouded)，点击「开始游戏」。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-13-50-JfQcqI.png)
   
2. 在游戏菜单中选择「加入（加入一局在线游戏）」。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-13-51-GdtYUD.jpg)

3. 您在 Steam 中收藏的游戏服务器将出现在「可用服务器」的顶端，直接点击「加入」。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-13-52-WsucRL.jpg)

4. 输入密码，点击「确认」按钮，即可加入游戏。
   
   ![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-22-13-53-DaCfH9.jpg)

## 进群

最后，欢迎加入 Sealos 雾锁王国服务器 QQ 交流群，与其他火焰之子一起重新夺回你的王国！

QQ 群号：688286365

二维码：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-02-23-01-04-RPARzr.jpg)