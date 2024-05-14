# 挂载文件夹


```
sudo mount -t cifs "@共享文件夹目录" "@想要挂载到的目录" -o vers=2.0,dir_mode=0777,file_mode=0777,mfsymlinks,cache=strict,rsize=1048576,wsize=1048576,username="@用户名",password="@密码"
```


# 安装依赖

```
pip install -r requirements.txt
```


# docker

```
docker build -t scheduler .
```
