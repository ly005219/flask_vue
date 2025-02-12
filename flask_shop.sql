/*
 Navicat Premium Dump SQL

 Source Server         : Test
 Source Server Type    : MySQL
 Source Server Version : 50735 (5.7.35-log)
 Source Host           : localhost:3306
 Source Schema         : flask_shop

 Target Server Type    : MySQL
 Target Server Version : 50735 (5.7.35-log)
 File Encoding         : 65001

 Date: 25/12/2024 21:42:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('42bdc6605a82');

-- ----------------------------
-- Table structure for t_attributes
-- ----------------------------
DROP TABLE IF EXISTS `t_attributes`;
CREATE TABLE `t_attributes`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `_type` enum('static','dynamic') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `category_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id`) USING BTREE,
  CONSTRAINT `t_attributes_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `t_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_attributes
-- ----------------------------
INSERT INTO `t_attributes` VALUES (1, '品牌', 'soulkiss', 'static', 65);
INSERT INTO `t_attributes` VALUES (2, '适用年龄', '25-29周岁', 'static', 65);
INSERT INTO `t_attributes` VALUES (3, '材质', '蚕丝', 'static', 65);
INSERT INTO `t_attributes` VALUES (4, '尺码', 'S M L', 'static', 65);
INSERT INTO `t_attributes` VALUES (5, '面料', '其他', 'static', 65);
INSERT INTO `t_attributes` VALUES (6, '图案', '纯色', 'static', 65);
INSERT INTO `t_attributes` VALUES (7, '风格', '通勤', 'static', 65);
INSERT INTO `t_attributes` VALUES (8, '通勤', '简约', 'static', 65);
INSERT INTO `t_attributes` VALUES (9, '领型', '立领', 'static', 65);
INSERT INTO `t_attributes` VALUES (10, '衣门襟', '单排扣', 'static', 65);
INSERT INTO `t_attributes` VALUES (11, '颜色分类', '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static', 65);
INSERT INTO `t_attributes` VALUES (12, '组合形式', '单件', 'static', 65);
INSERT INTO `t_attributes` VALUES (13, '货号', 'S904548', 'static', 65);
INSERT INTO `t_attributes` VALUES (14, '成分含量', '95%以上', 'static', 65);
INSERT INTO `t_attributes` VALUES (15, '裙型', 'A字裙', 'static', 65);
INSERT INTO `t_attributes` VALUES (16, '年份季节', '2019年夏季', 'static', 65);
INSERT INTO `t_attributes` VALUES (17, '袖长', '无袖', 'static', 65);
INSERT INTO `t_attributes` VALUES (18, '裙长', '中长裙', 'static', 65);
INSERT INTO `t_attributes` VALUES (19, '款式', '其他/other', 'static', 65);
INSERT INTO `t_attributes` VALUES (20, '廓形', 'A型', 'static', 65);
INSERT INTO `t_attributes` VALUES (21, '尺码', 'S,M,L,XL,XXL', 'dynamic', 65);
INSERT INTO `t_attributes` VALUES (22, '颜色分类', '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic', 65);
INSERT INTO `t_attributes` VALUES (24, '颜色', '深幽蓝', 'static', 82);
INSERT INTO `t_attributes` VALUES (25, '颜色类型', '红色,蓝色,绿色', 'dynamic', 83);
INSERT INTO `t_attributes` VALUES (27, '测试增加', '测试增加静态属性', 'static', 99);
INSERT INTO `t_attributes` VALUES (35, '火龙果', '好吃', 'static', 100);
INSERT INTO `t_attributes` VALUES (36, '火龙果', '哈哈哈', 'static', 100);
INSERT INTO `t_attributes` VALUES (37, '西瓜', NULL, 'static', 100);
INSERT INTO `t_attributes` VALUES (38, '草莓', NULL, 'static', 100);
INSERT INTO `t_attributes` VALUES (39, '蓝莓', NULL, 'static', 100);
INSERT INTO `t_attributes` VALUES (40, '尺码描述', NULL, 'dynamic', 100);
INSERT INTO `t_attributes` VALUES (41, '样式', NULL, 'dynamic', 65);
INSERT INTO `t_attributes` VALUES (47, '测试静态属性', '红色，黄色', 'static', 65);
INSERT INTO `t_attributes` VALUES (48, '动态测试', NULL, 'dynamic', 65);
INSERT INTO `t_attributes` VALUES (49, '哈哈哈', NULL, 'dynamic', 65);
INSERT INTO `t_attributes` VALUES (50, '嘻嘻', '红色,蓝色,绿色', 'dynamic', 65);

-- ----------------------------
-- Table structure for t_categories
-- ----------------------------
DROP TABLE IF EXISTS `t_categories`;
CREATE TABLE `t_categories`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `parent_id` int(11) NULL DEFAULT NULL,
  `level` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `parent_id`(`parent_id`) USING BTREE,
  CONSTRAINT `t_categories_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `t_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 162 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_categories
-- ----------------------------
INSERT INTO `t_categories` VALUES (1, '女装 /男装 /内衣', NULL, 1);
INSERT INTO `t_categories` VALUES (2, '鞋靴 /箱包 /配件', NULL, 1);
INSERT INTO `t_categories` VALUES (3, '童装玩具 /孕产 /用品', NULL, 1);
INSERT INTO `t_categories` VALUES (4, '家电 /数码 /手机', NULL, 1);
INSERT INTO `t_categories` VALUES (5, '美妆 /洗护 /保健品', NULL, 1);
INSERT INTO `t_categories` VALUES (6, '珠宝 /眼镜 /手表', NULL, 1);
INSERT INTO `t_categories` VALUES (7, '运动 /户外 /乐器', NULL, 1);
INSERT INTO `t_categories` VALUES (8, '游戏 /动漫 /影视', NULL, 1);
INSERT INTO `t_categories` VALUES (9, '美食 /生鲜 /零食', NULL, 1);
INSERT INTO `t_categories` VALUES (10, '鲜花 /宠物 /农资', NULL, 1);
INSERT INTO `t_categories` VALUES (11, '面料集采 /装修 /建材', NULL, 1);
INSERT INTO `t_categories` VALUES (12, '家具 /家饰 /家纺', NULL, 1);
INSERT INTO `t_categories` VALUES (13, '汽车 /二手车 /用品', NULL, 1);
INSERT INTO `t_categories` VALUES (14, '办公 /DIY /五金电子', NULL, 1);
INSERT INTO `t_categories` VALUES (15, '百货 /餐厨 /家庭保健', NULL, 1);
INSERT INTO `t_categories` VALUES (16, '学习 /卡券 /本地服务', NULL, 1);
INSERT INTO `t_categories` VALUES (17, '女装', 1, 2);
INSERT INTO `t_categories` VALUES (18, '男装', 1, 2);
INSERT INTO `t_categories` VALUES (19, '内衣', 1, 2);
INSERT INTO `t_categories` VALUES (20, '鞋靴', 2, 2);
INSERT INTO `t_categories` VALUES (21, '箱包', 2, 2);
INSERT INTO `t_categories` VALUES (22, '配件', 2, 2);
INSERT INTO `t_categories` VALUES (23, '童装玩具', 3, 2);
INSERT INTO `t_categories` VALUES (24, '孕产', 3, 2);
INSERT INTO `t_categories` VALUES (25, '用品', 3, 2);
INSERT INTO `t_categories` VALUES (26, '家电', 4, 2);
INSERT INTO `t_categories` VALUES (27, '数码', 4, 2);
INSERT INTO `t_categories` VALUES (28, '手机', 4, 2);
INSERT INTO `t_categories` VALUES (29, '美妆', 5, 2);
INSERT INTO `t_categories` VALUES (30, '洗护', 5, 2);
INSERT INTO `t_categories` VALUES (31, '保健品', 5, 2);
INSERT INTO `t_categories` VALUES (32, '珠宝', 6, 2);
INSERT INTO `t_categories` VALUES (33, '眼镜', 6, 2);
INSERT INTO `t_categories` VALUES (34, '手表', 6, 2);
INSERT INTO `t_categories` VALUES (35, '运动', 7, 2);
INSERT INTO `t_categories` VALUES (36, '户外', 7, 2);
INSERT INTO `t_categories` VALUES (37, '乐器', 7, 2);
INSERT INTO `t_categories` VALUES (38, '游戏', 8, 2);
INSERT INTO `t_categories` VALUES (39, '动漫', 8, 2);
INSERT INTO `t_categories` VALUES (40, '影视', 8, 2);
INSERT INTO `t_categories` VALUES (41, '美食', 9, 2);
INSERT INTO `t_categories` VALUES (42, '生鲜', 9, 2);
INSERT INTO `t_categories` VALUES (43, '零食', 9, 2);
INSERT INTO `t_categories` VALUES (44, '鲜花', 10, 2);
INSERT INTO `t_categories` VALUES (45, '宠物', 10, 2);
INSERT INTO `t_categories` VALUES (46, '农资', 10, 2);
INSERT INTO `t_categories` VALUES (47, '面料集采', 11, 2);
INSERT INTO `t_categories` VALUES (48, '装修', 11, 2);
INSERT INTO `t_categories` VALUES (49, '建材', 11, 2);
INSERT INTO `t_categories` VALUES (50, '家具', 12, 2);
INSERT INTO `t_categories` VALUES (51, '家饰', 12, 2);
INSERT INTO `t_categories` VALUES (52, '家纺', 12, 2);
INSERT INTO `t_categories` VALUES (53, '汽车', 13, 2);
INSERT INTO `t_categories` VALUES (54, '二手车', 13, 2);
INSERT INTO `t_categories` VALUES (55, '用品', 13, 2);
INSERT INTO `t_categories` VALUES (56, '办公', 14, 2);
INSERT INTO `t_categories` VALUES (57, 'DIY', 14, 2);
INSERT INTO `t_categories` VALUES (58, '五金电子', 14, 2);
INSERT INTO `t_categories` VALUES (59, '百货', 15, 2);
INSERT INTO `t_categories` VALUES (60, '餐厨', 15, 2);
INSERT INTO `t_categories` VALUES (61, '家庭保健', 15, 2);
INSERT INTO `t_categories` VALUES (62, '学习', 16, 2);
INSERT INTO `t_categories` VALUES (63, '卡券', 16, 2);
INSERT INTO `t_categories` VALUES (64, '本地服务', 16, 2);
INSERT INTO `t_categories` VALUES (65, '连衣裙', 17, 3);
INSERT INTO `t_categories` VALUES (66, '半身裙', 17, 3);
INSERT INTO `t_categories` VALUES (67, '毛针织衫', 17, 3);
INSERT INTO `t_categories` VALUES (68, 'T恤', 17, 3);
INSERT INTO `t_categories` VALUES (69, '短外套', 17, 3);
INSERT INTO `t_categories` VALUES (70, '卫衣', 17, 3);
INSERT INTO `t_categories` VALUES (71, '汉服', 17, 3);
INSERT INTO `t_categories` VALUES (72, 'JK制服', 17, 3);
INSERT INTO `t_categories` VALUES (73, 'LOLITA', 17, 3);
INSERT INTO `t_categories` VALUES (74, '衬衫', 17, 3);
INSERT INTO `t_categories` VALUES (75, '百搭裤装', 17, 3);
INSERT INTO `t_categories` VALUES (76, '裤裙', 17, 3);
INSERT INTO `t_categories` VALUES (77, '牛仔裤', 17, 3);
INSERT INTO `t_categories` VALUES (78, '西装', 17, 3);
INSERT INTO `t_categories` VALUES (79, '大码女装', 17, 3);
INSERT INTO `t_categories` VALUES (80, '时尚套装', 17, 3);
INSERT INTO `t_categories` VALUES (81, '蕾丝衫/雪纺衫', 17, 3);
INSERT INTO `t_categories` VALUES (82, '风衣', 17, 3);
INSERT INTO `t_categories` VALUES (83, '休闲裤', 17, 3);
INSERT INTO `t_categories` VALUES (84, '背心吊带', 17, 3);
INSERT INTO `t_categories` VALUES (85, '马夹', 17, 3);
INSERT INTO `t_categories` VALUES (86, '牛仔外套', 17, 3);
INSERT INTO `t_categories` VALUES (87, '阔腿裤', 17, 3);
INSERT INTO `t_categories` VALUES (88, '中老年女装', 17, 3);
INSERT INTO `t_categories` VALUES (89, '婚纱礼服', 17, 3);
INSERT INTO `t_categories` VALUES (90, '民族服装', 17, 3);
INSERT INTO `t_categories` VALUES (91, '打底裤', 17, 3);
INSERT INTO `t_categories` VALUES (92, '西装裤', 17, 3);
INSERT INTO `t_categories` VALUES (93, '唐装', 17, 3);
INSERT INTO `t_categories` VALUES (94, '旗袍', 17, 3);
INSERT INTO `t_categories` VALUES (95, '春夏新品', 18, 3);
INSERT INTO `t_categories` VALUES (96, 'T恤', 18, 3);
INSERT INTO `t_categories` VALUES (97, '衬衫', 18, 3);
INSERT INTO `t_categories` VALUES (98, 'POLO衫', 18, 3);
INSERT INTO `t_categories` VALUES (99, '休闲裤', 18, 3);
INSERT INTO `t_categories` VALUES (100, '牛仔裤', 18, 3);
INSERT INTO `t_categories` VALUES (101, '套装', 18, 3);
INSERT INTO `t_categories` VALUES (102, '外套', 18, 3);
INSERT INTO `t_categories` VALUES (103, '夹克', 18, 3);
INSERT INTO `t_categories` VALUES (104, '卫衣', 18, 3);
INSERT INTO `t_categories` VALUES (105, '风衣', 18, 3);
INSERT INTO `t_categories` VALUES (106, '西装', 18, 3);
INSERT INTO `t_categories` VALUES (107, '牛仔外套', 18, 3);
INSERT INTO `t_categories` VALUES (108, '棒球服', 18, 3);
INSERT INTO `t_categories` VALUES (109, '品质好物', 18, 3);
INSERT INTO `t_categories` VALUES (110, '皮衣', 18, 3);
INSERT INTO `t_categories` VALUES (111, '针织衫/毛衣', 18, 3);
INSERT INTO `t_categories` VALUES (112, '运动裤', 18, 3);
INSERT INTO `t_categories` VALUES (113, '工装裤', 18, 3);
INSERT INTO `t_categories` VALUES (114, '开衫', 18, 3);
INSERT INTO `t_categories` VALUES (115, '马甲', 18, 3);
INSERT INTO `t_categories` VALUES (116, '毛呢大衣', 18, 3);
INSERT INTO `t_categories` VALUES (117, '羽绒服', 18, 3);
INSERT INTO `t_categories` VALUES (118, '棉衣', 18, 3);
INSERT INTO `t_categories` VALUES (119, '中老年', 18, 3);
INSERT INTO `t_categories` VALUES (120, '情侣装', 18, 3);
INSERT INTO `t_categories` VALUES (121, '大码', 18, 3);
INSERT INTO `t_categories` VALUES (122, '民族风', 18, 3);
INSERT INTO `t_categories` VALUES (123, '专柜大牌', 18, 3);
INSERT INTO `t_categories` VALUES (124, '明星网红', 18, 3);
INSERT INTO `t_categories` VALUES (125, '原创设计', 18, 3);
INSERT INTO `t_categories` VALUES (126, '法式内衣', 19, 3);
INSERT INTO `t_categories` VALUES (127, '无钢圈内衣', 19, 3);
INSERT INTO `t_categories` VALUES (128, '内裤女', 19, 3);
INSERT INTO `t_categories` VALUES (129, '文胸', 19, 3);
INSERT INTO `t_categories` VALUES (130, '内裤男', 19, 3);
INSERT INTO `t_categories` VALUES (131, '长袖睡衣', 19, 3);
INSERT INTO `t_categories` VALUES (132, '睡裙', 19, 3);
INSERT INTO `t_categories` VALUES (133, '真丝睡衣', 19, 3);
INSERT INTO `t_categories` VALUES (134, '丝袜', 19, 3);
INSERT INTO `t_categories` VALUES (135, '船袜', 19, 3);
INSERT INTO `t_categories` VALUES (136, '情侣睡衣', 19, 3);
INSERT INTO `t_categories` VALUES (137, '抹胸', 19, 3);
INSERT INTO `t_categories` VALUES (138, '背心', 19, 3);
INSERT INTO `t_categories` VALUES (139, '睡袍', 19, 3);
INSERT INTO `t_categories` VALUES (140, '男士睡衣', 19, 3);
INSERT INTO `t_categories` VALUES (141, '塑身衣', 19, 3);
INSERT INTO `t_categories` VALUES (142, '内衣套装', 19, 3);
INSERT INTO `t_categories` VALUES (143, '打底裤', 19, 3);
INSERT INTO `t_categories` VALUES (144, '连体睡衣', 19, 3);
INSERT INTO `t_categories` VALUES (145, '聚拢文胸', 19, 3);
INSERT INTO `t_categories` VALUES (146, '男士袜子', 19, 3);
INSERT INTO `t_categories` VALUES (147, '棉袜女', 19, 3);
INSERT INTO `t_categories` VALUES (148, '卡通睡衣', 19, 3);
INSERT INTO `t_categories` VALUES (149, '无痕内裤', 19, 3);
INSERT INTO `t_categories` VALUES (150, '少女文胸', 19, 3);
INSERT INTO `t_categories` VALUES (151, 'iPhone手机', 28, 3);
INSERT INTO `t_categories` VALUES (155, '测试一级分类', NULL, 1);
INSERT INTO `t_categories` VALUES (157, '测试的第三级', NULL, 3);
INSERT INTO `t_categories` VALUES (158, '测试二级', 155, 2);
INSERT INTO `t_categories` VALUES (160, '测试2', NULL, 1);

-- ----------------------------
-- Table structure for t_express
-- ----------------------------
DROP TABLE IF EXISTS `t_express`;
CREATE TABLE `t_express`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `update_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_id`(`order_id`) USING BTREE,
  CONSTRAINT `t_express_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `t_orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_express
-- ----------------------------
INSERT INTO `t_express` VALUES (1, 1, '商品已经下单', '2050-01-19 12:17:21');
INSERT INTO `t_express` VALUES (2, 1, '您的订单开始处理', '2050-01-19 12:27:20');
INSERT INTO `t_express` VALUES (3, 1, '您的订单待配货', '2050-01-21 16:34:07');
INSERT INTO `t_express` VALUES (4, 1, '您的包裹已出库', '2050-01-21 16:34:07');
INSERT INTO `t_express` VALUES (5, 1, '包裹正在等待揽收', '2050-01-21 19:00:29');
INSERT INTO `t_express` VALUES (6, 1, '顺丰速运 已收取快件', '2050-01-22 15:30:00');
INSERT INTO `t_express` VALUES (7, 1, '快件在【金华婺城集收客户营业部】已装车,准备发往 【金华金东中转场】', '2050-01-23  5:30:00');
INSERT INTO `t_express` VALUES (8, 1, '快件到达 【金华金东中转场】', '2050-01-23 20:03:00');
INSERT INTO `t_express` VALUES (9, 1, '快件在【金华金东中转场】已装车,准备发往 【北京首都机场集散中心2】', '2050-01-23 22:36:00');
INSERT INTO `t_express` VALUES (10, 1, '快件到达 【北京首都机场集散中心2】', '2050-01-24 16:01:00');
INSERT INTO `t_express` VALUES (11, 1, '快件在【北京首都机场集散中心2】已装车,准备发往 【石家庄高开集散中心】', '2050-01-24 16:22:00');
INSERT INTO `t_express` VALUES (12, 1, '快件到达 【石家庄高开集散中心】', '2050-01-25 03:14:00');
INSERT INTO `t_express` VALUES (13, 1, '快件在【石家庄高开集散中心】已装车,准备发往 【衡水桃城集散点】', '2050-01-25 06:14:00');
INSERT INTO `t_express` VALUES (14, 1, '快件到达 【衡水桃城集散点】', '2050-01-25 13:38:00');
INSERT INTO `t_express` VALUES (15, 1, '快件在【衡水桃城集散点】已装车,准备发往 【衡水市桃城区肖家屯新村营业点】', '2050-01-26 06:26:00');
INSERT INTO `t_express` VALUES (16, 1, '快件到达 【衡水市桃城区肖家屯新村营业点】', '2050-01-25 07:23:00');
INSERT INTO `t_express` VALUES (17, 1, '快件交给潘君策,正在派送途中（联系电话：13788888888,顺丰已开启“安全呼叫”保护您的电话隐私,请放心接听！）', '2050-01-25 08:20:00');
INSERT INTO `t_express` VALUES (18, 1, '快件派送不成功(因电话无人接听/关机/无信号，暂无法联系到收方客户),正在处理中,待再次派送', '2050-01-25 10:01:00');
INSERT INTO `t_express` VALUES (19, 1, '已签收,感谢使用顺丰,期待再次为您服务', '2050-01-25 11:37:00');
INSERT INTO `t_express` VALUES (22, 2, '商品已经下单', '2050-01-20 10:17:21');
INSERT INTO `t_express` VALUES (23, 2, '您的订单开始处理', '2050-01-20 11:27:20');
INSERT INTO `t_express` VALUES (24, 2, '您的订单待配货', '2050-01-22 14:34:07');
INSERT INTO `t_express` VALUES (25, 2, '您的包裹已出库', '2050-01-22 14:34:07');
INSERT INTO `t_express` VALUES (26, 2, '包裹正在等待揽收', '2050-01-22 18:00:29');
INSERT INTO `t_express` VALUES (27, 2, '顺丰速运 已收取快件', '2050-01-23 09:30:00');
INSERT INTO `t_express` VALUES (28, 2, '快件在【上海浦东集收客户营业部】已装车,准备发往 【上海浦东中转场】', '2050-01-23 15:30:00');
INSERT INTO `t_express` VALUES (29, 2, '快件到达 【上海浦东中转场】', '2050-01-23 23:03:00');
INSERT INTO `t_express` VALUES (30, 2, '快件在【上海浦东中转场】已装车,准备发往 【杭州萧山中转场】', '2050-01-24 22:36:00');
INSERT INTO `t_express` VALUES (31, 2, '快件到达 【杭州萧山中转场】', '2050-01-25 16:01:00');
INSERT INTO `t_express` VALUES (32, 2, '快件在【杭州萧山中转场】已装车,准备发往 【广州市天河区集散中心】', '2050-01-25 17:22:00');
INSERT INTO `t_express` VALUES (33, 2, '快件到达 【广州市天河区集散中心】', '2050-01-26 10:38:00');
INSERT INTO `t_express` VALUES (34, 2, '快件在【广州市天河区集散中心】已装车,准备发往 【广州市天河区龙阳路营业点】', '2050-01-26 11:26:00');
INSERT INTO `t_express` VALUES (35, 2, '快件到达 【广州市天河区龙阳路营业点】', '2050-01-26 12:23:00');
INSERT INTO `t_express` VALUES (36, 2, '快件交给李华,正在派送途中（联系电话：13888888888,顺丰已开启“安全呼叫”保护您的电话隐私,请放心接听！）', '2050-01-26 13:20:00');
INSERT INTO `t_express` VALUES (37, 2, '已签收,感谢使用顺丰,期待再次为您服务', '2050-01-26 14:01:00');

-- ----------------------------
-- Table structure for t_menus
-- ----------------------------
DROP TABLE IF EXISTS `t_menus`;
CREATE TABLE `t_menus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `level` int(11) NULL DEFAULT NULL,
  `path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `parent_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `parent_id`(`parent_id`) USING BTREE,
  CONSTRAINT `t_menus_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `t_menus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 54 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_menus
-- ----------------------------
INSERT INTO `t_menus` VALUES (-1, '全部', 0, NULL, NULL);
INSERT INTO `t_menus` VALUES (1, '用户管理', 1, NULL, -1);
INSERT INTO `t_menus` VALUES (2, '权限管理', 1, NULL, -1);
INSERT INTO `t_menus` VALUES (3, '商品管理', 1, NULL, -1);
INSERT INTO `t_menus` VALUES (4, '订单管理', 1, NULL, -1);
INSERT INTO `t_menus` VALUES (5, '数据统计', 1, NULL, -1);
INSERT INTO `t_menus` VALUES (11, '用户列表', 2, '/user_list/', 1);
INSERT INTO `t_menus` VALUES (21, '角色列表', 2, '/role_list/', 2);
INSERT INTO `t_menus` VALUES (22, '权限列表', 2, '/permission_list/', 2);
INSERT INTO `t_menus` VALUES (31, '商品列表', 2, '/product_list/', 3);
INSERT INTO `t_menus` VALUES (32, '分类列表', 2, '/category_list/', 3);
INSERT INTO `t_menus` VALUES (33, '属性列表', 2, '/attribute_list/', 3);
INSERT INTO `t_menus` VALUES (41, '订单列表', 2, '/order_list/', 4);
INSERT INTO `t_menus` VALUES (51, '统计列表', 2, '/statistics_list/', 5);
INSERT INTO `t_menus` VALUES (53, 'SKU管理', 2, '/sku_manage/', 3);

-- ----------------------------
-- Table structure for t_order_details
-- ----------------------------
DROP TABLE IF EXISTS `t_order_details`;
CREATE TABLE `t_order_details`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NULL DEFAULT NULL,
  `product_id` int(11) NULL DEFAULT NULL,
  `number` int(11) NULL DEFAULT NULL,
  `price` float NULL DEFAULT NULL,
  `total_price` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_id`(`order_id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `t_order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `t_orders` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_order_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `t_products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_order_details
-- ----------------------------

-- ----------------------------
-- Table structure for t_orders
-- ----------------------------
DROP TABLE IF EXISTS `t_orders`;
CREATE TABLE `t_orders`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` float NULL DEFAULT NULL,
  `number` int(11) NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `pay_status` int(11) NULL DEFAULT NULL,
  `deliver_status` int(11) NULL DEFAULT NULL,
  `confirm_status` int(11) NULL DEFAULT NULL,
  `confirm_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `t_orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `t_users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_orders
-- ----------------------------
INSERT INTO `t_orders` VALUES (1, 100, 66, NULL, 1, 1, NULL, NULL, 1, NULL, NULL);
INSERT INTO `t_orders` VALUES (2, 400, 66, NULL, 0, 0, NULL, NULL, 7, NULL, NULL);
INSERT INTO `t_orders` VALUES (4, 300, 66, NULL, 1, 1, NULL, NULL, 9, NULL, NULL);

-- ----------------------------
-- Table structure for t_pictures
-- ----------------------------
DROP TABLE IF EXISTS `t_pictures`;
CREATE TABLE `t_pictures`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `product_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `t_pictures_ibfk_1`(`product_id`) USING BTREE,
  CONSTRAINT `t_pictures_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `t_products` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_pictures
-- ----------------------------
INSERT INTO `t_pictures` VALUES (9, '/static/uploads/9f3967549da0cd0b110b43b5e89726bb.png', 14);
INSERT INTO `t_pictures` VALUES (11, '/static/uploads/b596b3ef7928adee32129569d0e5742e.png', 16);
INSERT INTO `t_pictures` VALUES (12, '/static/uploads/55e196815d49abf42a4afa147d7f5f9c.png', 17);
INSERT INTO `t_pictures` VALUES (13, '/static/uploads/f37a233ffc756974a011bbd8d9b695bc.png', 18);
INSERT INTO `t_pictures` VALUES (14, '/static/uploads/d70a6cd6a43212ec33d5e3a0cc4953f2.png', 19);
INSERT INTO `t_pictures` VALUES (15, '/static/uploads/bb468170e06c9bbf3d19f2c47e803589.png', 20);
INSERT INTO `t_pictures` VALUES (16, '/static/uploads/cedd0e9d694c47f134f8590b23b15bc1.png', 21);
INSERT INTO `t_pictures` VALUES (17, '/static/uploads/7177334b2a60789ee90b3408f873325f.png', 22);
INSERT INTO `t_pictures` VALUES (18, '/static/uploads/06bd0575b11c4bdf86a630b9291e6ef4.png', 23);
INSERT INTO `t_pictures` VALUES (20, '/static/uploads/4ec0e39ac92f8acbe3d3eaf97df9ac7d.png', 25);

-- ----------------------------
-- Table structure for t_product_attrs
-- ----------------------------
DROP TABLE IF EXISTS `t_product_attrs`;
CREATE TABLE `t_product_attrs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NULL DEFAULT NULL,
  `attr_id` int(11) NULL DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `_type` enum('static','dynamic') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `attr_id`(`attr_id`) USING BTREE,
  INDEX `t_product_attrs_ibfk_2`(`product_id`) USING BTREE,
  CONSTRAINT `t_product_attrs_ibfk_1` FOREIGN KEY (`attr_id`) REFERENCES `t_attributes` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_product_attrs_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `t_products` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 282 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_product_attrs
-- ----------------------------
INSERT INTO `t_product_attrs` VALUES (5, 14, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (6, 14, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (7, 14, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (8, 14, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (9, 14, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (10, 14, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (11, 14, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (12, 14, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (13, 14, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (14, 14, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (15, 14, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (16, 14, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (17, 14, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (18, 14, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (19, 14, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (20, 14, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (21, 14, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (22, 14, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (23, 14, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (24, 14, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (25, 14, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (26, 14, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (49, 16, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (50, 16, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (51, 16, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (52, 16, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (53, 16, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (54, 16, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (55, 16, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (56, 16, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (57, 16, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (58, 16, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (59, 16, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (60, 16, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (61, 16, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (62, 16, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (63, 16, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (64, 16, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (65, 16, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (66, 16, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (67, 16, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (68, 16, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (69, 16, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (70, 16, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (71, 17, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (72, 17, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (73, 17, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (74, 17, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (75, 17, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (76, 17, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (77, 17, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (78, 17, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (79, 17, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (80, 17, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (81, 17, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (82, 17, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (83, 17, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (84, 17, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (85, 17, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (86, 17, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (87, 17, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (88, 17, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (89, 17, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (90, 17, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (91, 17, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (92, 17, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (93, 18, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (94, 18, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (95, 18, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (96, 18, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (97, 18, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (98, 18, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (99, 18, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (100, 18, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (101, 18, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (102, 18, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (103, 18, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (104, 18, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (105, 18, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (106, 18, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (107, 18, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (108, 18, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (109, 18, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (110, 18, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (111, 18, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (112, 18, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (113, 18, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (114, 18, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (115, 19, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (116, 19, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (117, 19, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (118, 19, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (119, 19, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (120, 19, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (121, 19, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (122, 19, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (123, 19, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (124, 19, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (125, 19, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (126, 19, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (127, 19, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (128, 19, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (129, 19, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (130, 19, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (131, 19, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (132, 19, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (133, 19, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (134, 19, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (135, 19, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (136, 19, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (137, 20, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (138, 20, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (139, 20, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (140, 20, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (141, 20, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (142, 20, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (143, 20, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (144, 20, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (145, 20, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (146, 20, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (147, 20, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (148, 20, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (149, 20, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (150, 20, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (151, 20, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (152, 20, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (153, 20, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (154, 20, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (155, 20, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (156, 20, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (157, 20, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (158, 20, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (159, 21, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (160, 21, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (161, 21, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (162, 21, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (163, 21, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (164, 21, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (165, 21, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (166, 21, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (167, 21, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (168, 21, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (169, 21, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (170, 21, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (171, 21, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (172, 21, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (173, 21, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (174, 21, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (175, 21, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (176, 21, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (177, 21, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (178, 21, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (179, 21, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (180, 21, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (181, 22, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (182, 22, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (183, 22, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (184, 22, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (185, 22, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (186, 22, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (187, 22, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (188, 22, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (189, 22, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (190, 22, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (191, 22, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (192, 22, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (193, 22, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (194, 22, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (195, 22, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (196, 22, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (197, 22, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (198, 22, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (199, 22, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (200, 22, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (201, 22, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (202, 22, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (203, 23, 21, 'S,M,L,XL,XXL,XXXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (204, 23, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (205, 23, 41, '', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (208, 23, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (209, 23, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (210, 23, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (211, 23, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (212, 23, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (213, 23, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (214, 23, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (215, 23, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (216, 23, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (217, 23, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (218, 23, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (219, 23, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (220, 23, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (221, 23, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (222, 23, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (223, 23, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (224, 23, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (225, 23, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (226, 23, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (227, 23, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (255, 25, 21, 'S,M,L,XL,XXL', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (256, 25, 22, '冷艳红梨色-100%桑蚕丝,高雅浅杏-100%桑蚕丝,高雅浅杏-100%桑蚕丝-36517批次,冷艳红梨色-100%桑蚕丝-预售,高雅浅杏-100%桑蚕丝-预售,无视洗涤说明概不负责', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (257, 25, 41, '', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (258, 25, 48, '', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (259, 25, 49, '', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (260, 25, 50, '红色,蓝色,绿色', 'dynamic');
INSERT INTO `t_product_attrs` VALUES (261, 25, 1, 'soulkiss', 'static');
INSERT INTO `t_product_attrs` VALUES (262, 25, 2, '25-29周岁', 'static');
INSERT INTO `t_product_attrs` VALUES (263, 25, 3, '蚕丝', 'static');
INSERT INTO `t_product_attrs` VALUES (264, 25, 4, 'S M L', 'static');
INSERT INTO `t_product_attrs` VALUES (265, 25, 5, '其他', 'static');
INSERT INTO `t_product_attrs` VALUES (266, 25, 6, '纯色', 'static');
INSERT INTO `t_product_attrs` VALUES (267, 25, 7, '通勤', 'static');
INSERT INTO `t_product_attrs` VALUES (268, 25, 8, '简约', 'static');
INSERT INTO `t_product_attrs` VALUES (269, 25, 9, '立领', 'static');
INSERT INTO `t_product_attrs` VALUES (270, 25, 10, '单排扣', 'static');
INSERT INTO `t_product_attrs` VALUES (271, 25, 11, '冷艳红梨色-100%桑蚕丝 高雅浅杏-100%桑蚕丝 高雅浅杏-100%桑蚕丝-36517批次 冷艳红梨色-100%桑蚕丝-预售 高雅浅杏-100%桑蚕丝-预售 无视洗涤说明概不负责', 'static');
INSERT INTO `t_product_attrs` VALUES (272, 25, 12, '单件', 'static');
INSERT INTO `t_product_attrs` VALUES (273, 25, 13, 'S904548', 'static');
INSERT INTO `t_product_attrs` VALUES (274, 25, 14, '95%以上', 'static');
INSERT INTO `t_product_attrs` VALUES (275, 25, 15, 'A字裙', 'static');
INSERT INTO `t_product_attrs` VALUES (276, 25, 16, '2019年夏季', 'static');
INSERT INTO `t_product_attrs` VALUES (277, 25, 17, '无袖', 'static');
INSERT INTO `t_product_attrs` VALUES (278, 25, 18, '中长裙', 'static');
INSERT INTO `t_product_attrs` VALUES (279, 25, 19, '其他/other', 'static');
INSERT INTO `t_product_attrs` VALUES (280, 25, 20, 'A型', 'static');
INSERT INTO `t_product_attrs` VALUES (281, 25, 47, '红色，黄色', 'static');

-- ----------------------------
-- Table structure for t_products
-- ----------------------------
DROP TABLE IF EXISTS `t_products`;
CREATE TABLE `t_products`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` float NULL DEFAULT NULL,
  `number` int(11) NULL DEFAULT NULL,
  `introduce` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `big_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `small_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `state` int(11) NULL DEFAULT NULL,
  `is_promote` int(11) NULL DEFAULT NULL,
  `hot_number` int(11) NULL DEFAULT NULL,
  `weight` int(11) NULL DEFAULT NULL,
  `cid_one` int(11) NULL DEFAULT NULL,
  `cid_two` int(11) NULL DEFAULT NULL,
  `cid_three` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cid_one`(`cid_one`) USING BTREE,
  INDEX `cid_three`(`cid_three`) USING BTREE,
  INDEX `cid_two`(`cid_two`) USING BTREE,
  CONSTRAINT `t_products_ibfk_1` FOREIGN KEY (`cid_one`) REFERENCES `t_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_products_ibfk_2` FOREIGN KEY (`cid_three`) REFERENCES `t_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_products_ibfk_3` FOREIGN KEY (`cid_two`) REFERENCES `t_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_products
-- ----------------------------
INSERT INTO `t_products` VALUES (1, 'SOULKISS 高冷气质硬核款 16姆米桑蚕真丝双绉显瘦挂脖露肩连衣裙', 879.99, 100, 'chanpin', '', '', 2, 1, 30, 100, 1, 17, 65);
INSERT INTO `t_products` VALUES (2, 'AmandaX定制重磅奢华真丝提花连肩袖小A连衣裙', 879.99, 100, 'chanpin', '', '', 1, 1, 30, 100, 1, 17, 65);
INSERT INTO `t_products` VALUES (3, 'AmandaX定制30姆米2色重缎可调节V领吊带连衣裙', 1380, 100, 'chanpin', '', '', 2, 1, 30, 100, 1, 17, 65);
INSERT INTO `t_products` VALUES (4, '吊带连衣裙女2020夏季新款V领雪纺气质印花A字复古小碎花过膝长裙', 359, 100, 'chanpin', '', '', -1, 1, 30, 100, 1, 17, 65);
INSERT INTO `t_products` VALUES (10, '测试商品1', 199, 100, '这是一件测试商品', NULL, NULL, 0, NULL, NULL, 10, 1, 17, 65);
INSERT INTO `t_products` VALUES (11, '测试商品2', 12, 15, '这是一件测试商品', NULL, NULL, -1, NULL, NULL, 10, 1, 17, 65);
INSERT INTO `t_products` VALUES (12, '测试商品1', 199, 100, '这是一件测试商品', NULL, NULL, NULL, NULL, NULL, 10, 1, 17, 65);
INSERT INTO `t_products` VALUES (14, 'm6', 1, 2, '<p>info1233</p>', NULL, NULL, 1, NULL, NULL, 3, 1, 17, 65);
INSERT INTO `t_products` VALUES (16, 'm3', 1, 2, '<p>增加3</p>', NULL, NULL, NULL, NULL, NULL, 3, 1, 17, 65);
INSERT INTO `t_products` VALUES (17, 'm4', 1, 2, '<p>哈哈哈</p>', NULL, NULL, NULL, NULL, NULL, 3, 1, 17, 65);
INSERT INTO `t_products` VALUES (18, 'm5', 1, 2, '<p>asd</p>', NULL, NULL, NULL, NULL, NULL, 3, 1, 17, 65);
INSERT INTO `t_products` VALUES (19, '柠檬', 12, 23, '<p>q</p>', NULL, NULL, 1, NULL, NULL, 3, 1, 17, 65);
INSERT INTO `t_products` VALUES (20, 'm9', 12, 3, '<p>q</p>', NULL, NULL, NULL, NULL, NULL, 4, 1, 17, 65);
INSERT INTO `t_products` VALUES (21, 'mpower', 1, 2, '<p>123</p>', NULL, NULL, -1, NULL, NULL, 3, 1, 17, 65);
INSERT INTO `t_products` VALUES (22, '超级大西瓜', 15, 25, '<p>阿德飒飒</p>', NULL, NULL, 1, NULL, NULL, 12, 1, 17, 65);
INSERT INTO `t_products` VALUES (23, '超级火龙果', 199, 100, '<p>请</p>', NULL, NULL, 0, NULL, NULL, 1, 1, 17, 65);
INSERT INTO `t_products` VALUES (25, 'sss', 23, 12, '', NULL, NULL, NULL, NULL, NULL, 12, 1, 17, 65);

-- ----------------------------
-- Table structure for t_roles
-- ----------------------------
DROP TABLE IF EXISTS `t_roles`;
CREATE TABLE `t_roles`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `desc` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_roles
-- ----------------------------
INSERT INTO `t_roles` VALUES (1, 'sroot', '系统管理员');
INSERT INTO `t_roles` VALUES (2, 'admin', '管理员');
INSERT INTO `t_roles` VALUES (3, 'vip', 'VIP会员');
INSERT INTO `t_roles` VALUES (4, 'user', '普通用户');
INSERT INTO `t_roles` VALUES (5, 'guest', '游客');

-- ----------------------------
-- Table structure for t_roles_menus
-- ----------------------------
DROP TABLE IF EXISTS `t_roles_menus`;
CREATE TABLE `t_roles_menus`  (
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  PRIMARY KEY (`role_id`, `menu_id`) USING BTREE,
  INDEX `menu_id`(`menu_id`) USING BTREE,
  CONSTRAINT `t_roles_menus_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `t_menus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_roles_menus_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `t_roles` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_roles_menus
-- ----------------------------
INSERT INTO `t_roles_menus` VALUES (1, 1);
INSERT INTO `t_roles_menus` VALUES (2, 1);
INSERT INTO `t_roles_menus` VALUES (3, 1);
INSERT INTO `t_roles_menus` VALUES (5, 1);
INSERT INTO `t_roles_menus` VALUES (1, 2);
INSERT INTO `t_roles_menus` VALUES (3, 2);
INSERT INTO `t_roles_menus` VALUES (5, 2);
INSERT INTO `t_roles_menus` VALUES (1, 3);
INSERT INTO `t_roles_menus` VALUES (2, 3);
INSERT INTO `t_roles_menus` VALUES (3, 3);
INSERT INTO `t_roles_menus` VALUES (1, 4);
INSERT INTO `t_roles_menus` VALUES (1, 5);
INSERT INTO `t_roles_menus` VALUES (1, 11);
INSERT INTO `t_roles_menus` VALUES (3, 11);
INSERT INTO `t_roles_menus` VALUES (5, 11);
INSERT INTO `t_roles_menus` VALUES (1, 21);
INSERT INTO `t_roles_menus` VALUES (3, 21);
INSERT INTO `t_roles_menus` VALUES (5, 21);
INSERT INTO `t_roles_menus` VALUES (1, 22);
INSERT INTO `t_roles_menus` VALUES (5, 22);
INSERT INTO `t_roles_menus` VALUES (1, 31);
INSERT INTO `t_roles_menus` VALUES (2, 31);
INSERT INTO `t_roles_menus` VALUES (1, 32);
INSERT INTO `t_roles_menus` VALUES (2, 32);
INSERT INTO `t_roles_menus` VALUES (1, 33);
INSERT INTO `t_roles_menus` VALUES (1, 41);
INSERT INTO `t_roles_menus` VALUES (1, 51);
INSERT INTO `t_roles_menus` VALUES (1, 53);

-- ----------------------------
-- Table structure for t_skus
-- ----------------------------
DROP TABLE IF EXISTS `t_skus`;
CREATE TABLE `t_skus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NULL DEFAULT NULL,
  `sku_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `specifications` json NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `stock` int(11) NULL DEFAULT NULL,
  `sales` int(11) NULL DEFAULT 0,
  `status` int(11) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `sku_code`(`sku_code`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  CONSTRAINT `t_skus_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `t_products` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_skus
-- ----------------------------
INSERT INTO `t_skus` VALUES (1, 1, 'SKU-001', '{\"尺码\": \"S\", \"颜色\": \"红色\"}', 199.99, 100, 20, 1, '2024-12-25 11:38:14', '2024-12-25 11:38:14');
INSERT INTO `t_skus` VALUES (2, 1, 'SKU-002', '{\"尺码\": \"M\", \"颜色\": \"红色\"}', 199.99, 150, 30, 1, '2024-12-25 11:38:14', '2024-12-25 11:38:14');
INSERT INTO `t_skus` VALUES (3, 1, 'SKU-003', '{\"尺码\": \"L\", \"颜色\": \"红色\"}', 199.99, 80, 15, 1, '2024-12-25 11:38:14', '2024-12-25 11:38:14');
INSERT INTO `t_skus` VALUES (4, 1, 'SKU-004', '{\"尺码\": \"S\", \"颜色\": \"蓝色\"}', 199.99, 120, 25, 1, '2024-12-25 11:38:14', '2024-12-25 11:38:14');
INSERT INTO `t_skus` VALUES (5, 1, 'SKU-005', '{\"尺码\": \"M\", \"颜色\": \"蓝色\"}', 222.00, 90, 40, 1, '2024-12-25 11:38:14', '2024-12-25 11:40:14');
INSERT INTO `t_skus` VALUES (6, 1, 'SKU-006', '{\"尺码\": \"L\", \"颜色\": \"蓝色\"}', 199.99, 72, 10, 1, '2024-12-25 11:38:14', '2024-12-25 12:19:13');

-- ----------------------------
-- Table structure for t_spec_templates
-- ----------------------------
DROP TABLE IF EXISTS `t_spec_templates`;
CREATE TABLE `t_spec_templates`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `category_id` int(11) NULL DEFAULT NULL,
  `specs` json NULL,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id`) USING BTREE,
  CONSTRAINT `t_spec_templates_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `t_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_spec_templates
-- ----------------------------
INSERT INTO `t_spec_templates` VALUES (1, '服装规格', 65, '{\"尺码\": [\"S\", \"M\", \"L\", \"XL\", \"XXL\"], \"颜色\": [\"红色\", \"蓝色\", \"黑色\", \"白色\"]}', '2024-12-25 11:38:15', '2024-12-25 11:38:15');
INSERT INTO `t_spec_templates` VALUES (2, '鞋靴规格', 84, '{\"鞋码\": [\"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\"], \"颜色\": [\"黑色\", \"白色\", \"棕色\"]}', '2024-12-25 11:38:15', '2024-12-25 11:38:15');
INSERT INTO `t_spec_templates` VALUES (3, '手机规格', 28, '{\"内存\": [\"4GB\", \"6GB\", \"8GB\"], \"存储\": [\"64GB\", \"128GB\", \"256GB\"], \"颜色\": [\"黑色\", \"白色\", \"金色\"]}', '2024-12-25 11:38:15', '2024-12-25 11:38:15');

-- ----------------------------
-- Table structure for t_stock_logs
-- ----------------------------
DROP TABLE IF EXISTS `t_stock_logs`;
CREATE TABLE `t_stock_logs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sku_id` int(11) NULL DEFAULT NULL,
  `change_amount` int(11) NULL DEFAULT NULL,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `operator` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `t_stock_logs_ibfk_1`(`sku_id`) USING BTREE,
  CONSTRAINT `t_stock_logs_ibfk_1` FOREIGN KEY (`sku_id`) REFERENCES `t_skus` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_stock_logs
-- ----------------------------
INSERT INTO `t_stock_logs` VALUES (1, 1, -10, 'sale', 'system', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (2, 1, 50, 'restock', 'admin', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (3, 2, -5, 'sale', 'system', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (4, 2, 30, 'restock', 'admin', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (5, 3, -8, 'sale', 'system', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (6, 4, -12, 'sale', 'system', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (7, 5, -15, 'sale', 'system', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (8, 6, -5, 'sale', 'system', '2024-12-25 11:38:16');
INSERT INTO `t_stock_logs` VALUES (9, 5, 0, 'manual', 'unknown', '2024-12-25 11:39:58');
INSERT INTO `t_stock_logs` VALUES (10, 5, 0, 'manual', 'unknown', '2024-12-25 11:40:14');
INSERT INTO `t_stock_logs` VALUES (11, 6, 2, 'manual', 'unknown', '2024-12-25 12:19:13');

-- ----------------------------
-- Table structure for t_users
-- ----------------------------
DROP TABLE IF EXISTS `t_users`;
CREATE TABLE `t_users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pwd` varchar(800) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `nick_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  `last_login` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  INDEX `t_users_ibfk_1`(`role_id`) USING BTREE,
  CONSTRAINT `t_users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `t_roles` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_users
-- ----------------------------
INSERT INTO `t_users` VALUES (1, 'baizhan', 'pbkdf2:sha256:1000000$ZXusoCN5cQJClDry$f01e4e1f5c965f8a63bbcf979c81f9b7c5aaaf63f1b8f3c4285017a1642570ae', '西施', '15658475666', '321@qq.com', '2024-11-02 21:45:34', '2024-12-25 20:33:11', 2, '2024-12-25 20:30:24');
INSERT INTO `t_users` VALUES (7, 'sxt', 'pbkdf2:sha256:1000000$MeKBN04q4tfCKFDR$c9f1cd37b4ea16da033e78a1f4f5d55ec1f2644beb542613a035148ee9c258ce', '貂蝉', '13654896571', '121@123.com', '2024-11-10 14:59:46', '2024-12-09 22:36:57', 2, NULL);
INSERT INTO `t_users` VALUES (9, '刘备', 'pbkdf2:sha256:1000000$mVk8ekP2Ap3218P9$0a168c5bdf7bcf38eabb59522f689b42e0f4718129a9ee34778d2029cef945cf', '玄德', '13365478512', '12365@qq.com', '2024-11-11 12:36:30', '2024-11-11 12:36:30', 4, NULL);
INSERT INTO `t_users` VALUES (11, '孙悟空', 'pbkdf2:sha256:1000000$qWXdI2QNv1saikr0$bf5e3cfaba9b4afcc14afacd09e02e01c5f45d629a38ead543e1e0c914ef5413', '齐天大圣', '18236547851', '225@qq.com', '2024-11-11 12:46:27', '2024-12-25 17:26:38', 1, '2024-12-25 17:26:38');
INSERT INTO `t_users` VALUES (12, '李白', 'pbkdf2:sha256:1000000$ZqtXlsFtJsiFgApQ$773ecab328bb43e4703a56a0a5744c80680132eb62b0d06c77a5ef7005bd2d3d', '诗仙', '15896585478', '12@qq.com', '2024-11-11 12:49:58', '2024-11-11 12:49:58', 2, NULL);
INSERT INTO `t_users` VALUES (14, '亚索', 'pbkdf2:sha256:1000000$29IrgFYr99VBYqng$9512fa8aba3d9516646b7e6ac97d5ed75c3ad2faa682c872616139925978512a', '疾风', '13369875896', '234@qq.com', '2024-11-14 11:48:06', '2024-11-14 11:48:06', 4, NULL);
INSERT INTO `t_users` VALUES (18, '袁绍', 'pbkdf2:sha256:1000000$4xQllBftxD3ItnWa$5bce55a6cf8d3010892e87cb7c4a13b831724b97953ff7173ea52d0ea7a0e616', '本初', '13365478564', '1234@qq.com', '2024-12-09 22:09:36', '2024-12-09 22:09:36', 1, NULL);
INSERT INTO `t_users` VALUES (19, '西瓜', 'pbkdf2:sha256:1000000$axekwOKvZuqXAzer$675f6b530a997d37d1c9569e5c6a3dfc288b98a0af2a7a60b4e4399007a8445f', 'water', '13365478542', '11112@qq.com', '2024-12-11 05:54:36', '2024-12-11 05:54:36', 1, NULL);

SET FOREIGN_KEY_CHECKS = 1;
