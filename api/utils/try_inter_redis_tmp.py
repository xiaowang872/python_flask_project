import redis
try:
    # 创建一个Redis连接
    r = redis.Redis(
        host='192.168.117.200',
        port=6379,
        password='1234567890',
        decode_responses=True #自动解码返回为字符串

    )
    # 测试连接
    response = r.ping()
    print(f"Redis连接成功: {response}")

    # 测试基本操作
    r.set('name', 'John')
    value = r.get('name')
    print(f"获取的name值为: {value}")

    # 获取服务器信息
    info = r.info()
    print(f"Redis服务器信息: {info}")
    print(f"Redis版本: {info['redis_version']}")


except Exception as e:
    print(f"连接失败，发生错误: {str(e)}")