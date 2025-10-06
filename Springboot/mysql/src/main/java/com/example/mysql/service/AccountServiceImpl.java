package com.example.mysql.service;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;

import com.example.mysql.controller.CtrlCommon;
import com.example.mysql.controller.ResponseResult;
import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.LoginUser;
import com.example.mysql.util.JWTUtil;

@Service
public class AccountServiceImpl {

    @Autowired
    private AuthenticationManager authenticationManager;

    public ResponseResult doLogin(AccountDto user) {
        // AuthenticationManage进行用户认证
        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(user.getUsername(), user.getPassword());
        Authentication authenticate;
        try {
            authenticate = authenticationManager.authenticate(authenticationToken);
        } catch (Exception ex) {
            return CtrlCommon.error("用户不存在");
        }
        // 判断认证是否通过
        if (Objects.isNull(authenticate)) {
            return CtrlCommon.error("用户不存在");
        } else {
            // 生成token存入response并返回
            LoginUser loginUser = (LoginUser) authenticate.getPrincipal();
            Map<String, Object> json = new HashMap<>();
            json.put("token", JWTUtil.createJwt(loginUser));
            return CtrlCommon.success(json);
        }
    }
}
