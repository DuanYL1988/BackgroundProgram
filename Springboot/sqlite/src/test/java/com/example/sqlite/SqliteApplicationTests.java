package com.example.sqlite;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

import com.example.sqlite.model.Hero;
import com.example.sqlite.model.Menu;
import com.example.sqlite.model.Servant;
import com.example.sqlite.model.TableInfo;
import com.example.sqlite.repository.HeroRepository;
import com.example.sqlite.repository.MenuRepository;
import com.example.sqlite.repository.ServantRepository;
import com.example.sqlite.repository.TableInfoRepository;

@SpringBootTest
class SqliteApplicationTests {

    @Autowired
    MenuRepository menuDao;

    @Test
    void testMenuDao() {
        Menu condition = new Menu();
        menuDao.selectByDto(condition);
    }

}
