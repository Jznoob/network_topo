// 主题切换相关脚本

// 应用主题（浅色/深色）
function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.remove('dark-theme');
    }
}

// 初始化主题设置（根据本地存储）
function initializeTheme() {
    const savedPreferences = JSON.parse(localStorage.getItem('preferences') || '{}');
    const theme = savedPreferences.theme || 'light';
    applyTheme(theme);
    // 同步下拉框选项
    const themeSelect = document.querySelector('select[name="theme"]');
    if (themeSelect) {
        themeSelect.value = theme;
    }
}

// 监听主题选择下拉框变化
function setupThemeListener() {
    const themeSelect = document.querySelector('select[name="theme"]');
    if (themeSelect) {
        themeSelect.addEventListener('change', function(e) {
            const theme = e.target.value;
            applyTheme(theme);
            const savedPreferences = JSON.parse(localStorage.getItem('preferences') || '{}');
            savedPreferences.theme = theme;
            localStorage.setItem('preferences', JSON.stringify(savedPreferences));
        });
    }
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    setupThemeListener();
}); 