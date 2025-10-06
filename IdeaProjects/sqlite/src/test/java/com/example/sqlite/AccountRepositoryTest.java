package com.example.sqlite;

import com.example.sqlite.model.Account;
import com.example.sqlite.repository.AccountRepository;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class AccountRepositoryTest {

    @Autowired
    AccountRepository testDao;

    @Test
    public void testFindOne(){
        testDao.selectOneById(1);
    }

    @Test
    public void testFindByCondition() {
        Account condition = new Account();
        List<Account> resultList = testDao.selectByDto(condition);
        Assert.assertTrue(resultList.size() > 0);
    }

}
