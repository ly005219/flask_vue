insert into t_orders (user_id,price,number,pay_status,deliver_status) value (1,100,66,1,1);
insert into t_orders (user_id,price,number,pay_status,deliver_status) value (7,400,66,1,1);
insert into t_orders (user_id,price,number,pay_status,deliver_status) value (8,200,66,1,1);
insert into t_orders (user_id,price,number,pay_status,deliver_status) value (9,300,66,1,1);


insert into  t_express(order_id,update_time,content) value (1,'2050-01-19 12:17:21','商品已经下单');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-19 12:27:20','您的订单开始处理');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-21 16:34:07','您的订单待配货');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-21 16:34:07','您的包裹已出库');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-21 19:00:29','包裹正在等待揽收');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-22 15:30:00','顺丰速运 已收取快件');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-23  5:30:00','快件在【金华婺城集收客户营业部】已装车,准备发往 【金华金东中转场】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-23 20:03:00','快件到达 【金华金东中转场】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-23 22:36:00','快件在【金华金东中转场】已装车,准备发往 【北京首都机场集散中心2】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-24 16:01:00','快件到达 【北京首都机场集散中心2】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-24 16:22:00','快件在【北京首都机场集散中心2】已装车,准备发往 【石家庄高开集散中心】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 03:14:00','快件到达 【石家庄高开集散中心】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 06:14:00','快件在【石家庄高开集散中心】已装车,准备发往 【衡水桃城集散点】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 13:38:00','快件到达 【衡水桃城集散点】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-26 06:26:00','快件在【衡水桃城集散点】已装车,准备发往 【衡水市桃城区肖家屯新村营业点】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 07:23:00','快件到达 【衡水市桃城区肖家屯新村营业点】');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 08:20:00','快件交给潘君策,正在派送途中（联系电话：13788888888,顺丰已开启“安全呼叫”保护您的电话隐私,请放心接听！）');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 10:01:00','快件派送不成功(因电话无人接听/关机/无信号，暂无法联系到收方客户),正在处理中,待再次派送');
insert into  t_express(order_id,update_time,content) value (1,'2050-01-25 11:37:00','已签收,感谢使用顺丰,期待再次为您服务');




-- 给用户7生成数据
insert into t_express(order_id,update_time,content) value (2,'2050-01-20 10:17:21','商品已经下单');
insert into t_express(order_id,update_time,content) value (2,'2050-01-20 11:27:20','您的订单开始处理');
insert into t_express(order_id,update_time,content) value (2,'2050-01-22 14:34:07','您的订单待配货');
insert into t_express(order_id,update_time,content) value (2,'2050-01-22 14:34:07','您的包裹已出库');
insert into t_express(order_id,update_time,content) value (2,'2050-01-22 18:00:29','包裹正在等待揽收');
insert into t_express(order_id,update_time,content) value (2,'2050-01-23 09:30:00','顺丰速运 已收取快件');
insert into t_express(order_id,update_time,content) value (2,'2050-01-23 15:30:00','快件在【上海浦东集收客户营业部】已装车,准备发往 【上海浦东中转场】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-23 23:03:00','快件到达 【上海浦东中转场】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-24 22:36:00','快件在【上海浦东中转场】已装车,准备发往 【杭州萧山中转场】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-25 16:01:00','快件到达 【杭州萧山中转场】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-25 17:22:00','快件在【杭州萧山中转场】已装车,准备发往 【广州市天河区集散中心】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-26 10:38:00','快件到达 【广州市天河区集散中心】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-26 11:26:00','快件在【广州市天河区集散中心】已装车,准备发往 【广州市天河区龙阳路营业点】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-26 12:23:00','快件到达 【广州市天河区龙阳路营业点】');
insert into t_express(order_id,update_time,content) value (2,'2050-01-26 13:20:00','快件交给李华,正在派送途中（联系电话：13888888888,顺丰已开启“安全呼叫”保护您的电话隐私,请放心接听！）');
insert into t_express(order_id,update_time,content) value (2,'2050-01-26 14:01:00','已签收,感谢使用顺丰,期待再次为您服务');

