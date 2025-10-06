package com.example.oracle;

import com.example.oracle.model.Hero;
import com.example.oracle.repository.HeroRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class OracleApplicationTests {

    @Autowired
    HeroRepository heroDao;

    @Test
    void contextLoads() {
        Hero condition = new Hero();
        heroDao.selectByDto(condition);
    }

}
