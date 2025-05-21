<?php
session_start();


$response = ['success' => false];

if (isset($_POST['captcha']) && isset($_SESSION['forgot_password_captcha'])) {
    if (strtolower($_POST['captcha']) === strtolower($_SESSION['forgot_password_captcha'])) {
        $response['success'] = true;
        // 验证成功后清除session中的验证码
        unset($_SESSION['forgot_password_captcha']);
    }
}

header('Content-Type: application/json');
echo json_encode($response);
?> 