package com.example.sqlite.service;

import com.auth0.jwt.JWT;
import com.example.sqlite.controller.CtrlCommon;
import com.example.sqlite.controller.Response;
import com.example.sqlite.model.Account;
import com.example.sqlite.repository.AccountRepository;
import com.example.sqlite.util.JWTUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AccountServiceImpl {

    @Autowired
    AccountRepository dao;

    /**
     * 用户登录
     * @param userName 用户名
     * @param password 密码
     * @return 登录结果
     */
    public Response regist(String userName, String password) {
        Account coundition = new Account();
        coundition.setLoginName(userName);
        coundition.setPassword(password);
        List<Account> user = dao.selectByDto(coundition);
        if(user.size() == 1) {
            // 生成token
            String token = JWTUtil.createJwt(user.get(0));
            return CtrlCommon.success(token);
        } else {
            return CtrlCommon.error("该用户不存在或重复登录");
        }
    }

    /**
     * 通过用户ID取得用户信息
     * @param id 用户ID
     * @return 用户信息
     */
    public Account getAccount(String id) {
        return dao.selectOneById(Integer.parseInt(id));
    }
}
