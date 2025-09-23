import requests
import time

def test_routes():
    base_url = "http://127.0.0.1:5000"
    routes = [
        "/add",        # 先添加测试数据
        "/query1",     # 查询所有用户
        "/query2",     # 主键查询ID=3的用户
        "/query3",     # 查询第一条数据
        "/query4",     # 条件查询：signature='理想'
        "/query5"      # filter_by查询：signature='信念'
    ]
    
    results = []
    
    for route in routes:
        try:
            url = base_url + route
            print(f"正在访问: {url}")
            
            # 发送请求
            response = requests.get(url)
            
            # 记录结果
            result = {
                'route': route,
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            results.append(result)
            print(f"  状态码: {response.status_code}")
            
            # 添加延迟，避免请求过快
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            error_result = {
                'route': route,
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            results.append(error_result)
            print(f"  错误: {e}")
    
    return results

def save_to_file(results, filename="abc.txt"):
    """将结果保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Flask路由测试结果\n")
        f.write("=" * 50 + "\n\n")
        
        for result in results:
            f.write(f"路由: {result['route']}\n")
            f.write(f"时间: {result['timestamp']}\n")
            
            if 'status_code' in result:
                f.write(f"状态码: {result['status_code']}\n")
                
                if result['status_code'] == 200:
                    f.write("响应数据:\n")
                    # 格式化JSON输出
                    if isinstance(result['response'], dict):
                        for key, value in result['response'].items():
                            if isinstance(value, list):
                                f.write(f"  {key}: \n")
                                for item in value:
                                    f.write(f"    {item}\n")
                            else:
                                f.write(f"  {key}: {value}\n")
                    else:
                        f.write(f"  {result['response']}\n")
                else:
                    f.write(f"响应: {result['response']}\n")
            else:
                f.write(f"错误: {result['error']}\n")
            
            f.write("-" * 30 + "\n\n")
    
    print(f"结果已保存到 {filename}")

if __name__ == "__main__":
    print("开始测试Flask路由...")
    print("=" * 40)
    
    # 运行测试
    test_results = test_routes()
    
    # 保存结果到文件
    save_to_file(test_results)
    
    print("测试完成！")