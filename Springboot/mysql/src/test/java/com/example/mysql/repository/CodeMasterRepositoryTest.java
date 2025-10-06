package com.example.mysql.repository;

import java.util.List;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.CodeMasterDto;
import com.example.mysql.model.CodeMaster;

@SpringBootTest
class CodeMasterRepositoryTest {

    @Autowired
    CodeMasterRepository testRepository;

    @Test
    @Rollback
    public void testSample() {
        // 通过ID检索
        CodeMaster result = testRepository.selectOneById(String.valueOf(1));

        // 动态检索
        CodeMasterDto condition = new CodeMasterDto();
        condition.setApplication(result.getApplication());
        condition.setCategoryId(result.getCategoryId());
        condition.setName(result.getName());

        int searchCount = testRepository.getCountByDto(condition);
        List<CodeMaster> resultList = testRepository.selectByDto(condition);
        Assert.assertTrue(resultList.size() == searchCount);

        // 新ID
        String newId = result.getId() + "_N";
        // 插入
        result.setId(result.getId() + 1);
        testRepository.insert(result);

        // 更新
        testRepository.update(result);

        // 删除
        testRepository.delete(newId);

        // 自定义
        condition.setSelectQuary("APPLICATION AS application,CATEGORY_ID AS categoryId,ROLE_GROUP AS roleGroup,PARENT_ID AS parentId");
        condition.setCondition("");
        condition.setGroupBy("APPLICATION,CATEGORY_ID,ROLE_GROUP,PARENT_ID");
        condition.setHaving("count(PARENT_ID) > 1");
        condition.setOrderBy("1");
        List<CodeMaster> custumList = testRepository.customQuary(condition);
        System.out.println(custumList.size());

    }
}
