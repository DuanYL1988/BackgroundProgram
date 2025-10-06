package com.example.sqlite.controller;

import com.example.sqlite.context.Context;
import com.example.sqlite.model.Account;
import com.example.sqlite.service.AccountServiceImpl;
import com.example.sqlite.service.MenuServiceImpl;
import com.example.sqlite.util.JWTUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class IndexController {

    @Autowired
    MenuServiceImpl menuService;

    @Autowired
    AccountServiceImpl accountService;

    @PostMapping("index")
    public Response doIndex(String username,String password) {
        Response response = accountService.regist(username,password);
        return response;
    }

    @GetMapping("config/userinfo")
    public Response getUserInfo(@RequestHeader(name = Context.AUTHORIZATION) String token){
        Map<String,String> userInfo = JWTUtil.parseToken(token);
        Account account = accountService.getAccount(userInfo.get(Context.USER_ID));
        return CtrlCommon.success(account);
    }
}
