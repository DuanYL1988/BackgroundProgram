package com.example.mysql.repository;

import java.util.List;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.TableInfo;

@SpringBootTest
class TableInfoRepositoryTest {

    @Autowired
    TableInfoRepository testRepository;

    @Test
    @Rollback
    public void testSample() {

        // 动态检索
        TableInfoDto condition = new TableInfoDto();
        condition.setTableName("FIREEMBLEM_HERO");
        condition.setColFifterable("1");

        int searchCount = testRepository.getCountByDto(condition);
        List<TableInfo> resultList = testRepository.selectByDto(condition);
        Assert.assertTrue(resultList.size() == searchCount);

    }
}
