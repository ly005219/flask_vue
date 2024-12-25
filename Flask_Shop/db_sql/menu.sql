-- 清理现有菜单数据
TRUNCATE TABLE t_menus;

-- 添加一级菜单
INSERT INTO t_menus (id, name, level, path, parent_id) VALUES 
(1, '用户管理', 1, '/users/', NULL),
(2, '权限管理', 1, '/rights/', NULL),
(3, '商品管理', 1, '/goods/', NULL),
(4, '订单管理', 1, '/orders/', NULL),
(5, '数据统计', 1, '/reports/', NULL);

-- 添加二级菜单
INSERT INTO t_menus (name, level, path, parent_id) VALUES 
('用户列表', 2, '/user_list/', 1),
('角色列表', 2, '/role_list/', 2),
('权限列表', 2, '/permission_list/', 2),
('商品列表', 2, '/goods_list/', 3),
('分类参数', 2, '/params/', 3),
('商品分类', 2, '/categories/', 3),
('SKU管理', 2, '/sku_manage/', 3),
('订单列表', 2, '/order_list/', 4),
('数据报表', 2, '/reports/', 5); 