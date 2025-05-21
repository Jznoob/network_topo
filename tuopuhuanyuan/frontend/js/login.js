document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerLink = document.getElementById('registerLink');
    let currentCaptcha = '';

    // 检查必要的 DOM 元素是否存在
    if (!loginForm) {
        console.error('登录表单元素未找到');
        return;
    }

    // 获取CSRF Token
    function getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 登录表单提交
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');

        
        // 检查所有必要的输入元素是否存在
        if (!usernameInput || !passwordInput) {
            console.error('必要的表单元素未找到');
            return;
        }
        
        const username = usernameInput.value;
        const password = passwordInput.value;

        try {
            // 获取CSRF令牌
            // const csrfToken = getCSRFToken();
            // if (!csrfToken) {
            //     alert('无法获取安全令牌，请刷新页面重试');
            //     return;
            // }

            // 发送登录请求
            const response = await fetch('http://127.0.0.1:8000/auth/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
                credentials: 'include'  // 包含 cookies
            });

            const data = await response.json();

            if (response.ok) {
                // 登录成功
                const successMessage = document.getElementById('successMessage');
                if (successMessage) {
                    successMessage.style.display = 'block';
                }
                
                // 禁用表单
                const inputs = loginForm.querySelectorAll('input');
                inputs.forEach(input => input.disabled = true);
                const submitButton = loginForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = true;
                }
                
                // 如果选择了"记住我"，保存用户名
                if (rememberMe) {
                    localStorage.setItem('rememberedUsername', username);
                } else {
                    localStorage.removeItem('rememberedUsername');
                }
                
                // 保存登录状态和用户信息
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('currentUser', JSON.stringify(data.user));
                
                // 跳转到主页
                setTimeout(() => {
                    window.location.href = './index.html';
                }, 50);
            } else {
                // 登录失败
                alert(data.error || '登录失败，请检查用户名和密码');
                passwordInput.value = '';
                captchaInput.value = '';
            }
        } catch (error) {
            console.error('登录请求失败:', error);
            alert('登录请求失败，请稍后重试');
        }
    });

    // 注册链接点击事件
    if (registerLink) {
        registerLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/auth/register/';
        });
    }

    // 检查是否有记住的用户名
    const rememberedUsername = localStorage.getItem('rememberedUsername');
    const usernameInput = document.getElementById('username');
    const rememberMeInput = document.getElementById('rememberMe');
    
    if (rememberedUsername && usernameInput && rememberMeInput) {
        usernameInput.value = rememberedUsername;
        rememberMeInput.checked = true;
    }
}); 