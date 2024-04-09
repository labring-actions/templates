三分钟即可拥有一个强大稳定的 Minecraft 联机服务器。

直接打开这个链接：

+ [https://bja.sealos.run/?openapp=system-template%3FtemplateName%3Dminecraft](https://bja.sealos.run/?openapp=system-template%3FtemplateName%3Dminecraft)

> 没错，你看到的就是 Sealos 的应用模板，这些模板可用于快速创建和部署网站和各种应用程序。你可以在模板市场中找到各种类型的模板，这些模板不仅包含了前端项目，还包含了后端和其他各类应用的部署，具体可参考 [Sealos 模板市场相关文档](https://sealos.run/docs/guides/templates/)。

接下来你只需要选择服务器的核心（TYPE），输入服务器的 Minecraft 版本（VERSION），然后点击右上角的「去 Sealos 部署」。

> 如果您是第一次使用 Sealos，则需要注册登录 Sealos 公有云账号，登录之后会立即跳转到模板的部署页面。

跳转进来之后，点击右上角的「部署应用」开始部署，部署完成后，直接点击应用的「详情」进入该应用的详情页面。

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-03-02-21-03-IPhnsg.png)

等待应用变成 Running 状态，然后点击日志按钮查看日志，只要出现了下面的日志，便是启动成功了：

![](https://cdn.jsdelivr.net/gh/yangchuansheng/imghosting-test@main/uPic/2024-03-02-21-05-ovzT6f.png)

启动成功后，你可以关闭或者最小化「应用管理」App，然后回到「模板市场」的 minecraft 应用界面，拉到最下面的「Others」，你会看到有一个类型叫「Service」的资源，它的描述部分有一个字段是这样写的：`25565:31483/TCP`。25565 后面的端口就是公网端口，比如这里的公网端口就是 31483。

那么你这个 Minecraft 服务器的地址就是 `bja.sealos.run:31483`