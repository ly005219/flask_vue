-- SKU表
CREATE TABLE t_skus (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    sku_code VARCHAR(50) UNIQUE,
    specifications JSON,
    price DECIMAL(10,2),
    stock INT,
    sales INT DEFAULT 0,
    status INT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES t_products(id)
);

-- 规格模板表
CREATE TABLE t_spec_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    category_id INT,
    specs JSON,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES t_categories(id)
);

-- 库存日志表
CREATE TABLE t_stock_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sku_id INT,
    change_amount INT,
    type VARCHAR(20),
    operator VARCHAR(50),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku_id) REFERENCES t_skus(id)
); 

-- 先检查是否存在
DELETE FROM t_menus WHERE name = 'SKU管理';

-- 添加新菜单
INSERT INTO t_menus (name, level, path, parent_id) 
VALUES ('SKU管理', 2, '/sku_manage/', 3);

-- 添加测试数据
INSERT INTO t_skus (product_id, sku_code, specifications, price, stock, sales, status) VALUES 
(1, 'SKU-001', '{"颜色": "红色", "尺码": "S"}', 199.99, 100, 20, 1),
(1, 'SKU-002', '{"颜色": "红色", "尺码": "M"}', 199.99, 150, 30, 1),
(1, 'SKU-003', '{"颜色": "红色", "尺码": "L"}', 199.99, 80, 15, 1),
(1, 'SKU-004', '{"颜色": "蓝色", "尺码": "S"}', 199.99, 120, 25, 1),
(1, 'SKU-005', '{"颜色": "蓝色", "尺码": "M"}', 199.99, 90, 40, 1),
(1, 'SKU-006', '{"颜色": "蓝色", "尺码": "L"}', 199.99, 70, 10, 1);

-- 添加规格模板测试数据
INSERT INTO t_spec_templates (name, category_id, specs) VALUES
('服装规格', 65, '{"尺码": ["S", "M", "L", "XL", "XXL"], "颜色": ["红色", "蓝色", "黑色", "白色"]}'),
('鞋靴规格', 84, '{"鞋码": ["35", "36", "37", "38", "39", "40", "41", "42", "43", "44"], "颜色": ["黑色", "白色", "棕色"]}'),
('手机规格', 28, '{"内存": ["4GB", "6GB", "8GB"], "存储": ["64GB", "128GB", "256GB"], "颜色": ["黑色", "白色", "金色"]}');

-- 添加库存变动日志测试数据
INSERT INTO t_stock_logs (sku_id, change_amount, type, operator) VALUES
(1, -10, 'sale', 'system'),
(1, 50, 'restock', 'admin'),
(2, -5, 'sale', 'system'),
(2, 30, 'restock', 'admin'),
(3, -8, 'sale', 'system'),
(4, -12, 'sale', 'system'),
(5, -15, 'sale', 'system'),
(6, -5, 'sale', 'system');