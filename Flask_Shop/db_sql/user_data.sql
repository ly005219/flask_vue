INSERT into t_menus(id,name,level,path) VALUES(-1,'全部',0,NULL);--#-1为系统默认菜单不写0，因为sql里面代表维护了

INSERT into t_menus(id,name,level,parent_id) VALUES(1,'用户管理',1,-1);--parent_id为-1代表父节点为系统默认菜单
INSERT into t_menus(id,name,level,parent_id) VALUES(2,'权限管理',1,-1);
INSERT into t_menus(id,name,level,parent_id) VALUES(3,'商品管理',1,-1);
INSERT into t_menus(id,name,level,parent_id) VALUES(4,'订单管理',1,-1);
INSERT into t_menus(id,name,level,parent_id) VALUES(5,'数据统计',1,-1);






INSERT into t_menus(id,name,level,path,parent_id) VALUES(11,'用户列表',2,'/user_list/',1);
INSERT into t_menus(id,name,level,path,parent_id) VALUES(21,'角色列表',2,'/role_list/',2);
INSERT into t_menus(id,name,level,path,parent_id) VALUES(22,'权限列表',2,'/permission_list/',2);
INSERT into t_menus(id,name,level,path,parent_id) VALUES(31,'商品列表',2,'/product_list/',3);
INSERT into t_menus(id,name,level,path,parent_id) VALUES(32,'分类列表',2,'/category_list/',3);--3表示一级目录的第三个菜单，2表示该菜单下的第二个子菜单
INSERT into t_menus(id,name,level,path,parent_id) VALUES(41,'订单列表',2,'/order_list/',4);
INSERT into t_menus(id,name,level,path,parent_id) VALUES(51,'统计列表',2,'/statistics_list/',5);




