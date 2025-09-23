
function updateFileInfo() {
    const fileInput = document.getElementById('video_file');
    const fileInfo = document.getElementById('fileInfo');
    
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const fileSize = (file.size / (1024 * 1024)).toFixed(2);
        fileInfo.textContent = `已选择: ${file.name} | 大小: ${fileSize} MB | 类型: ${file.type}`;
    } else {
        fileInfo.textContent = '请选择视频文件 | 支持格式: MP4, AVI, MOV, WMV, FLV, WEBM, MKV | 最大大小: 500MB';
    }
}

// 表单验证
document.querySelector('form').addEventListener('submit', function(e) {
    const title = document.getElementById('title').value.trim();
    const file = document.getElementById('video_file').files[0];
    
    if (!title) {
        e.preventDefault();
        alert('请输入视频标题');
        return false;
    }
    
    if (!file) {
        e.preventDefault();
        alert('请选择视频文件');
        return false;
    }
    
    // 文件大小检查
    const maxSize = 500 * 1024 * 1024; // 500MB
    if (file.size > maxSize) {
        e.preventDefault();
        alert('文件大小超过500MB限制');
        return false;
    }
});
