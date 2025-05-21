<?php
session_start();

// 设置验证码图片的宽度和高度
$width = 100;
$height = 38;

// 创建图片
$image = imagecreatetruecolor($width, $height);

// 设置背景色为白色
$bg_color = imagecolorallocate($image, 255, 255, 255);
imagefill($image, 0, 0, $bg_color);

// 生成随机验证码
$chars = '2345678abcdefhijkmnpqrstuvwxyzABCDEFGHJKLMNPQRTUVWXY';
$captcha = '';
for ($i = 0; $i < 4; $i++) {
    $captcha .= $chars[rand(0, strlen($chars) - 1)];
}

// 将验证码保存到session
$_SESSION['forgot_password_captcha'] = $captcha;

// 添加干扰线
for ($i = 0; $i < 5; $i++) {
    $line_color = imagecolorallocate($image, rand(150, 200), rand(150, 200), rand(150, 200));
    imageline($image, rand(0, $width), rand(0, $height), rand(0, $width), rand(0, $height), $line_color);
}

// 添加干扰点
for ($i = 0; $i < 100; $i++) {
    $pixel_color = imagecolorallocate($image, rand(150, 200), rand(150, 200), rand(150, 200));
    imagesetpixel($image, rand(0, $width), rand(0, $height), $pixel_color);
}

// 设置验证码文字颜色
$text_color = imagecolorallocate($image, 0, 0, 0);

// 在图片上写入验证码
$font = 5; // 使用内置字体
$font_width = imagefontwidth($font);
$font_height = imagefontheight($font);
$text_width = $font_width * strlen($captcha);
$text_height = $font_height;

// 计算文字位置使其居中
$x = ($width - $text_width) / 2;
$y = ($height - $text_height) / 2;

// 写入文字
imagestring($image, $font, $x, $y, $captcha, $text_color);

// 设置响应头
header('Content-Type: image/png');
header('Cache-Control: no-cache, must-revalidate');

// 输出图片
imagepng($image);
imagedestroy($image);
?> 