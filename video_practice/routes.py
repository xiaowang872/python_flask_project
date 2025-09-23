from flask import Blueprint ,current_app,request, render_template,Flask,flash,redirect,url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import random  

# UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
# 在函数内部使用 current_app

# UPLOAD_FOLDER = 'video_practice/uploads/videos'
#创建一个视频蓝图
video_bp = Blueprint(
    'video', __name__,            # 蓝图名称
    template_folder='templates',  # 指定模板文件夹
    static_folder='static'         # 指定静态文件夹
)
# UPLOAD_FOLDER = 'video_practice/uploads/videos'  # 设置上传文件的保存路径

# 允许上传的视频格式
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'rmvb', '3gp', 'mpg', 'mpeg', 'm4v', 'webm', 'ogg', 'ts', 'm2ts', 'mkv', 'mts', 'm2v', 'm4v', 'm4p', 'm4b', 'm4r', 'm4a', 'm4s', 'm4e',}
# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_file_size(size_bytes):
    """格式化文件大小（字节 → KB/MB/GB）"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
def format_file_time(timestamp):
    """格式化文件时间（时间戳 → 年月日 时分秒）"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_uploaded_videos():
    """获取已上传的视频信息"""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    upload_videos = []
    video_id = 1 # 简单的ID生成
    # 确保上传目录存在
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
        return None # 他会返回一个空的列表
    # ####################################
    print(f"=== 获取上传视频列表 ===")
    print(f"上传目录: {upload_folder}")
    print(f"目录是否存在: {os.path.exists(upload_folder)}")
    files_tmp = os.listdir(upload_folder)
    print(f"目录中的文件: {files_tmp}")
    #####################################
    # 遍历目录下的文件
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path) and allowed_file(filename):
            file_stat = os.stat(file_path)
            file_size = format_file_size(file_stat.st_size)
            upload_time = format_file_time(file_stat.st_mtime)
            # 生成视频标题，去掉后缀名
            video_title = os.path.splitext(filename)[0]
            video_url = f"/uploads/videos/{filename}"  # 格式：/uploads/videos/xxx.mp4
            # 添加到动态列表
            upload_videos.append({
                'id': video_id,
                'title': video_title,
                'file_name': filename,  # 原始文件名
                'url': video_url,
                'size': file_size,
                'upload_time': upload_time,
                'file_path': file_path,
            })
            video_id += 1
    ##########################
    print(f"总共找到 {len(upload_videos)} 个视频文件")
    ################################
    return upload_videos
# 视频首页
@video_bp.route('/', endpoint = 'video_index')
def video():
        uploaded_videos = get_uploaded_videos()
        if not uploaded_videos:
            videos = [
                {'id': 1, 'title': 'Flask入门教程', 'url': 'https://example.com/video1.mp4','duration': '10:00'},
                {'id': 2, 'title': 'SQLAlchemy基础', 'url': 'https://example.com/video2.mp4','duration': '15:30'},
                {'id': 3, 'title': '前端与后端交互', 'url': 'https://example.com/video3.mp4','duration': '12:45'},
            ]
        else:
            videos = []
            for video in uploaded_videos:
                videos.append({
                    'id': video['id'],
                    'title': video['title'],
                    'url': video['url'],
                    'duration': '时长待计算'  # 这里可以添加实际时长计算逻辑,
                })
    # "把 videos 数据传递给 templates/video/index.html 模板，渲染后返回给浏览器显示"。
        return render_template('video/index.html', videos=videos)

# 视频详情页
@video_bp.route('/play/<int:video_id>')
def play_video(video_id):
    upload_videos = get_uploaded_videos()
    # 根据 video_id 查找对应的视频信息
    target_video = None
    for _ in upload_videos:
        if _['id'] == video_id:
            target_video = _
            break

    if not target_video:
        # 如果没有找到对应的视频，返回404页面
        return "视频未找到", 404
    video_info = {
        'id': target_video['id'],
        'title': target_video['title'],
        'description': f'上传时间: {target_video["upload_time"]}, 大小: {target_video["size"]}',
        'url': f"/uploads/videos/{target_video['file_name']}", # 匹配 /uploads/videos/xxx.mp4
        'filename': target_video['file_name'],
        'upload_time': target_video['upload_time'],
        'size': target_video['size'],

    }
    return render_template('video/play.html', video=video_info)


# 视频上传页
@video_bp.route('/upload', methods=['GET', 'POST'])
def video_upload():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    print(f"=== 上传请求开始 ===")
    print(f"请求方法: {request.method}")
    if request.method == 'POST':
        # 处理视频上传逻辑
        if 'video_file' not in request.files:
            print("没有找到video_file字段")
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        video_file = request.files['video_file']
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        # 验证输入
        if not title:
            flash('请输入视频标题', 'error')
            return redirect(request.url)
        
        if video_file.filename == '':
            flash('请选择视频文件', 'error')
            return redirect(request.url)
        
        # 验证文件类型
        if not allowed_file(video_file.filename):
            flash('不支持的文件格式。请上传MP4, AVI, MOV, WMV, FLV, WEBM或MKV格式的视频。', 'error')
            return redirect(request.url)
        try:
            # 生成安全的文件名
            original_filename = secure_filename(video_file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            
            # 创建唯一文件名（时间戳+随机数）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            import random
            random_str = str(random.randint(1000, 9999))
            unique_filename = f"video_{timestamp}_{random_str}.{file_extension}"
            
            # 确保上传目录存在
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)

            # 保存文件
            video_file.save(file_path)
            
            # 这里可以添加数据库操作
            # save_video_to_db(title, description, unique_filename, file_path)
            print(f"文件保存成功: {file_path}")
            flash(f'视频 "{title}" 上传成功！', 'success')
            print("准备重定向到首页")
            return redirect(url_for('video.video_index'))
            
        except Exception as e:
            print(f"上传出错: {str(e)}")
            flash(f'文件上传失败: {str(e)}', 'error')
            return redirect(request.url)
    
    # GET请求，显示上传表单
    print("GET请求，显示上传表单")
    return render_template('video/upload.html')
@video_bp.route('/manage')
def manage_videos():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    """视频管理页面"""
    # 这里可以从数据库获取用户上传的视频列表
    # uploaded_videos = [
    #     {'id': 1, 'title': '我的视频1', 'upload_date': '2024-01-15', 'size': '150MB'},
    #     {'id': 2, 'title': '我的视频2', 'upload_date': '2024-01-16', 'size': '250MB'}
    # ]
    # return render_template('video/manage.html', videos=uploaded_videos)
    # 从上传目录读取视频文件列表
    # 视频管理页面，动态读取 UPLOAD_FOLDER 目录下的所有视频文件
    upload_videos = []
    video_id = 1 # 简单的ID生成
    # 确保上传目录存在
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
        return render_template('video/manage.html', videos=upload_videos)# 他会返回一个空的列表

    # 遍历目录下的文件
    for filename in os.listdir(upload_folder):
    # 拼接完整路径
        file_path = os.path.join(upload_folder,filename)
        #筛选出文件
        if os.path.isfile(file_path) and allowed_file(filename):
            file_stat = os.stat(file_path)
            file_size = format_file_size(file_stat.st_size)
            upload_time = format_file_time(file_stat.st_mtime)

            # 生成视频标题，去掉后缀名
            video_title = os.path.splitext(filename)[0]

            # 添加到动态列表
            upload_videos.append({
                'id': video_id,
                'title': video_title,
                'file_name': filename,  # 原始文件名
                'upload_time': upload_time,
                'size': file_size,
                'file_path': file_path
            })
            video_id += 1
    # 7. 传递动态列表给模板
    return render_template('video/manage.html', videos=upload_videos)

        

# 视频删除
@video_bp.route('/delete/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    """删除视频"""
    # 这里应该添加删除逻辑
    # 1. 从数据库删除视频记录
    # 2. 从文件系统删除视频文件
    uploaded_videos = []
    target_video = None  # 存储要删除的视频信息
    if os.path.exists(upload_folder):
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path) and allowed_file(filename):
                uploaded_videos.append({
                    'id': len(uploaded_videos) + 1,
                    'filename': filename,
                    'file_path': file_path
                })
    # 根据id找到视频
    for video in uploaded_videos:
        if video['id'] == video_id:
            target_video = video
            break
    # 执行删除操作
    if target_video:
        try:
            # 文件系统中的文件
            os.remove(target_video['file_path'])
            flash(f'视频 {video_id} 已删除: {target_video["filename"]}', 'success')
        except Exception as e:
            flash(f'删除视频 {video_id} 失败: {str(e)}', 'error')
    else:
        flash(f'未找到ID为 {video_id} 的视频', 'error')
    # 重定向回视频管理页面
    return redirect(url_for('video.manage_videos'))

# 辅助函数：保存视频信息到数据库（示例）
def save_video_to_db(title, description, filename, file_path):
    """
    将视频信息保存到数据库
    """
    # 这里应该是数据库操作代码
    # 例如使用SQLAlchemy:
    """
    from models import Video, db
    
    video = Video(
        title=title,
        description=description,
        filename=filename,
        file_path=file_path,
        upload_date=datetime.now(),
        size=os.path.getsize(file_path)
    )
    db.session.add(video)
    db.session.commit()
    """
    pass

# 辅助函数：获取文件大小格式
def get_file_size(file_path):
    """获取文件大小（格式化输出）"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"





