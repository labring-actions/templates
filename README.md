## Deploy On Sealos

通过本仓库的模板可以轻松在 Sealos 上运行各种应用，无需关心应用之间的依赖关系，只需一键轻松部署。

https://fastdeploy.cloud.sealos.io/   （一键部署链接）

![](homepage.png)

## 如何创建模板

- 你能够通过现有的模板文件或 Create Template(todo)按钮来创建你的应用模版。可基于 [template.yaml](template.yaml) 来创建想要的模板。你也可以像 GitHub Action 一样通过${{ SEALOS_NAMESPACE }}填写一些环境变量的的信息。环境变量的具体信息查看[environment.txt](environment.txt)。
- 以FastGPT为例展示如何创建一个模板，详见[example.md](example.md)

## 如何引入Deploy On Sealos

- 在png目录下为您准备了 Deploy On Sealos 的按钮图标，您只需将该按钮跳转到https://fastdeploy.cloud.sealos.io/deploy?type=form&templateName=fastgpt 即可进入 Sealos 的一键部署页面，详见 [Deploy On Sealos.md](Deploy%20On%20Sealos.md)。

[![](png/deploy on sealos/Deploy-On-Sealos-B-1.5x.png)](https://fastdeploy.cloud.sealos.io/deploy?type=form&templateName=fastgpt)

