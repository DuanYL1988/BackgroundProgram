package com.example.mysql.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.service.AccountServiceImpl;
import com.example.mysql.service.MenuServiceImpl;
import com.example.mysql.util.JWTUtil;

@RestController
public class IndexController {

    @Autowired
    private AccountServiceImpl accountService;

    @Autowired
    private MenuServiceImpl menuServiceImpl;

    @PostMapping("/login")
    public ResponseResult login(@RequestBody AccountDto user) {
        return accountService.doLogin(user);
    }

    @PostMapping("/getMenuList")
    public ResponseResult getMenuList(@RequestHeader("Authorization") String token) {
        System.out.println("Token: " + token);
        AccountDto loginUser = JWTUtil.parseTokenToAccount(token);
        Map<String, Object> response = new HashMap<>();
        response.put("menuGroup", menuServiceImpl.getAllMenu(loginUser));
        return CtrlCommon.success(response);
    }

}
