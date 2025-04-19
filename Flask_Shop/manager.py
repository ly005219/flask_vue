from flask_migrate import Migrate
from flask_shop import create_app, db

app = create_app('development')

# 不要重复配置CORS，create_app中已经配置过了
# CORS(app, supports_credentials=True) # 这行删除，避免CORS配置冲突

# 创建同步数据库对象
migrate = Migrate(app, db)  # 传递app和数据库对象

if __name__ == '__main__':
    # 设置host为0.0.0.0允许外部访问，并使用debug模式方便开发
    app.run(host='0.0.0.0', debug=True)

