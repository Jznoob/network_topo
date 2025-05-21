<?php
session_start();

// 创建验证码图片
$width = 100;
$height = 49;
$image = imagecreatetruecolor($width, $height);

// 设置背景色
$bgColor = imagecolorallocate($image, 255, 255, 255);
imagefill($image, 0, 0, $bgColor);

// 生成随机验证码
$chars = '2345678abcdefhijkmnpqrstuvwxyzABCDEFGHJKLMNPQRTUVWXY';
$length = 4;
$code = '';
for ($i = 0; $i < $length; $i++) {
    $code .= $chars[rand(0, strlen($chars) - 1)];
}

// 将验证码存入session
$_SESSION['captcha'] = $code;

// 添加干扰线
for ($i = 0; $i < 5; $i++) {
    $lineColor = imagecolorallocate($image, rand(150, 200), rand(150, 200), rand(150, 200));
    imageline($image, rand(0, $width), rand(0, $height), rand(0, $width), rand(0, $height), $lineColor);
}

// 添加干扰点
for ($i = 0; $i < 100; $i++) {
    $pixelColor = imagecolorallocate($image, rand(150, 200), rand(150, 200), rand(150, 200));
    imagesetpixel($image, rand(0, $width), rand(0, $height), $pixelColor);
}

// 写入验证码文字
for ($i = 0; $i < $length; $i++) {
    $textColor = imagecolorallocate($image, rand(0, 100), rand(0, 100), rand(0, 100));
    $fontSize = rand(18, 22);
    $angle = rand(-15, 15);
    $x = 20 + $i * 20;
    $y = rand(25, 35);
    imagestring($image, $fontSize, $x, $y, $code[$i], $textColor);
}

// 输出图片
header('Content-Type: image/png');
imagepng($image);
imagedestroy($image);
?> 