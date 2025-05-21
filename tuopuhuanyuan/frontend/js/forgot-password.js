document.addEventListener('DOMContentLoaded', function() {
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    let currentCaptcha = '';

        // 生成随机验证码
        function generateCaptcha() {
            const chars = '2345678abcdefhijkmnpqrstuvwxyzABCDEFGHJKLMNPQRTUVWXY';
            const length = 4;
            let code = '';
            for (let i = 0; i < length; i++) {
                code += chars[Math.floor(Math.random() * chars.length)];
            }
            currentCaptcha = code;
            return code;
        }
    
        // 创建验证码图片
        function createCaptchaImage() {
            const canvas = document.createElement('canvas');
            canvas.width = 100;
            canvas.height = 38;
            const ctx = canvas.getContext('2d');
    
            // 设置背景色
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
    
            // 添加干扰线
            for (let i = 0; i < 5; i++) {
                ctx.strokeStyle = `rgb(${Math.random() * 50 + 150}, ${Math.random() * 50 + 150}, ${Math.random() * 50 + 150})`;
                ctx.beginPath();
                ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
                ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
                ctx.stroke();
            }
    
            // 添加干扰点
            for (let i = 0; i < 100; i++) {
                ctx.fillStyle = `rgb(${Math.random() * 50 + 150}, ${Math.random() * 50 + 150}, ${Math.random() * 50 + 150})`;
                ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 1, 1);
            }
    
            // 写入验证码文字
            const code = generateCaptcha();
            for (let i = 0; i < code.length; i++) {
                ctx.fillStyle = `rgb(${Math.random() * 100}, ${Math.random() * 100}, ${Math.random() * 100})`;
                ctx.font = `${Math.random() * 4 + 18}px Arial`;
                ctx.fillText(code[i], 20 + i * 20, Math.random() * 10 + 25);
            }
    
            return canvas.toDataURL();
        }
    
        // 初始化验证码
        function initCaptcha() {
            captchaImg.src = createCaptchaImage();
        }
    
        // 点击验证码图片刷新
        captchaImg.addEventListener('click', function() {
            initCaptcha();
        });
    
        // 初始化验证码
        initCaptcha();

    // 表单提交处理
    const form = document.getElementById('forgotPasswordForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const captcha = document.getElementById('captcha').value;

            // 验证码验证
            if (captcha.toLowerCase() !== currentCaptcha.toLowerCase()) {
                alert('验证码错误，请重新输入');
                initCaptcha(); // 刷新验证码
                document.getElementById('captcha').value = '';
                return;
            }

            // 邮箱验证
            if (!email) {
                alert('请输入邮箱地址');
                return;
            }

            // 这里添加发送重置链接的逻辑
            alert('重置密码链接已发送到您的邮箱');
            window.location.href = 'login.html';
        });
    }
}); 