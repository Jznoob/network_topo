document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');

    if (!registerForm) {
        console.error('注册表单未找到');
        return;
    }

    registerForm.addEventListener('submit', async function (e) {
        e.preventDefault(); // 阻止表单默认提交行为

        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirmPassword');

        if (!usernameInput || !passwordInput || !confirmPasswordInput) {
            console.error('输入框缺失');
            return;
        }

        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // 表单校验逻辑
        if (!username || !password || !confirmPassword) {
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
                    password: password
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
