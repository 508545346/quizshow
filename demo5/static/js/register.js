function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click",function(event){
        var $this = $(this)
        var email = $("input[name='email']").val();
        if(!email){
            alert("请输入邮箱！");
            return;
        }
        $.ajax({
            url: "/captcha",
            method: "POST",
            data:{
                "email":email
            },
            success: function(res){
                var code = res['code'];
                if(code === 200){
                    // 取消点击事件
                    $this.off("click");
                    // 开始倒计时
                    var countDown = 60;
                    var timer = setInterval(function(){
                        countDown -= 1;
                        if(countDown > 0){
                            $this.text(countDown+"秒后重新发送");
                        }else{
                            $this.text("获取验证码");
                            // 重新执行下这个函数，重新绑定事件
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时了，那么要记得清除倒计时，否则会一直执行下去
                            clearInterval(timer);
                        }
                    }, 1000);
                    alert("验证码发送成功");
                }else{
                    alert(res['message']);
                }
            }
        })
    });

}

// 等待网页文档所有元素都加载完成之后在执行
$(function(){
    bindCaptchaBtnClick();
});
