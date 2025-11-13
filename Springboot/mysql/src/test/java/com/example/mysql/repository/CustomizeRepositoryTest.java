package com.example.mysql.repository;

import com.example.mysql.dto.FireemblemHeroDto;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.Map;

@SpringBootTest
class CustomizeRepositoryTest {

    @Autowired
    CustomizeRepository testDao;

    @Test
    public void testGetFehSkill(){
        FireemblemHeroDto paramDto = new FireemblemHeroDto();
        paramDto.setName("Lyn");

        List<Map<String, Object>> result = testDao.getFehSkillsInfo(paramDto);

        int dataCnt = 1;
        for (Map<String, Object> row : result) {
            System.out.println("ROW :" + dataCnt + ":" + row.get("imgName"));
            for (Map.Entry<String, Object> entry : row.entrySet()) {
                System.out.println(entry.getKey() + " = " + entry.getValue());
            }
            dataCnt++;
        }
    }
}
