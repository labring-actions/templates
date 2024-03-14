为远程连接工具rustdesk在sealos中建立服务端。
1. 按照模板一键部署
> TIPS: 建议ENCRYPTED_ONLY选择1，这样只允许建立加密连接，不易被别人白嫖    

2. 部署成功，应用处于running状态后，在日志中找到暴露的域名（这里示例是ENCRYPTED_ONLY=0的情况）：    
![image](https://github.com/labring-actions/templates/assets/45360163/6c4042f7-3537-4aee-8c5f-d5a136d18c03)

3. 在我的应用--Other中找到映射的端口：    
![image](https://github.com/labring-actions/templates/assets/45360163/e8edc007-f41a-4415-bb0e-244bcb4e91f9)

4. 在你的客户端填入信息如下：    
> TIPS: 当ENCRYPTED_ONLY选择1时，必须填入下图设置中的Key。其内容从上面图1中的日志获取。

![image](https://github.com/labring-actions/templates/assets/45360163/437b342e-2439-4312-a697-6e0e8117bea8)

5. 点击客户端左上角 **主页**，看到底部状态栏绿色**就绪**，即部署+连接成功。Enjoy！
> TIPS: 管理好自己的中继/ID服务器信息，泄密会造成难以评估的后果！
