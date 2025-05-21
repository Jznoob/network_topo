<?php
session_start();

$response = array('success' => false);

if (isset($_POST['captcha']) && isset($_SESSION['captcha'])) {
    if (strtolower($_POST['captcha']) === strtolower($_SESSION['captcha'])) {
        $response['success'] = true;
    }
    // 验证完成后清除session中的验证码
    unset($_SESSION['captcha']);
}

header('Content-Type: application/json');
echo json_encode($response);
?> 