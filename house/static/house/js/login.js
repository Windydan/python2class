$(document).ready(function () {
    // 注册表单校验（已存在，保留原有注册逻辑）
    $('#registeform').bootstrapValidator({
        message: 'This value is not valid',
        fields: {
            name: {
                message: '用户名校验信息',
                validators: {
                    notEmpty: { message: '用户名不能为空' },
                    stringLength: {
                        min: 6,
                        max: 15,
                        message: '用户名长度必须在6到15位之间'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: '用户名只能包含大写、小写、数字和下画线'
                    },
                    different: {
                        field: 'password',
                        message: '用户名不能与密码相同'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: { message: '邮箱不能为空' },
                    emailAddress: { message: '无效的邮箱地址' }
                }
            },
            password: {
                validators: {
                    notEmpty: { message: '密码不能为空' },
                    identical: {
                        field: 'confirmPassword',
                        message: '与确认密码不一致'
                    },
                    different: {
                        field: 'name',
                        message: '密码不能与用户名相同'
                    }
                }
            },
            confirmPassword: {
                validators: {
                    notEmpty: { message: '确认密码不能为空' },
                    identical: {
                        field: 'password',
                        message: '与密码不一致'
                    },
                    different: {
                        field: 'name',
                        message: '确认密码不能与用户名相同'
                    }
                }
            }
        }
    });

    // 注册按钮点击事件
    $('#registe-btn').on('click', function (event) {
        event.preventDefault();
        var validator = $('#registeform').data('bootstrapValidator');
        validator.validate();
        if (validator.isValid()) {
            $.ajax({
                type: 'post',
                url: '/register',
                data: $('#registeform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg']);
                        var validatorObj = $("#registeform").data('bootstrapValidator');
                        if (validatorObj) {
                            $("#registeform").data('bootstrapValidator').destroy();
                            $('#registeform').data('bootstrapValidator', null);
                        }
                    } else {
                        window.location.href = "/user";
                    }
                }
            });
        }
    });

    // 登录表单校验（只初始化一次）
    $('#loginform').bootstrapValidator({
        message: 'This value is not valid',
        fields: {
            name: {
                validators: {
                    notEmpty: { message: '用户名不能为空' },
                    stringLength: {
                        min: 6,
                        max: 15,
                        message: '用户名长度必须在6到15位之间'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: '用户名只能包含大写、小写、数字和下画线'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: { message: '密码不能为空' },
                    different: {
                        field: 'name',
                        message: '密码不能与用户名相同'
                    }
                }
            }
        }
    });

    // 登录按钮点击事件
    $('#login-btn').on('click', function (event) {
        event.preventDefault();
        var validator = $('#loginform').data('bootstrapValidator');
        validator.validate();
        if (validator.isValid()) {
            $.ajax({
                type: 'post',
                url: '/login',
                data: $('#loginform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg']);
                        var validatorObj = $("#loginform").data('bootstrapValidator');
                        if (validatorObj) {
                            $("#loginform").data('bootstrapValidator').destroy();
                            $('#loginform').data('bootstrapValidator', null);
                        }
                    } else {
                        window.location.href = "/user";
                    }
                }
            });
        }
    });
// 退出
$("#logout").on('click', function () {
    $.ajax({
        url: '/logout',
        type: 'get',
        dataType: 'json',
        success: function (res) {
            if (res["valid"] == '1') {   // 退出成功
                alert(res["msg"]);
                window.location.href = '/';
            } else {                     // 退出失败
                alert(res["msg"]);
            }
        }
    })
});
});