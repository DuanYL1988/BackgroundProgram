package com.example.mysql.controller;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.service.AccountServiceImpl;
import com.example.mysql.service.MenuServiceImpl;
import com.example.mysql.util.JWTUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
public class IndexController {

    @Autowired
    private AccountServiceImpl accountService;

    @Autowired
    private MenuServiceImpl menuServiceImpl;

    /**
     * 登录页面取得用户下拉列表
     */
    @GetMapping("/initUser")
    public ResponseResult getAccountList() {
        return accountService.getAccountList();
    }

    /**
     * 登录
     * @param user 输入的用户名,密码
     */
    @PostMapping("/login")
    public ResponseResult login(@RequestBody AccountDto user) {
        return accountService.doLogin(user);
    }

    /**
     * 根据登录后用户的token解析用户情报取得相应的菜单
     * @param token token信息
     */
    @PostMapping("/getMenuList")
    public ResponseResult getMenuList(@RequestHeader("Authorization") String token) {
        System.out.println("Token: " + token);
        AccountDto loginUser = JWTUtil.parseTokenToAccount(token);
        Map<String, Object> response = new HashMap<>();
        response.put("menuGroup", menuServiceImpl.getAllMenu(loginUser));
        return CtrlCommon.success(response);
    }

}
