<?php
session_start();
header('Content-Type: application/json');

$response = ['success' => false];

if (isset($_POST['captcha']) && isset($_SESSION['register_captcha'])) {
    if (strtolower($_POST['captcha']) === strtolower($_SESSION['register_captcha'])) {
        $response['success'] = true;
        // 验证成功后清除session中的验证码
        unset($_SESSION['register_captcha']);
    }
}

echo json_encode($response);
?> 