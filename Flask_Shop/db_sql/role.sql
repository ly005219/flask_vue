-- 清理现有角色数据
TRUNCATE TABLE t_roles;
TRUNCATE TABLE t_roles_menus;

-- 添加角色
INSERT INTO t_roles (id, name, desc) VALUES
(1, '超级管理员', '拥有所有权限'),
(2, '商品管理员', '管理商品相关'),
(3, '订单管理员', '管理订单相关');

-- 为超级管理员添加所有菜单权限
INSERT INTO t_roles_menus (role_id, menu_id)
SELECT 1, id FROM t_menus;

-- 为商品管理员添加商品相关菜单
INSERT INTO t_roles_menus (role_id, menu_id)
SELECT 2, id FROM t_menus WHERE parent_id = 3 OR id = 3;

-- 为订单管理员添加订单相关菜单
INSERT INTO t_roles_menus (role_id, menu_id)
SELECT 3, id FROM t_menus WHERE parent_id = 4 OR id = 4; 