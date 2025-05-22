document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');

    if (!registerForm) {
        console.error('注册表单未找到');
        return;
    }

    // 发送验证码按钮点击事件
    sendCaptchaBtn.addEventListener('click', async function () {
        const emailInput = document.getElementById('email');
        if (!emailInput) {
            console.error('邮箱输入框未找到');
            return;
        }

        const email = emailInput.value.trim();
        if (!email) {
            alert('请输入邮箱地址');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/api/forgot-password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email }),
                credentials: 'include'
            });

            const data = await response.json();
            if (response.ok) {
                alert('验证码已发送，请查收邮箱');
            } else {
                alert(data.error || '发送验证码失败');
            }
        } catch (error) {
            console.error('发送验证码请求失败:', error);
            alert('网络异常，发送失败');
        }
    });

    registerForm.addEventListener('submit', async function (e) {
        e.preventDefault(); // 阻止表单默认提交行为

        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const emailInput = document.getElementById('email');
        const codeInput = document.getElementById('code');

        if (!usernameInput || !passwordInput || !confirmPasswordInput || !emailInput || !codeInput) {
            console.error('输入框缺失');
            return;
        }

        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const email = emailInput.value;
        const code = codeInput.value;


        // 表单校验逻辑
        if (!username || !password || !confirmPassword || !email || !code) {
            alert('所有字段不能为空');
            return;
        }

        if (password.length < 6) {
            alert('密码长度不能少于6位');
            return;
        }

        if (password !== confirmPassword) {
            alert('两次密码输入不一致');
            return;
        }

        try {
            // 发送注册请求
            const response = await fetch('http://127.0.0.1:8000/auth/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    email: email,
                    code: code
                }),
                credentials: 'include'  // 发送cookie（如有需要）
            });

            const data = await response.json();

            if (response.ok) {
                alert('注册成功，正在跳转到登录页...');
                setTimeout(() => {
                    window.location.href = './login.html';  // 跳转到登录页
                }, 1000);
            } else {
                alert(data.error || '注册失败，请检查输入');
            }

        } catch (error) {
            console.error('注册请求失败:', error);
            alert('网络异常，请稍后重试');
        }
    });

    
});
