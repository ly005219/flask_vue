# flask_vue
去master分支下载对应的demo，这个main分支只有项目的介绍和部署，在word文档里面也有项目效果图和部分介绍

# 本地部署
  #虚拟环境

  
    python -m venv myenv
    
  
    myenv\Scripts\activate   #(windows)
    

    #source myenv/bin/activate  #(mac)




2：用编辑器打开Flask_Shop文件夹 pip install -r requirements.txt   (安装项目的第三方库)

3: 创建一个名为flask_shop的数据库，mysql5.7（其实mysql8版本好像也可以）指定utf8mb4,运行flask_shop.sql文件，最后启动manager.py即可  (我指定的用户名和密码都是root，你也可以根据config.py更改)
![image](https://github.com/user-attachments/assets/48f30d0b-8961-444f-b6c1-8f9c2165b7b7)

4:前端得下载好node.js版本，我的是v22.11.0，如果你有多个版本可以使用  fnm use 版本号  暂时来切换到项目所需的版本

     4.1： npm install -g yarn

     4.2:  yarn install  #安装依赖
     
     4.3： yarn serve   #启动项目即可

# docker部署
可以打开文件夹电商后端管理，使用-p指定名称，使用docker来启动项目，如有端口需要可以更改具体的dockerfile

    docker-compose -p myecommerce up --build -d  



# 部分效果图(具体在word里面有)

<img width="414" alt="image" src="https://github.com/user-attachments/assets/4f705f0a-6f8b-45f0-b276-64c1313f51ca" />


<img width="416" alt="image" src="https://github.com/user-attachments/assets/84d32a13-ab4c-4ecb-a503-3e1c758c5eff" />


<img width="415" alt="image" src="https://github.com/user-attachments/assets/efdb2c2b-1ac1-4ea7-ade6-11698d22aea8" />


<img width="416" alt="image" src="https://github.com/user-attachments/assets/806e91ce-3d4d-401f-862e-1379385a47af" />
