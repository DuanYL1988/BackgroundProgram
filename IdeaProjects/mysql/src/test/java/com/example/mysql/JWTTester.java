package com.example.mysql;

import java.util.Map;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.Account;
import com.example.mysql.model.LoginUser;
import com.example.mysql.repository.AccountRepository;
import com.example.mysql.util.JWTUtil;

@SpringBootTest
public class JWTTester {

    @Autowired
    AccountRepository dao;

    @Test
    public void testJwt() {
        Account account = dao.selectOneById(String.valueOf(1));
        LoginUser user = new LoginUser(account, null);
        String token = JWTUtil.createJwt(user);
        System.out.println(token);

        Map<String, String> jsonObj = JWTUtil.parseToken(token);
        for (String key : jsonObj.keySet()) {
            System.out.println(key + " : " + jsonObj.get(key));
        }
        AccountDto decodeUser = JWTUtil.parseTokenToAccount(token);
        System.out.println(decodeUser.getCompany());
    }

    @Test
    public void testEncodePsd() {
        String encodePsd = JWTUtil.getEncodePsd("1");
        System.out.println(encodePsd);
        PasswordEncoder encoder = new BCryptPasswordEncoder();
        Assert.assertTrue(encoder.matches("1", encodePsd));
    }
}
