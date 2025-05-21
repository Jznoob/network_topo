from django.core.mail import send_mail
from django.http import JsonResponse

def send_test_email(request):
    send_mail(
        subject='测试邮件标题',
        message='你好，这是来自Django的测试邮件内容。',
        from_email=None,  # 使用默认邮箱
        recipient_list=['wh.fan.eud@outlook.com'],
        fail_silently=False,
    )
    return JsonResponse({"msg": "邮件已发送"})