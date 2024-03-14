为远程连接工具 rustdesk 在 sealos 中建立服务端。    

1. 按照模板一键部署    

> TIPS：建议 ENCRYPTED_ONLY 选择 1，这样只允许建立加密连接，不易被别人白嫖    

2. 部署成功，应用处于 running 状态后，在日志中找到暴露的域名 (这里示例是 ENCRYPTED_ONLY=0 的情况)：   

![](https://github.com/labring-actions/templates/assets/45360163/6c4042f7-3537-4aee-8c5f-d5a136d18c03)

3. 在我的应用--Other 中找到映射的端口：    

![](https://github.com/labring-actions/templates/assets/45360163/e8edc007-f41a-4415-bb0e-244bcb4e91f9)

4. 在你的客户端填入信息如下：

> TIPS：当 ENCRYPTED_ONLY 选择1时，必须填入下图设置中的 Key。其内容从上面图 1 中的日志获取。

![](https://github.com/labring-actions/templates/assets/45360163/437b342e-2439-4312-a697-6e0e8117bea8)

5. 点击客户端左上角**主页**，看到底部状态栏绿色**就绪**，即部署+连接成功。Enjoy！

> TIPS：管理好自己的中继/ID 服务器信息，泄密会造成难以评估的后果！
