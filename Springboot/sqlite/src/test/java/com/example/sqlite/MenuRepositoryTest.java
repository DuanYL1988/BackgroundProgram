package com.example.sqlite;

import com.example.sqlite.model.Menu;
import com.example.sqlite.repository.MenuRepository;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class MenuRepositoryTest {

    @Autowired
    MenuRepository menuDao;

    @Test
    public void testFindOne(){
        menuDao.selectOneById(1);
    }

    @Test
    public void testFindByCondition() {
        Menu condition = new Menu();
        condition.setApplication("fireemblem");
        List<Menu> resultList = menuDao.selectByDto(condition);
        Assert.assertTrue(resultList.size() > 0);
    }

}
