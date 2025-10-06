package com.example.mysql.repository;

import java.util.List;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.ArknightsOperatorDto;
import com.example.mysql.model.ArknightsOperator;

@SpringBootTest
class ArknightsOperatorRepositoryTest {

    @Autowired
    ArknightsOperatorRepository testRepository;

    @Test
    @Rollback
    public void testSample() {
        // 通过ID检索
        ArknightsOperator result = testRepository.selectOneById("AA01");

        // 动态检索
        ArknightsOperatorDto condition = new ArknightsOperatorDto();
        condition.setName(result.getName());

        int searchCount = testRepository.getCountByDto(condition);
        List<ArknightsOperator> resultList = testRepository.selectByDto(condition);
        Assert.assertTrue(resultList.size() == searchCount);

        // 新ID
        String newId = result.getId() + "_N";
        // 插入
        result.setId(newId);
        testRepository.insert(result);

        // 更新
        testRepository.update(result);

        // 删除
        testRepository.delete(newId);

        // 自定义
        condition.setSelectQuary("RARITY AS rarity,VOCATION AS vocation,SUB_VOCATION AS subVocation,INFLUENCE AS influence,BIRTH_PLACE AS birthPlace,RACE AS race");
        condition.setCondition("");
        condition.setGroupBy("RARITY,VOCATION,SUB_VOCATION,INFLUENCE,BIRTH_PLACE,RACE");
        condition.setHaving("count(RACE) > 1");
        condition.setOrderBy("1");
        List<ArknightsOperator> custumList = testRepository.customQuary(condition);
        System.out.println(custumList.size());

    }
}
