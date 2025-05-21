document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    try {
      const response = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include'  // 如果需要session保持
      });
  
      const data = await response.json();
      if (data.code === 200) {
        alert('登录成功');
        // 这里可以跳转页面，比如 window.location.href = '/profile.html';
      } else {
        alert('登录失败: ' + data.msg);
      }
    } catch (error) {
      alert('请求失败');
      console.error(error);
    }
  });
  