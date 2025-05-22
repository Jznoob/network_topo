window.addEventListener('DOMContentLoaded', async () => {
    // 获取用户信息
    try {
        const token = localStorage.getItem('jwt_token');
        if (!token) {
          throw new Error('No JWT token found');
        }
        const response = await fetch('https://8dbf-111-22-34-251.ngrok-free.app/auth/api/profile/', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',  // GET 请求有时不写也行
            },
            credentials: 'include',
        });

        const data = await response.json();
        console.info('bug');
        if (response.ok) {
            console.info('data:', data);
            document.getElementById('username').value = data.profile.username || '';
            document.getElementById('email').value = data.profile.email || '';
            document.getElementById('registerTime').value = new Date(data.profile.created_at).toLocaleString() ||  '';
        } else {
            alert(data.error || '获取用户信息失败');
        }
    } catch (error) {
        console.error('获取用户信息失败：', error);
        alert('网络异常，请稍后重试');
    }

    // 编辑资料按钮
    document.getElementById('editProfile').addEventListener('click', function () {
        alert('编辑个人资料功能即将上线');
    });

    // 提交修改密码表单
    const securityForm = document.getElementById('securityForm');
    
    securityForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const oldPassword = document.getElementById('oldpassword').value.trim();
        const newPassword = document.getElementById('newpassword').value.trim();
        const confirmPassword = document.getElementById('newpassword2').value.trim();

        if (newPassword !== confirmPassword) {
            alert('新密码与确认密码不一致，请重新输入。');
            return;
        }

        if (newPassword.length < 8) {
            alert('新密码长度不能少于8位');
            return;
        }

        if (!oldPassword || !newPassword) {
            alert('请填写完整的密码信息。');
            return;
        }
        const token = localStorage.getItem('jwt_token');
        console.log('token:', token);
        try {
            
            const response = await fetch('https://8dbf-111-22-34-251.ngrok-free.app/auth/api/password/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token  // 携带JWT
                },
                credentials: 'include',  
                body: JSON.stringify({
                    old_password: oldPassword,
                    new_password: newPassword
                }),
            });

            const data = await response.json();

            if (response.ok) {
                alert('密码修改成功，请重新登录');
                window.location.href = 'login.html';
            } else {
                alert(data.error || '密码修改失败');
            }
        } catch (error) {
            console.error('请求失败:', error);
            alert('网络异常，修改失败');
        }
    });

    // 保存通知设置
    document.getElementById('notificationsForm').addEventListener('submit', function (e) {
        e.preventDefault();
        alert('通知设置已保存');
    });

    // 保存偏好设置并写入 localStorage
    const preferencesForm = document.getElementById('preferencesForm');
    preferencesForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const theme = preferencesForm.querySelector('select[name="theme"]').value;
        const language = preferencesForm.querySelector('select[name="language"]').value;

        localStorage.setItem('preferences', JSON.stringify({ theme, language }));
        alert('偏好设置已保存');
    });

    // 加载保存的偏好设置
    const savedPreferences = JSON.parse(localStorage.getItem('preferences') || '{}');
    if (savedPreferences.theme) {
        document.querySelector('select[name="theme"]').value = savedPreferences.theme;
    }
    if (savedPreferences.language) {
        document.querySelector('select[name="language"]').value = savedPreferences.language;
    }

    // ✅ 保存当前 Tab 到 localStorage
    document.querySelectorAll('a[data-bs-toggle="list"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            const activeTab = e.target.getAttribute('href'); // #security 之类的
            localStorage.setItem('activeProfileTab', activeTab);
        });
    });

    // ✅ 页面加载时恢复之前的 Tab
    const lastTab = localStorage.getItem('activeProfileTab');
    if (lastTab) {
        const tabTrigger = document.querySelector(`a[href="${lastTab}"]`);
        if (tabTrigger) {
            new bootstrap.Tab(tabTrigger).show();
        }
    }
});
