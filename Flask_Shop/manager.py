

from flask_migrate import Migrate
from flask_shop import create_app,db
from flask_cors import CORS
app = create_app('development')


CORS(app, supports_credentials=True) # 解决跨域问题


 #创建同步数据库对象,$env:Flask_app="manager.py"
migrate = Migrate(app, db)#传递app和数据库对象,创建完数据库后就进行三步命令：flask db init,flask db migrate -m '',flask db upgrade


if __name__ == '__main__':
    app.run()

