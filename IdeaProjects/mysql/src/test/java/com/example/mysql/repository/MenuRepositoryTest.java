package com.example.mysql.repository;

import java.util.List;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.MenuDto;
import com.example.mysql.model.Menu;

@SpringBootTest
class MenuRepositoryTest {

    @Autowired
    MenuRepository testRepository;

    @Test
    @Rollback
    public void testSample() {
        // 通过ID检索
        Menu result = testRepository.selectOneById(String.valueOf(1));

        // 动态检索
        MenuDto condition = new MenuDto();
        condition.setApplication(result.getApplication());
        condition.setMenuCode(result.getMenuCode());

        int searchCount = testRepository.getCountByDto(condition);
        List<Menu> resultList = testRepository.selectByDto(condition);
        Assert.assertTrue(resultList.size() == searchCount);

        // 自定义
        condition.setSelectQuary("APPLICATION AS application,COMP_GROUP AS compGroup,PARENT_ID AS parentId");
        condition.setCondition("");
        condition.setGroupBy("APPLICATION,COMP_GROUP,PARENT_ID");
        condition.setHaving("count(PARENT_ID) > 1");
        condition.setOrderBy("1");
        List<Menu> custumList = testRepository.customQuary(condition);
        System.out.println(custumList.size());

    }
}
