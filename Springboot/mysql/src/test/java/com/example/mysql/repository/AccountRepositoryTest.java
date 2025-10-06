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
    AccountRepository testDao;

    @Test
    public void testFindOne() {
        testDao.selectOneById(String.valueOf(1));
    }

    @Test
    public void testFindByCondition() {
        AccountDto condition = new AccountDto();
        List<Account> resultList = testDao.selectByDto(condition);
        Assert.assertTrue(resultList.size() > 0);
    }

}
