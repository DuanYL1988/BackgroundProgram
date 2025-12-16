package com.example.mysql.repository;

import java.util.List;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.Account;

@SpringBootTest
class AccountRepositoryTest {

    @Autowired
    AccountRepository accountDao;

    @Test
    public void testFindOne() {
        accountDao.selectOneById(String.valueOf(1));
    }

    @Test
    public void testFindByCondition() {
        AccountDto condition = new AccountDto();
        String joinStr = " INNER JOIN MENU ON ACCOUNT.APPLICATION = MENU.APPLICATION AND ACCOUNT.ROLE_ID = MENU.COMP_GROUP ";
        condition.setJoinPart(joinStr);
        List<Account> resultList = accountDao.selectByDto(condition);
        Assert.assertTrue(resultList.size() > 0);
    }

}
