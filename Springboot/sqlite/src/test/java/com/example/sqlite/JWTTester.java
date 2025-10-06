package com.example.sqlite;

import com.example.sqlite.model.Account;
import com.example.sqlite.repository.AccountRepository;
import com.example.sqlite.util.JWTUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Map;

@SpringBootTest
public class JWTTester {

    @Autowired
    AccountRepository dao;

    @Test
    public void testJwt(){
        Account account = dao.selectOneById(1);
        String token = JWTUtil.createJwt(account);
        System.out.println(token);

        Map<String, String> jsonObj = JWTUtil.parseToken(token);
        for (String key : jsonObj.keySet()) {
            System.out.println(key + " : " + jsonObj.get(key));
        }
    }
}
