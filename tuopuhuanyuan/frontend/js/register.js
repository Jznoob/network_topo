document.addEventListener('DOMContentLoaded', function() {
    let currentCaptcha = '';

    const registerForm = document.getElementById('registerForm');
    const registerLink = document.getElementById('registerLink');
    const captchaImg = document.getElementById('captchaImg');

    // 生成验证码
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
        if (captchaImg) {
            captchaImg.src = createCaptchaImage();
        }
    }

    // 点击验证码图片刷新
    if (captchaImg) {
        captchaImg.addEventListener('click', function() {
            initCaptcha();
        });
    }

    // 初始化验证码
    initCaptcha();

    // 表单提交处理
    const form = document.getElementById('registerForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const captcha = document.getElementById('captcha').value;
            const agreeTerms = document.getElementById('agreeTerms').checked;
        

            // 验证码验证
            if (captcha.toLowerCase() !== currentCaptcha.toLowerCase()) {
                alert('验证码错误，请重新输入');
                initCaptcha();
                document.getElementById('captcha').value = '';
                return;
            }

            // 验证密码是否匹配
            if (password !== confirmPassword) {
                alert('两次输入的密码不一致');
                document.getElementById('password').value = '';
                document.getElementById('confirmPassword').value = '';
                document.getElementById('captcha').value = '';
                initCaptcha();
                return;
            }

            // 验证是否同意条款
            if (!agreeTerms) {
                alert('请阅读并同意服务条款和隐私政策');
                return;
            }

            // 验证必填字段
            if (!username || !email || !password) {
                alert('请填写完整信息');
                return;
            }

            // 这里添加注册逻辑
            alert('注册成功，请登录');
            window.location.href = 'login.html';
        });
    }
}); 