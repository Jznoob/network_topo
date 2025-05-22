document.addEventListener('DOMContentLoaded', function () {
    const forgotForm = document.getElementById('forgotPasswordForm');
    const sendCaptchaBtn = document.getElementById('sendCaptchaBtn');

    if (!forgotForm || !sendCaptchaBtn) {
        console.error('忘记密码表单或按钮未找到');
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
//api/forgot-password/
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

    // 提交找回密码表单
    forgotForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const usernameInput = document.getElementById('username');
        const emailInput = document.getElementById('email');
        const captchaInput = document.getElementById('code');
        const newPasswordInput = document.getElementById('new_Password');

        if (!usernameInput || !emailInput || !captchaInput || !newPasswordInput) {
            console.error('输入框缺失');
            return;
        }

        const username = usernameInput.value.trim();
        const email = emailInput.value.trim();
        const captcha = captchaInput.value.trim();
        const newPassword = newPasswordInput.value;

        if (!username || !email || !captcha || !newPassword) {
            alert('所有字段均为必填');
            return;
        }

        if (newPassword.length < 6) {
            alert('新密码长度不能少于6位');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/api/reset-password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    code: captcha,
                    new_password: newPassword
                }),
                credentials: 'include'
            });

            const data = await response.json();
            if (response.ok) {
                alert('密码重置成功，请登录');
                window.location.href = './login.html';
            } else {
                alert(data.error || '密码重置失败');
            }
        } catch (error) {
            console.error('密码重置请求失败:', error);
            alert('网络异常，请稍后重试');
        }
    });
});
