package com.example.mysql.repository;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.ConfigrationDto;
import com.example.mysql.model.Configration;

@SpringBootTest
class ConfigrationRepositoryTest {

    @Autowired
    ConfigrationRepository testRepository;

    @Test
    @Rollback
    public void testSample(){
         // 通过ID检索
        Configration result = testRepository.selectOneById(String.valueOf(1));
        
         // 动态检索
        ConfigrationDto condition = new ConfigrationDto();
        condition.setTableName(result.getTableName());

    }
}
